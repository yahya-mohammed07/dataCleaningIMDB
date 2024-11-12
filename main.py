import pandas as pd
import numpy as np


data = pd.read_csv("messy_IMDB_dataset.csv", sep=';',
                   # Handle various null indicators
                   quotechar='"', encoding='utf-8', na_values=['Nan', 'NULL', 'Not Applicable', 'Inf', '', 'None'],
                   )


def cleaning(dataRef: pd.DataFrame):
  print(dataRef.head())
  dataRef = dataRef.copy()
  # process
  return dataRef


result = cleaning(data)

result.to_csv(r"D:\Programming\Master\dataCleaning\cleaned.csv", index=False)
