import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, re, sys, utils

# Ignore PyPlot warning.
plt.rcParams.update({'figure.max_open_warning': 0})

# List of relevant features.
wind_features = ['WTP_AW_angle', 'WTP_AW_speed']

# Create bins.
def create_bins(df, dx=10, dy=2, outlier_thresh=10, min_thresh=100):
    bins = {}
    x, y = 0, 0
    while x <= 180:
        y = 0
        while y <= 52:
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} & {1} >= {3} & {1} < {3}+{5}'.format(wind_features[0], wind_features[1], x, y, dx, dy))
            if len(binned_df) >= outlier_thresh:
                if len(binned_df) < min_thresh:
                    return create_bins(df, dx+2, dy+1)
                x_end, y_end = x+dx, y+dy
                bins['bin_x{}to{}_y{}to{}'.format(x, x_end, y, y_end)] = binned_df
            y = y+dy
        x = x+dx
    if x > 180:
        x = 180
    return bins, dx, dy, x, y

# Plot angle-speed space.
def plot_angle_speed(df, x_start, y_start, x_finish, y_finish, dx, dy, markersize, base_path, fname):
    fig = plt.figure()
    ax = fig.gca()
    plt.xlabel(wind_features[0])
    plt.ylabel(wind_features[1])
    plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=markersize)
    ax.set_xticks(np.arange(x_start, x_finish, dx))
    ax.set_yticks(np.arange(y_start, y_finish, dy))
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
bins, dx, dy, x_max, y_max = create_bins(df)

# Plot and save the bins.
base_path = './report'
plot_angle_speed(df, 0, 0, x_max+1, y_max+1, dx, dy, 0.25, base_path, 'bins')
for bin_name, df in bins.items():
    x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(r'\d+', bin_name)]
    dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
    plot_angle_speed(df, x_start, y_start, x_finish+dx, y_finish+dy, dx, dy, 3, base_path, bin_name)
