import pandas as pd

results = pd.read_csv('./data/ext_full.csv')

print("Number of lines present:-",
      len(results))