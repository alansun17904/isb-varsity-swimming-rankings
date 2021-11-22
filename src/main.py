from load_settings import Settings
from weighting import Weight
from ranker import Ranker


print("Welcome to the ISB Varsity Swim Team Ranker")
sex = input("Choose girls/boys team to rank (enter FEMALE or MALE, respectively): ")
output = input("Choose an output file name: ")
print("Initializing settings...")
setting = Settings()
setting.load_bonus()
setting.load_hyperparameters()
print("Initializing weighting function...")
weights = Weight(setting.hyperparameters["weighting-function"][0],
        setting.hyperparameters["weighting-function"][1],
        setting.hyperparameters["h-index"])
print("Initializing ranker...")
ranker = Ranker(sex, weights, setting)
print("Ranking...")
ranker.export_ranks(output)
