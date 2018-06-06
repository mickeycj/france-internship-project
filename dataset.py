def read_data():
    import pandas as pd

    return pd.read_csv('./data/datalog-05102017-Full_1Hz.1s_clean.csv', sep=';')

def find_corr_of(df, target):
    import math

    for col in df.drop(['date TU', 'heure TU', 'latitude', 'longitude'], axis=1).columns:
        if col != target:
            corr = df[target].corr(df[col])
            if not math.isnan(corr):
                yield (col, corr)

def plot_correlation_matrix(df):
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    
    _, ax = plt.subplots(figsize=(14, 10))
    corr = df.corr()
    sns.heatmap(corr,
                mask=np.zeros_like(corr, dtype=np.bool),
                cmap=sns.diverging_palette(220, 10, as_cmap=True),
                square=True,
                ax=ax)
    plt.show()

# Read from CSV.
df = read_data()

# Show the sample.
sample = df.head(n=10)
i = 0
while i<len(sample.keys()):
    print('{}\n'.format(sample.iloc[:, i:i+5]))
    i+=6

# Find the correlation between the speed of the boat with different sensors.
for col, corr in sorted(list(find_corr_of(df, 'WTP_SelBoatSpd')),
                        key=lambda x: x[1],
                        reverse=True):
    print('{}: {}'.format(col, corr))

# Plot the correlation matrix.
plot_correlation_matrix(df)
