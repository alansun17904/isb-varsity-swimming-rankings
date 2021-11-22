"""Alan Sun
Settings and Hyperparameter Initialization, ISB Varsity Swim Rankings
11/21/2021

This module contains functionality that loads the settings from the
hyperparameter initialization files. It will then encapsulate all of these
settings for ease of use by the ranking module. During initialization, the
functions herein will also prompt the user to confirm the settings that have
been imported. We note that there are two files the user define for ranking
to proceed:
    - `bonus-matrix.settings` which contains the bonus matrix that is applied
    as the bonus score. The inputs in this file must be in matrix form.
    Moveover, its columns must have valid event codes.
    - `hyperparameter.settings` which contains the rest of the hyperparameters
    that is necessary for optimization. These specific arguments are described
    in full in the README.md
"""

import os
import sys
import pandas as pd



class Settings:
    def __init__(self):
        self.bonus_matrix = {}
        self.hyperparameters = {}

    def load_hyperparameters(self):
        """
        (description): Load hyperparamters reads the hyperparameters from the
        hyperparamter file `hyperparameters.settings`. It the initializes the
        self.hyperparameters attribute with the information from this file.
        Such that this newly initialied dictionary's keys are the argument
        names and its values are the given argument values.

        (error handling): If this initialization is confronted with invalid
        arguments the program will ignore the invalid arguments and only read
        the valid ones.
        """
        if not os.path.exists("hyperparameters.settings"):
            raise RuntimeError("The required `hyperparameters.settings` file \
                    does not exist, please manually create this file in the \
                    top level directory to proceed.")

        fp = open("hyperparameters.settings", "r")
        for line in fp.readlines():
            # assume that the first word must be the argument name, also assume
            # that argument values are separated by spaces.
            args = list(map(lambda x: x.strip(), line.split(" ")))
            if args[0] == "attendence-bonus":
                print(args[1])
                if args[1].lower() == "false":
                    self.hyperparameters[args[0]] = (False, 0)
                else:
                    self.hyperparameters[args[0]] = (True, float(args[2]))
            elif args[0] == "h-index":
                self.hyperparameters[args[0]] = float(args[1])
            elif args[0] == "weighting-function":
                self.hyperparameters[args[0]] = (args[1], float(args[2]))
            else:
                self.hyperparameters[args[0]] = args[1]
        if len(self.hyperparameters.keys()) < 3:
            raise RuntimeError("There were not enough arguments provided.");
        fp.close()

    def load_bonus(self):
        """
        (description): Load bonus matrix from the bonus matrix file. It will
        initialize the attribute `self.bonus_matrix` with a dictionary whose
        keys represent the event codes and whose values represent a list of
        floats which correspond to the percentage discount of each rank in
        increasing order.

        (error handling): If the format of this bonus matrix file is invalid
        or if the event codes are given this will result in undefined behavior
        by the ranker.
        """
        df = pd.read_csv("bonus-matrix.settings", index_col=False, delimiter=' ')
        for column in df.columns:
            if column == "Rank":
                continue
            else:
                self.bonus_matrix[column] = df[column].tolist()
        return df
