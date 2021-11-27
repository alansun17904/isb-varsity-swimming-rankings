import json
from ranker.models import User, Profile, Entry, Hyperparameters
from ranker.weighting import Weight


event_codes = ['FLY50m', 'FR50m', 'BA50m', 'BR50m', 'FLY100m', 'FR100m',
        'BA100m', 'BR100m', 'FR200m', 'FR400m', 'IM100m', 'IM200m']

def find_top_h(name, h, sex):
    hyp = Hyperparameters.objects.all()[0]
    pmale = len(Profile.objects.filter(sex='MALE', is_coach=False))
    pfemale = len(Profile.objects.filter(sex='FEMALE', is_coach=False))

    person = Entry.objects.filter(
            swimmer__user__username=name
    ).order_by('rank')
    ranks = [v.rank for v in person]
    events = {}

    if len(ranks) < hyp.h_index:
        ranks += [pmale if sex == 'MALE' else pfemale] * (hyp.h_index - len(ranks))

    score = sum(ranks[0:hyp.h_index])
    versatility = _versatility(ranks)

    # add versatility to score
    score += versatility

    # add all events into dictionary for ease of assigning bonuses
    for entry in person:
        event = entry.event
        rank = entry.rank
        time = entry.time
        meet = entry.meet
        events[event] = (rank, time, meet)
    return [score, events, name, versatility]

def _versatility(ranks):
    hyp = Hyperparameters.objects.all()[0]
    weightfunc = Weight(hyp.weight_type, hyp.weight_a, hyp.h_index)
    versatility = 0
    for i in range(1, len(ranks)):
        versatility += (ranks[i] - ranks[i-1]) * weightfunc.weighting(i + 1)
    return versatility

def _assign_bonus(name, event_dict):
    hyp = Hyperparameters.objects.all()[0]
    bonus_matrix = hyp.bonus_matrix
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
    hyp = Hyperparameters.objects.all()[0]
    rankings = []
    names = [v.user.username for v in Profile.objects.all().filter(is_coach=False) if v.sex == sex]
    for name in names:
        rank = find_top_h(name, hyp.h_index, sex)
        bonus = _assign_bonus(name, rank[1])
        rank[0] = (1 - bonus) * rank[0]
        rank.append(bonus)
        rankings.append(rank)
    rankings.sort(key=lambda x: x[0])
    return rankings
