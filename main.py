import pandas as pd
import re

data: pd.DataFrame = pd.read_csv("messy_IMDB_dataset_cleaned.csv", sep=';',
                                 # Handle various null indicators
                                 quotechar='"', encoding='utf-8',
                                 )



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
  # duration
  df['Duration'] = df['Duration'].astype(
      str).apply(lambda x: re.sub(r'\D', '', x))

  # country
  df['Country'] = df['Country'].str.strip(
      '123._/\\')  # remove numbers, _, ., \

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
      lambda x: re.sub(r'[a-zA-Z]', '', str(x)))  # remove all a-z

  # votes
  # df['Votes'] = df['Votes'].fillna(' ')
  df['Votes'] = df['Votes'].str.replace('.', ',', regex=False)

  # Score
  def clean_and_format_number(x):
    if pd.isna(x):  # Handle NaN values
      return x

    # Convert to string and replace separators with dot
    x_str = str(x).replace(',', '.').replace(';', '.').replace(':', '.')

    # Remove everything except numbers and dots
    cleaned = re.sub(r'[^0-9.]', '', x_str)

    # Handle multiple dots
    dot_parts = cleaned.split('.')
    if len(dot_parts) > 2:  # Multiple dots
      cleaned = dot_parts[0] + '.' + ''.join(dot_parts[1:])

    # Handle empty string or just a dot
    if not cleaned or cleaned == '.':
      return 'Invalid'

    try:
      num = float(cleaned)
      # Format the number
      if num.is_integer():
        return str(int(num))
      else:
        # Round to 1 decimal place
        formatted = "{:.1f}".format(num)
        # If it ends with .0, convert to integer
        if formatted.endswith('.0'):
          return formatted[:-2]
        return formatted
    except ValueError:
      return 'Invalid'

  df['Score'] = df['Score'].apply(clean_and_format_number)

  return df


result = cleaning(data)
print(result.head())

result.to_csv(
    r"D:\Programming\Master\dataCleaning\cleaned.csv", index=False)
