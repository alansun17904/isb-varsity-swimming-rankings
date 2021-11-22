import pytest
import os
import sys
from src.load_settings import Settings

class TestSettings:
    def setup_method(self, test_method):
        os.chdir(os.getcwd())
        os.remove("hyperparameters.settings")
        self.setting = Settings()
        open("hyperparameters.settings", "x")

    def test_load_hyperparameter_invalid(self):
        fp = open("hyperparameters.settings", "w")
        fp.write("h-index 2\n")
        try:
            self.setting.load_hyperparameters()
        except RuntimeError:
            assert True
        else:
            assert False

    def test_load_hyperparameter_simple(self):
        fp = open("hyperparameters.settings", "w")
        fp.write("h-index 10\n")
        fp.write("attendence-bonus true 0.04\n")
        fp.write("weighting-function exponential 0.1\n")
        fp.close()
        self.setting.load_hyperparameters()
        hyp = self.setting.hyperparameters
        assert hyp["h-index"] == 10
        assert hyp["attendence-bonus"][0]
        assert hyp["attendence-bonus"][1] == 0.04
        assert hyp["weighting-function"][0] == "exponential"
        assert hyp["weighting-function"][1] == 0.1

    def test_load_hyperparameter_complex(self):
        pass

    def test_load_hyperparameter_weighting(self):
        pass
