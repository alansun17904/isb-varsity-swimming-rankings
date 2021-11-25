"""Alan Sun
Ranker, ISB Varsity Swim Rankings
11/21/2021

This module contains funtionality that ranks swimmers based on the
hyperparameters given in settings and the weighting function. The
times for each swimmer that is being ranked is given in the excel sheet:
`rankings-to-date.xlsx`.
"""

import os
import pandas as pd
from load_settings import Settings


class Ranker:
    def __init__(self, sex, weights, settings):
        self.df = pd.read_excel("rankings-to-date.xlsx")
        self.sex = sex
        self.weights = weights
        self.settings = settings
        self.ranks = []
        self.names = self.df[self.df["Sex"] == self.sex]["Name"].unique()

    def _find_top_h(self, name, h):
        person = self.df[self.df["Name"] == name].sort_values(by=["Ranking", "Event"])
        ranks = person["Ranking"].tolist()
        events = {}

        # target person did not swim h-index events.
        if len(ranks) < h:
            ranks += [len(self.names)] * (int(h) - len(person))
        # we find person's top h events
        score = self._sum_ranks(ranks[:int(h)])

        # add all events into dictionary for ease of assigning bonuses
        for row in range(len(person)):
            event = person["Event"].iloc[row]
            rank = person["Ranking"].iloc[row]
            time = person["Time"].iloc[row]
            meet = person["Meet"].iloc[row]
            events[event] = (rank, time, meet)
        return [score, events, name]

    def _sum_ranks(self, ranks):
        score = 0
        for i in range(len(ranks)):
            score += ranks[i] * self.weights.weighting(i + 1)
        return score

    def _assign_bonus(self, name, event_dict):
        bonus = 0.0
        bonus_matrix = self.settings.bonus_matrix

        # check for attendence bonus
        if self.settings.hyperparameters["attendance-bonus"][0]:
            attendence = pd.read_excel("attendence.xlsx",
                        sheet_name=self.sex)
            p = attendence[attendence["Name"] == name]

            if len(p) != 0 and p.didAttendAllPractices:
                bonus += self.settings.hyperparameters["attendance-bonus"][1]

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

    def rank(self):
        rankings = []
        for name in self.names:
            rank = self._find_top_h(name,
                    self.settings.hyperparameters["h-index"])
            rank[0] = (1 - self._assign_bonus(name, rank[1])) * rank[0]
            rankings.append(rank)
        rankings.sort(key=lambda x: x[0])
        return rankings

    def export_ranks(self, fname):
        rankings = self.rank()
        fp = open(fname, "w")

        for rank, info in enumerate(rankings):
            fp.write(f"Bonus Pct.: {self._assign_bonus(info[2], info[1])}\n")
            fp.write(f"${str(rank + 1).ljust(3)} ---> {info[2].ljust(15)}\n")
            fp.write(f"Score: {round(info[0], 3)}\n")
            for event, score in info[1].items():
                num = score[0]
                time = score[1]
                meet = score[2]
                fp.write(f"{event.ljust(7)}: {str(num).ljust(3)} ---> ")
                fp.write(f"{str(time).ljust(10)} @ {meet}\n")
            fp.write("*-------------------*\n")

