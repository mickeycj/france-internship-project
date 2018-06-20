import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import math, os, re, sys

# Ignore PyPlot warning.
plt.rcParams.update({'figure.max_open_warning': 0})

# Possible bin angles.
bin_angles = [4, 5, 6, 9, 10, 12, 15, 18, 20, 30, 45]

# List of relevant features and axis names.
wind_features = ['WTP_AW_angle', 'WTP_AW_speed']
boat_speed_feature = 'WTP_SelBoatSpd'
bins_axis_names = ['Wind Angle (˚)', 'Wind Speed (knot)']
boxplot_axis_name = 'Boat Speed (knot)'

def read_csv(fname):
    """Read a CSV file to a Pandas Dataframe"""
    return pd.read_csv(fname, sep=';')

def transform_columns(df, new_cols, regex):
    """Transform the dataset"""
    for col in new_cols:
        filtered = df.filter(regex=(regex.format(col)))
        df[col] = filtered.mean(axis=1)
        df.drop(filtered.columns, axis=1, inplace=True)
    cols = df.columns.values.tolist()
    split = len(cols)-len(new_cols)
    return df[cols[:4] + cols[split:] + cols[4:split]]

def create_if_not_exist(path):
    """Create a directory if not exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def create_bins(df, dx=bin_angles[0], dy=2, min_thresh=100, tries=0):
    """Create bins"""
    bins = {}
    max_x = 0
    while max_x < 180:
        max_y = 0
        while max_y < math.ceil(df.loc[df[wind_features[1]].idxmax()][wind_features[1]]):
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} & {1} >= {3} & {1} < {3}+{5}'.format(wind_features[0], wind_features[1], max_x, max_y, dx, dy))
            if len(binned_df) >= int(math.ceil(min_thresh * 0.1)):
                if len(binned_df) < min_thresh:
                    return create_bins(df, dx=bin_angles[tries+1], dy=dy+2, min_thresh=min_thresh, tries=tries+1)
                bins['bin_x{}to{}_y{}to{}'.format(max_x, max_x+dx, max_y, max_y+dy)] = binned_df
            max_y+=dy
        max_x+=dx
    return bins, dx, dy, max_x, max_y

def plot_wind_angle_speed(df, x_start, y_start, x_finish, y_finish, dx, dy, markersize, base_path, fname):
    """Plot the wind angle-speed space"""
    plt.xlabel(bins_axis_names[0])
    plt.ylabel(bins_axis_names[1])
    plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=markersize)
    plt.xticks(np.arange(x_start, x_finish, dx))
    plt.yticks(np.arange(y_start, y_finish, dy))
    plt.grid(lw=.75)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig('{}/{}.pdf'.format(base_path, fname))
    plt.clf()

def plot_boxplot(df, column, outliers, base_path, fname):
    """Plot the boxplot for boat speed"""
    df.boxplot(column=column, showfliers=outliers)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.ylabel(boxplot_axis_name)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig('{}/{}.pdf'.format(base_path, fname))
    plt.clf()

def plot_corr(df, target, base_path, fname):
    """Plot the correlations with boat speed"""
    corrs = {}
    for col in df.drop(['date TU', 'heure TU', 'latitude', 'longitude'], axis=1).columns:
        if col != target:
            corr = df[target].corr(df[col])
            if not math.isnan(corr):
                corrs[col] = corr
    sorted_corrs = sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True)[:20]
    sorted_corrs = sorted(sorted_corrs, key=lambda x: x[1], reverse=True)
    cols = [target] + [i[0] for i in sorted_corrs]
    corr = df[cols].corr()
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, lw=.75)
    plt.xticks(rotation=30, ha='right', fontsize=5)
    plt.yticks(fontsize=5)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig('{}/{}.pdf'.format(base_path, fname))
    plt.clf()

# Read from CSV.
df = read_csv('{}.csv'.format(sys.argv[1]))

# Transform the dataset to decrease the number of features.
df = transform_columns(df,
                    ['1s_FBM_P_lfwd', '1s_FBM_P_uaft', '1s_FBM_P_ufwd',
                    '1s_FBM_S_laft', '1s_FBM_S_lfwd', '1s_FBM_S_uaft', '1s_FBM_S_ufwd',
                    '1s_HUL_C_lport', '1s_HUL_C_lstbd', '1s_HUL_C_uport', '1s_HUL_C_ustbd',
                    '1s_HUL_P_lport', '1s_HUL_P_lstbd', '1s_HUL_P_uport', '1s_HUL_P_ustbd',
                    '1s_HUL_S_lport', '1s_HUL_S_lstbd', '1s_HUL_S_uport', '1s_HUL_S_ustbd',
                    '1s_Foil_B_P_01_i', '1s_Foil_B_P_01_o',
                    '1s_Foil_B_S_01_i', '1s_Foil_B_S_01_o',
                    '1s_Foil_ELE_C_01_p', '1s_Foil_ELE_C_01_s',
                    '1s_Foil_ELE_LOAD_P', '1s_Foil_ELE_LOAD_S'],
                    '.*{}.*')

# Combine positive and negative wind angles.
df.eval('{0} = abs({0})'.format(wind_features[0]), inplace=True)

# Create different-sized bins.
bin_sizes = [10, 50, 100]
for min_thresh in bin_sizes:
    # Determine the size of the bins.
    bins, dx, dy, max_x, max_y = create_bins(df, min_thresh=min_thresh)

    # Plot and save the bins.
    base_path = './report/min_thresh_{}'.format(min_thresh)
    plot_wind_angle_speed(df, 0, 0, max_x+1, max_y+1, dx, dy, 0.25, base_path, 'bins')
    base_path = '{}/bins'.format(base_path)
    for bin_name, binned_df in bins.items():
        bin_base_path = '{}/{}'.format(base_path, bin_name)
        x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(r'\d+', bin_name)]
        dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
        plot_wind_angle_speed(binned_df, x_start, y_start, x_finish+dx, y_finish+dy, dx, dy, 3, bin_base_path, 'bin')
        plot_boxplot(binned_df, boat_speed_feature, False, bin_base_path, 'boxplot')
        plot_corr(binned_df, boat_speed_feature, bin_base_path, 'corr')
