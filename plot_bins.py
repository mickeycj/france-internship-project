import math
import os
import re
import sys

import chardet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Ignore PyPlot warning.
plt.rcParams.update({'figure.max_open_warning': 0})

# Command line arguments.
version = sys.argv[1]
fnames = sys.argv[2:]

# Data path.
data_path = './data/{}'.format(version)

# Possible bin angles.
bin_angles = [5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72]

# List of relevant features and axis names.
identifier_features = [
    ('Date', 'Date'),
    ('Hour', 'Hour'),
    ('VarFilter_WTP_GPS1_lat', 'Latitude'),
    ('VarFilter_WTP_GPS1_long', 'Longitude')
]
fiber_optics_structure_features = [
    ('1s_FBM_P_TEMP', 'Front Beam - Temp. (Port)'),
    ('1s_FBM_P_TEMP_To', 'Front Beam - Temp. To. (Port)'),
    ('1s_FBM_P_To', 'Front Beam - To. (Port)'),
    ('1s_FBM_P_laft', 'Front Beam - Lower Aft Rake (Port)'),
    ('1s_FBM_P_laft', 'Front Beam - Lower Forward Rake (Port)'),
    ('1s_FBM_P_uaft', 'Front Beam - Upper Aft Rake (Port)'),
    ('1s_FBM_P_uaft', 'Front Beam - Upper Forward Rake (Port)'),
    ('1s_FBM_S_TEMP', 'Front Beam - Temp. (Starboard)'),
    ('1s_FBM_S_TEMP_To', 'Front Beam - Temp. To. (Starboard)'),
    ('1s_FBM_S_To', 'Front Beam - To. (Starboard)'),
    ('1s_FBM_S_laft', 'Front Beam - Lower Aft Rake (Starboard)'),
    ('1s_FBM_S_laft', 'Front Beam - Lower Forward Rake (Starboard)'),
    ('1s_FBM_S_uaft', 'Front Beam - Upper Aft Rake (Starboard)'),
    ('1s_FBM_S_uaft', 'Front Beam - Upper Forward Rake (Starboard)'),
    ('1s_HUL_C_TEMP', 'Hull - Temp. (Center)'),
    ('1s_HUL_C_TEMP_To', 'Hull - Temp. To. (Center)'),
    ('1s_HUL_C_To', 'Hull - To. (Center)'),
    ('1s_HUL_C_lport', 'Hull - Lower Port (Center)'),
    ('1s_HUL_C_lstbd', 'Hull - Lower Starboard (Center)'),
    ('1s_HUL_C_uport', 'Hull - Upper Port (Center)'),
    ('1s_HUL_C_ustbd', 'Hull - Upper Starboard (Center)'),
    ('1s_HUL_P_TEMP', 'Hull - Temp. (Port)'),
    ('1s_HUL_P_TEMP_To', 'Hull - Temp. To. (Port)'),
    ('1s_HUL_P_To', 'Hull - To. (Port)'),
    ('1s_HUL_P_lport', 'Hull - Lower Port (Port)'),
    ('1s_HUL_P_lstbd', 'Hull - Lower Starboard (Port)'),
    ('1s_HUL_P_uport', 'Hull - Upper Port (Port)'),
    ('1s_HUL_P_ustbd', 'Hull - Upper Starboard (Port)'),
    ('1s_HUL_S_TEMP', 'Hull - Temp. (Starboard)'),
    ('1s_HUL_S_TEMP_To', 'Hull - Temp. To. (Starboard)'),
    ('1s_HUL_S_To', 'Hull - To. (Starboard)'),
    ('1s_HUL_S_lport', 'Hull - Lower Port (Starboard)'),
    ('1s_HUL_S_lstbd', 'Hull - Lower Starboard (Starboard)'),
    ('1s_HUL_S_uport', 'Hull - Upper Port (Starboard)'),
    ('1s_HUL_S_ustbd', 'Hull - Upper Starboard (Starboard)')
]
fiber_optics_appendix_features = [
    ('1s_Foil_B_P_1_TEMP', 'Board Temp. (Port)'),
    ('1s_Foil_B_P_1_TEMP_To', 'Board Temp. To. (Port)'),
    ('1s_Foil_B_P_1_To', 'Board To. (Port)'),
    ('1s_Foil_B_P_1_i', 'Board Deformation - Inside (Port)'),
    ('1s_Foil_B_P_1_o', 'Board Deformation - Outside (Port)'),
    ('1s_Foil_B_S_1_TEMP', 'Board Temp. (Starboard)'),
    ('1s_Foil_B_S_1_TEMP_To', 'Board Temp. To. (Starboard)'),
    ('1s_Foil_B_S_1_To', 'Board To. (Starboard)'),
    ('1s_Foil_B_S_1_i', 'Board Deformation - Inside (Starboard)'),
    ('1s_Foil_B_S_1_o', 'Board Deformation - Outside (Starboard)'),
    ('1s_Foil_RUD_C_1_TEMP', 'Board Temp. (Center)'),
    ('1s_Foil_RUD_C_1_TEMP_To', 'Board Temp. To. (Center)'),
    ('1s_Foil_RUD_C_To', 'Board To. (Center)'),
    ('1s_Foil_RUD_C_1_e_0_P', 'Rudder - Port (Center)'),
    ('1s_Foil_RUD_C_1_e_0_S', 'Rudder - Starboard (Center)')
]
other_sensor_features = [
    ('IxBlue_Heading', 'IxB - Heading'),
    ('IxBlue_Heave', 'IxB - Heave'),
    ('IxBlue_HeaveAccel', 'IxB - Heave Accel.'),
    ('IxBlue_Pitch', 'IxB - Pitch'),
    ('IxBlue_PitchRate', 'IxB - Pitch RAte'),
    ('IxBlue_Roll', 'IxB - Roll'),
    ('IxBlue_RollRate', 'IxB - Roll Rate'),
    ('IxBlue_SurgeAccel', 'IxB - Surge Accel.'),
    ('IxBlue_SwayAccel', 'IxB - Sway Accel.'),
    ('IxBlue_YawRate', 'IxB - Yaw Rate'),
    ('RM_RM', 'Righting Moment'),
    ('VarFilter_sirius_b2_ 1', 'Mainsail 2'),
    ('VarFilter_sirius_b2_ 2', 'Mainsail 1'),
    ('VarFilter_sirius_b2_ 3', 'Mainsail Full'),
    ('VarFilter_WTP_Mainsheet_Load', 'Mainsail Load'),
    ('VarFilter_WTP_Forestay_0_Load', 'Forestay Load (J0)'),
    ('VarFilter_WTP_Forestay_1_Load', 'Forestay Load (J1)'),
    ('VarFilter_WTP_Forestay_2_Load', 'Forestay Load (J2)'),
    ('VarFilter_WTP_MastRot', 'Mast Rotation Angle'),
    ('VarFilter_WTP_CBoard_Elevator_angle', 'Board - Elevator Angle (Center)'),
    ('VarFilter_WTP_CBoard_Trimmer_angle_norm', 'Board - Trimmer Angle (Center)'),
    ('VarFilter_WTP_Cboard_Extension', 'Board - Extension (Center)'),
    ('VarFilter_WTP_Cboard_Load', 'Board - Load (Center)'),
    ('VarFilter_WTP_Foil_Prt_Extension', 'Board - Extension (Port)'),
    ('VarFilter_WTP_Foil_Prt_Rake', 'Board - Rake (Port)'),
    ('VarFilter_WTP_Foil_Stb_Extension', 'Board - Extension (Starboard)'),
    ('VarFilter_WTP_Foil_Stb_Rake', 'Board - Rake (Starboard)'),
    ('VarFilter_WTP_Rudder_Angle_CC', 'Rudder - Angle (Center)'),
    ('VarFilter_WTP_Rudder_CC_Elevator_angle', 'Rudder - Elevator Angle (Center)'),
    ('VarFilter_WTP_Rudder_Angle_Prt', 'Rudder - Angle (Port)'),
    ('VarFilter_WTP_Rudder_Prt_Elevator_angle', 'Rudder - Elevator Angle (Port)'),
    ('VarFilter_WTP_Rudder_Prt_Load_I', 'Rudder - Inside Load (Port)'),
    ('VarFilter_WTP_Rudder_Prt_Load_O', 'Rudder - Outside Load (Port)'),
    ('VarFilter_WTP_Rudder_Angle_Stb', 'Rudder - Angle (Starboard)'),
    ('VarFilter_WTP_Rudder_Stb_Elevator_angle', 'Rudder - Elevator Angle (Starboard)'),
    ('VarFilter_WTP_Rudder_Stb_Load_I', 'Rudder - Inside Load (Starboard)'),
    ('VarFilter_WTP_Rudder_Stb_Load_O', 'Rudder - Outside Load (Starboard)'),
    ('VarFilter_WTP_Shroud_Prt_Load', 'Shroud - Load (Port)'),
    ('VarFilter_WTP_Shroud_Stb_Load', 'Shroud - Load (Starboard)')
]
wind_features = [
    ('VarFilter_WTP_TW_angle', 'Wind Angle'),
    ('VarFilter_WTP_TW_speed', 'Wind Speed')
]
target_features = [
    ('VarFilter_WTP_SelBoatSpd', 'Boat Speed')
]
old_wind_features = ['VarFilter_WTP_AW_angle', 'VarFilter_WTP_AW_speed']
boat_speed_feature = 'VarFilter_WTP_SelBoatSpd'
bins_axis_names = ['Wind Angle (˚)', 'Wind Speed (knots)']
boxplot_axis_name = 'Boat Speed (knots)'

# Regular expressions.
feature_regex = r'.*{}.*'
bin_dimensions_regex = r'[+-]?\d+'

def read_csv(fnames):
    """Read CSV file(s) to a Pandas Dataframe"""
    print('Creating dataframe...')
    def detect_and_read(fname):
        with open(fname, 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
            print('File {}\'s encoding: {}'.format(fname, encoding))
            return pd.read_csv(fname, sep=';', encoding=encoding)
    df = pd.concat(map(lambda fname: detect_and_read(fname), fnames), sort=False)
    print('Dataframe created!')
    return df

def transform_columns(df, identifier_cols, cols_to_transform, other_cols, regex):
    """Transform the dataset"""
    print('Transforming columns...')
    transformed_df = pd.DataFrame()
    for old_col, new_col in identifier_cols + cols_to_transform + other_cols:
        if (old_col, new_col) not in identifier_cols + other_cols:
            transformed_df[new_col] = df.filter(regex=(regex.format(old_col))).mean(axis=1)
        else:
            transformed_df[new_col] = df[old_col]
    print('Columns transformed!')
    return transformed_df

def create_bins(df, dx=bin_angles[0], dy=1, min_thresh=10, tries=0):
    """Create bins"""
    if tries == 0:
        print('Creating bins...')
    else:
        print('Bin\'s size adjusted. Tries: {}'.format(tries))
    bins = {}
    max_x = -180
    while max_x < 180:
        max_y = 0
        while max_y < math.ceil(df[old_wind_features[1]].max()):
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} & {1} >= {3} & {1} < {3}+{5}'.format(old_wind_features[0], old_wind_features[1], max_x, max_y, dx, dy))
            if len(binned_df) >= int(math.ceil(min_thresh*0.1)):
                if len(binned_df) < min_thresh:
                    return create_bins(df, dx=bin_angles[tries+1], dy=dy+1, min_thresh=min_thresh, tries=tries+1)
                bins['bin_x{}to{}_y{}to{}'.format(max_x, max_x+dx, max_y, max_y+dy)] = binned_df
            max_y+=dy
        max_x+=dx
    if tries == 0:
        tries_str = '1 try'
    else:
        tries_str = '{} tries'.format(tries+1)
    print('Bins created after {}!'.format(tries_str))
    return bins, dx, dy, max_x, max_y

def create_if_not_exist(path):
    """Create a directory if not exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print('Directory {} created!'.format(path))

def plot_wind_angle_speed(df, x_start, y_start, x_finish, y_finish, dx, dy, markersize, base_path, fname):
    """Plot the wind angle-speed space"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    plt.xlabel(bins_axis_names[0])
    plt.ylabel(bins_axis_names[1])
    plt.plot(df[old_wind_features[0]].tolist(), df[old_wind_features[1]].tolist(), 'ko', markersize=markersize)
    plt.xticks(np.arange(x_start, x_finish, dx))
    plt.yticks(np.arange(y_start, y_finish, dy))
    plt.grid(lw=.75)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

def plot_boxplot(df, base_path, fname):
    """Plot the boxplot for boat speed"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    df.boxplot(column=boat_speed_feature, showfliers=df[boat_speed_feature].median() == df[boat_speed_feature].mode().iloc[0])
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.ylabel(boxplot_axis_name)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

def plot_corr(df, num_features, base_path, fname):
    """Plot the correlations with boat speed"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    corrs = {}
    for col in df.drop(old_wind_features, axis=1).columns:
        if col != boat_speed_feature:
            corr = df[boat_speed_feature].corr(df[col])
            if not math.isnan(corr):
                corrs[col] = corr
    sorted_corrs = sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True)[:num_features]
    sorted_corrs = sorted(sorted_corrs, key=lambda x: x[1], reverse=True)
    cols = [boat_speed_feature] + [x[0] for x in sorted_corrs]
    corr = df[cols].corr()
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, lw=.75)
    plt.xticks(rotation=30, ha='right', fontsize=5)
    plt.yticks(fontsize=5)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

print('Initializing bins creation...')
print('------------------------------------------')
# Read from CSV file(s).
df = read_csv(map(lambda arg: '{}/{}.csv'.format(data_path, arg), fnames))

print('------------------------------------------')
# Transform the dataset to decrease the number of features.
df = transform_columns(df,
                    identifier_features,
                    fiber_optics_structure_features + fiber_optics_appendix_features,
                    other_sensor_features + wind_features + target_features,
                    feature_regex)
print(df.columns)

# Create different-sized bins.
# bin_sizes = [10, 50, 100]
# for min_thresh in bin_sizes:
#     print('------------------------------------------')
#     # Determine the size of the bins.
#     print('Creating bins with minimum size of {}.'.format(min_thresh))
#     bins, dx, dy, _, max_y = create_bins(df, min_thresh=min_thresh)

#     # Plot and save the bins.
#     print('Creating plots...')
#     reports_path = './reports/{}/min_thresh_{}'.format(version, min_thresh)
#     plot_wind_angle_speed(df, -180, 0, 180+1, max_y+1, dx, dy, 0.25, reports_path, 'bins')
#     reports_path = '{}/bins'.format(reports_path)
#     for bin_name, binned_df in bins.items():
#         bin_reports_path = '{}/{}'.format(reports_path, bin_name)
#         x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(bin_dimensions_regex, bin_name)]
#         dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
#         plot_wind_angle_speed(binned_df, x_start, y_start, x_finish+dx, y_finish+dy, dx, dy, 3, bin_reports_path, 'bin')
#         plot_boxplot(binned_df, bin_reports_path, 'boxplot')
#         plot_corr(binned_df, 20, bin_reports_path, 'corr')
#     print('All plots saved!')
# print('------------------------------------------')
# print('Bins creation finished!')
