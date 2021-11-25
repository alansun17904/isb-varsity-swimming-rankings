import json
from ranker.models import User, Profile, Entry, Hyperparameters
from ranker.weighting import Weight


event_codes = ['FLY50m', 'FR50m', 'BA50m', 'BR50m', 'FLY100m', 'FR100m',
        'BA100m', 'BR100m', 'FR200m', 'FR400m', 'IM100m', 'IM200m']

hyp = Hyperparameters.objects.all()[0]
pmale = len([v for v in Profile.objects.all() if v.sex == 'MALE'])
pfemale = len([v for v in Profile.objects.all() if v.sex == 'FEMALE'])
weightfunc = Weight(hyp.weight_type, hyp.weight_a, hyp.h_index)

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
    for entry in range(len(person)):
        event = row.event
        rank = row.rank
        time = row.time
        meet = row.meet
        events[event] = (rank, time, meet)
    return [score, events, name]

def _sum_ranks(ranks):
    score = 0
    for i in range(len(ranks)):
        score += ranks[i] * weightfunc(i + 1)
    return score
