import pandas as pd

input_dir = 'Secret/'

def read_input_excel(file, sheet_name):
    df_sheet = pd.read_excel(input_dir + file, sheet_name, dtype=str)
    return df_sheet