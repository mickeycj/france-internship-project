import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, re, sys, utils

# Ignore PyPlot warning.
plt.rcParams.update({'figure.max_open_warning': 0})

# List of relevant features and axis names.
wind_features = ['WTP_AW_angle', 'WTP_AW_speed']
axis_names = ['Wind Angle (˚)', 'Wind Speed (knot)']

# Create bins.
def create_bins(df, dx=10, dy=2, outlier_thresh=10, min_thresh=100):
    bins = {}
    max_x, max_y = 0, 0
    while max_x < 180:
        max_y = 0
        while max_y < 52:
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} & {1} >= {3} & {1} < {3}+{5}'.format(wind_features[0], wind_features[1], max_x, max_y, dx, dy))
            if len(binned_df) >= outlier_thresh:
                if len(binned_df) < min_thresh:
                    return create_bins(df, dx+2, dy+1)
                added_max_x = max_x+dx
                if added_max_x > 180:
                    added_max_x = 180
                bins['bin_x{}to{}_y{}to{}'.format(max_x, added_max_x, max_y, max_y+dy)] = binned_df
            max_y+=dy
        max_x+=dx
    return bins, dx, dy, max_x, max_y

# Plot angle-speed space.
def plot_angle_speed(df, x_start, y_start, x_finish, y_finish, dx, dy, markersize, base_path, fname, is_main_plot=False):
    fig = plt.figure()
    ax = fig.gca()
    plt.xlabel(axis_names[0])
    plt.ylabel(axis_names[1])
    plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=markersize)
    if is_main_plot and x_finish > 181:
        plt.axvline(180, label='Maximum Angle', color='black', lw=1.0, ls='--')
        plt.legend(loc='upper right')
    ax.set_xticks(np.arange(x_start, x_finish, dx))
    ax.set_yticks(np.arange(y_start, y_finish, dy))
    plt.grid(lw=.75)
    plt.tight_layout()
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    plt.savefig('{}/{}.pdf'.format(base_path, fname))
    plt.clf()

# Read from CSV.
df = utils.read_csv('{}.csv'.format(sys.argv[1]))

# Combine positive and negative wind angle.
df.eval('{0} = abs({0})'.format(wind_features[0]), inplace=True)

bin_properties = [(2, 1, 1, 10), (5, 1, 3, 50), (10, 2, 10, 100)]
for dx, dy, outlier_thresh, min_thresh in bin_properties:
    # Determine the size of the bins.
    bins, dx, dy, max_x, max_y = create_bins(df, dx=dx, dy=dy, outlier_thresh=outlier_thresh, min_thresh=min_thresh)

    # Plot and save the bins.
    base_path = './report/outlier{}_min{}'.format(outlier_thresh, min_thresh)
    plot_angle_speed(df, 0, 0, max_x+1, max_y+1, dx, dy, 0.25, base_path, 'bins', is_main_plot=True)
    for bin_name, binned_df in bins.items():
        x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(r'\d+', bin_name)]
        dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
        plot_angle_speed(binned_df, x_start, y_start, x_finish+dx, y_finish+dy, dx, dy, 3, base_path, bin_name)
