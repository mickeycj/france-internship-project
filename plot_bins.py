import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys, utils

def create_bins(df, x_steps=10, y_steps=2, outlier_thresh=1, min_thresh=5):
    x_feature, y_feature = 'WTP_AW_angle', 'WTP_AW_speed'
    bins = {}
    x, y = 0, 0
    while y <= 52-y_steps:
        while x <= 180-x_steps:
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} & {1} >= {3} & {1} < {3}+{5}'.format(x_feature, y_feature, x, y, x_steps, y_steps))
            if len(binned_df) > outlier_thresh:
                if len(binned_df) < min_thresh:
                    return create_bins(df, x_steps+2, y_steps+1)
                bins['bin_x{}to{}_y{}to{}'.format(x, x+x_steps, y, y+y_steps)] = binned_df
            x = x+x_steps
        x = 0
        y = y+y_steps
    return bins, x_steps, y_steps

# Read from CSV.
df = utils.read_csv('{}.csv'.format(sys.argv[1]))

# List of relevant features.
wind_features = ['WTP_AW_angle', 'WTP_AW_speed']

# Combine positive and negative wind angle.
df.eval('{0} = abs({0})'.format(wind_features[0]), inplace=True)

# Determine the size of the bins.
bins, x_steps, y_steps = create_bins(df)

# Plot and save the bins.
fig = plt.figure()
ax = fig.gca()
plt.xlabel(wind_features[0])
plt.ylabel(wind_features[1])
plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=0.25)
ax.set_xticks(np.arange(0, 181, x_steps*2))
ax.set_xticks(np.arange(0, 181, x_steps), minor=True)
ax.set_yticks(np.arange(0, 53, y_steps*2))
ax.set_yticks(np.arange(0, 53, y_steps), minor=True)
plt.grid(which='both')
path = './report'
if not os.path.exists(path):
    os.makedirs(path)
plt.savefig('{}/all_bins.pdf'.format(path))
