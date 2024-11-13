import pandas as pd
import numpy as np
import re

data = pd.read_csv("messy_IMDB_dataset_cleaned.csv", sep=';',
                   # Handle various null indicators
                   quotechar='"', encoding='utf-8'
                   )

data = data.replace('', np.nan)
data = data.replace(' ', np.nan)


def cleaning(df: pd.DataFrame):
  df = df.copy()
  # process
  df.drop_duplicates()  # reduce redundancy
  df.dropna()  # remove empty rows
  df.dropna(how='all', axis=1, inplace=True)  # remove columns
  ##
  df['Original title'] = df['Original title'].str.strip(
      '123._/\\')  # remove numbers, _, ., \

  df['Release year'] = pd.to_datetime(
      # one format for the date
      df['Release year'], format='mixed', errors='coerce')
  df['Duration'] = df['Duration'].astype(
      str).apply(lambda x: re.sub(r'\D', '', x))
  df['Country'] = df['Country'].astype(
      str).apply(lambda x: re.sub(r'\W', '', x))
  df['Country'] = df['Country'].astype(
      str).apply(lambda x: re.sub(r'\d', '', x))

  # Handle missing values and convert to string
  df['Content Rating'] = df['Content Rating'].fillna('').astype(str)
  df['Content Rating'] = df['Content Rating'].str.replace(
      'Unrated', 'Not Rated')
  df['Content Rating'] = df['Content Rating'].str.replace(
      'Approved', 'G')
  df['Content Rating'] = df['Content Rating'].apply(
      lambda x: re.sub(r'^PG$', 'PG-13', x))

  # director
  df['Director'] = df['Director'].str.strip(
      '123._/\\')  # remove numbers, _, ., \

  # income
  df['Income'] = df['Income'].apply(
      lambda x: re.sub(r'(\d)(?=(\d{3})+(?!\d))', r'\1,', str(x)))
  df['Income'] = df['Income'].apply(
      lambda x: re.sub(r'[a-zA-Z]', '', str(x)))

  return df


result = cleaning(data)
print(result.head())

result.to_csv(r"D:\Programming\Master\dataCleaning\cleaned.csv", index=False)
