import json
from ranker.models import User, Profile, Entry, Hyperparameters
from ranker.weighting import Weight


event_codes = ['FLY50m', 'FR50m', 'BA50m', 'BR50m', 'FLY100m', 'FR100m',
        'BA100m', 'BR100m', 'FR200m', 'FR400m', 'IM100m', 'IM200m']

hyp = Hyperparameters.objects.all()[0]
pmale = len([v for v in Profile.objects.all() if v.sex == 'MALE'])
pfemale = len([v for v in Profile.objects.all() if v.sex == 'FEMALE'])
weightfunc = Weight(hyp.weight_type, hyp.weight_a, hyp.h_index)
bonus_matrix = hyp.bonus_matrix

def calculate_entry_ranks():
    # since the rankings for boys and girls are calculated separately
    # this needs to be done in two iterations.
    # calculate ranks for each event
    # thus, we need to filter by event codes first
    girls = [v for v in Entry.objects.all() if v.swimmer.sex == 'MALE']
    boys = [v for v in Entry.objects.all() if v.swimmer.sex == 'FEMALE']

    for bg in [girls, boys]:
        for event in event_codes:
            entries = [v for v in bg if v.event == event]
            entries.sort(key=lambda x: float(x.time))
            for rank, entry in enumerate(entries):
                entry.rank = rank + 1
                entry.save()

def find_top_h(name, h, sex):
    person = [v for v in Entry.objects.all()
                if v.swimmer.user.username == name]
    ranks = [v.rank for v in person]
    events = {}

    ranks.sort()
    if len(ranks) < hyp.h_index:
        ranks += [pmale if sex == 'MALE' else pfemale] * (hyp.h_index - len(ranks))

    score = _sum_ranks(ranks)

    # add all events into dictionary for ease of assigning bonuses
    for entry in person:
        event = entry.event
        rank = entry.rank
        time = entry.time
        meet = entry.meet
        events[event] = (rank, time, meet)
    return [score, events, name]

def _sum_ranks(ranks):
    score = 0
    for i in range(len(ranks)):
        score += ranks[i] * weightfunc.weighting(i + 1)
    return score

def _assign_bonus(name, event_dict):
    bonus = 0.0

    # check for attendence bonus
    if hyp.attendance_bonus:
        person = [v for v in Profile.objects.all()
                if v.user.username == name][0]
        if person.attendance:
            bonus += hyp.attendance_weight

    # check for top event bonuses
    event_bonuses = []

    for key in bonus_matrix.keys():
        if key in event_dict.keys():
            rank = event_dict[key][0]
            # if the rank is sufficient to qualify for a bonus
            if rank - 1 < len(bonus_matrix[key]):
                event_bonuses.append(bonus_matrix[key][rank - 1])
    event_bonuses.sort(reverse=True)
    bonus += sum(event_bonuses[:2])
    return bonus

def rank(sex='FEMALE'):
    rankings = []
    names = [v.user.username for v in Profile.objects.all() if v.sex == sex]
    for name in names:
        rank = find_top_h(name, hyp.h_index, sex)
        rank[0] = (1 - _assign_bonus(name, rank[1])) * rank[0]
        rankings.append(rank)
    rankings.sort(key=lambda x: x[0])
    return rankings
