import pandas as pd

def read_data():
    return pd.read_csv('./data/datalog-05102017-Full_1Hz.1s_clean.csv', sep=';')

def print_data(df, steps):
    i = 0
    while i<len(df.keys()):
        print('{}\n'.format(df.iloc[:, i:i+steps]))
        i+=(steps+1)
