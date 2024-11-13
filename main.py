import pandas as pd
import numpy as np


data = pd.read_csv("messy_IMDB_dataset_cleaned.csv", sep=';',
                   # Handle various null indicators
                   quotechar='"', encoding='utf-8', na_values=['Nan', 'NULL', 'Not Applicable', 'Inf', '', 'None'],
                   )


def cleaning(df: pd.DataFrame):
  df = df.copy()
  # process
  df.drop_duplicates()  # reduce redundancy
  df['Original title'] = df['Original title'].str.strip(
      '123._/\\')  # remove numbers, _, ., \
  df.dropna(axis='rows')  # remove empty rows
  df.dropna(how='all', axis=1, inplace=True)  # remove empty columns

  return df


result = cleaning(data)
print(result.head())

result.to_csv(r"D:\Programming\Master\dataCleaning\cleaned.csv", index=False)
