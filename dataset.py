import pandas as pd

def read_data():
    return pd.read_csv('./datalog-05102017-Full_1Hz.1s_clean.csv', sep=';')
