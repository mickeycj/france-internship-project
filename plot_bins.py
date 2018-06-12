import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re, sys, utils

# Ignore PyPlot warning.
plt.rcParams.update({'figure.max_open_warning': 0})

# List of relevant features.
wind_features = ['WTP_AW_angle', 'WTP_AW_speed']

# Create bins.
def create_bins(df, x_steps=10, y_steps=2, outlier_thresh=1, min_thresh=5):
    bins = {}
    x, y = 0, 0
    while y <= 52-y_steps:
        while x <= 180-x_steps:
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} & {1} >= {3} & {1} < {3}+{5}'.format(wind_features[0], wind_features[1], x, y, x_steps, y_steps))
            if len(binned_df) > outlier_thresh:
                if len(binned_df) < min_thresh:
                    return create_bins(df, x_steps+2, y_steps+1)
                bins['bin_x{}to{}_y{}to{}'.format(x, x+x_steps, y, y+y_steps)] = binned_df
            x = x+x_steps
        x = 0
        y = y+y_steps
    return bins, x_steps, y_steps

# Plot angle-speed space.
def plot_angle_speed(df, x_start, y_start, x_finish, y_finish, x_steps, y_steps, markersize, base_path, fname):
    fig = plt.figure()
    ax = fig.gca()
    plt.xlabel(wind_features[0])
    plt.ylabel(wind_features[1])
    plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=markersize)
    ax.set_xticks(np.arange(x_start, x_finish, x_steps*2))
    ax.set_xticks(np.arange(x_start, x_finish, x_steps), minor=True)
    ax.set_yticks(np.arange(y_start, y_finish, y_steps*2))
    ax.set_yticks(np.arange(y_start, y_finish, y_steps), minor=True)
    plt.grid(which='both')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    plt.savefig('{}/{}.pdf'.format(base_path, fname))
    plt.clf()

# Read from CSV.
df = utils.read_csv('{}.csv'.format(sys.argv[1]))

# Combine positive and negative wind angle.
df.eval('{0} = abs({0})'.format(wind_features[0]), inplace=True)

# Determine the size of the bins.
bins, x_steps, y_steps = create_bins(df)

# Plot and save the bins.
base_path = './report'
plot_angle_speed(df, 0, 0, 181, 53, x_steps, y_steps, 0.25, base_path, 'all_bins')
for bin_name, df in bins.items():
    x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(r'\d+', bin_name)]
    dx, dy = (x_finish-x_start)/8.0, (y_finish-y_start)/8.0
    plot_angle_speed(df, x_start, y_start, x_finish+dx, y_finish+dy, dx, dy, 3, base_path, bin_name)
