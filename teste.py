import pandas as pd

small_array = ['foo', 'bar', 'baz']

# create a sample dataframe with string values
df = pd.DataFrame({'column_name': ['foo_value', 'bar_value', 'other_value', 'baz_value']})

# check if each substring in the small array is part of the 'column_name' column of the dataframe
is_in_df = df['column_name'].str.contains('|'.join(small_array))

# print out the results
for value, is_in in zip(df['column_name'], is_in_df):
    if is_in:
        print(f"{value} found in df")
    else:
        print(f"{value} not found in df")