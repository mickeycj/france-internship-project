import pandas as pd
import utils

# Read from CSV.
df = utils.read_csv('./data/datalog-05102017-Full_1Hz.1s_clean.csv')

# Max-min.
# The column names to be reduced/combined.
max_min_cols = ['Max_1s_FBM_P_lfwd', 'Max_1s_FBM_P_uaft', 'Max_1s_FBM_P_ufwd',
                'Max_1s_FBM_S_laft', 'Max_1s_FBM_S_lfwd', 'Max_1s_FBM_S_uaft', 'Max_1s_FBM_S_ufwd',
                'Max_1s_HUL_C_lport', 'Max_1s_HUL_C_lstbd', 'Max_1s_HUL_C_uport', 'Max_1s_HUL_C_ustbd',
                'Max_1s_HUL_P_lport', 'Max_1s_HUL_P_lstbd', 'Max_1s_HUL_P_uport', 'Max_1s_HUL_P_ustbd',
                'Max_1s_HUL_S_lport', 'Max_1s_HUL_S_lstbd', 'Max_1s_HUL_S_uport', 'Max_1s_HUL_S_ustbd',
                'Max_1s_Foil_B_P_01_i', 'Max_1s_Foil_B_P_01_o',
                'Max_1s_Foil_B_S_01_i', 'Max_1s_Foil_B_S_01_o',
                'Max_1s_Foil_ELE_C_01_p', 'Max_1s_Foil_ELE_C_01_s',
                'Max_1s_Foil_ELE_LOAD_P', 'Max_1s_Foil_ELE_LOAD_S',
                'Min_1s_FBM_P_lfwd', 'Min_1s_FBM_P_uaft', 'Min_1s_FBM_P_ufwd',
                'Min_1s_FBM_S_laft', 'Min_1s_FBM_S_lfwd', 'Min_1s_FBM_S_uaft', 'Min_1s_FBM_S_ufwd',
                'Min_1s_HUL_C_lport', 'Min_1s_HUL_C_lstbd', 'Min_1s_HUL_C_uport', 'Min_1s_HUL_C_ustbd',
                'Min_1s_HUL_P_lport', 'Min_1s_HUL_P_lstbd', 'Min_1s_HUL_P_uport', 'Min_1s_HUL_P_ustbd', 
                'Min_1s_HUL_S_lport', 'Min_1s_HUL_S_lstbd', 'Min_1s_HUL_S_uport', 'Min_1s_HUL_S_ustbd',
                'Min_1s_Foil_B_P_01_i', 'Min_1s_Foil_B_P_01_o',
                'Min_1s_Foil_B_S_01_i', 'Min_1s_Foil_B_S_01_o',
                'Min_1s_Foil_ELE_C_01_p', 'Min_1s_Foil_ELE_C_01_s',
                'Min_1s_Foil_ELE_LOAD_P', 'Min_1s_Foil_ELE_LOAD_S']

# Reduce different sensors from the same location to the same columns and print the result.
transformed_df = utils.transform(df.copy(deep=True), max_min_cols, '{}.*')
utils.print_data(transformed_df.head(10), 7)

# Find the correlation between the speed of the boat with different sensors.
utils.print_corr(utils.find_corr_of(transformed_df, 'WTP_SelBoatSpd'))

# Plot the correlation matrix.
utils.plot_corr(transformed_df)

# Average.
# The column names to be reduced/combined.
avg_cols = ['1s_FBM_P_lfwd', '1s_FBM_P_uaft', '1s_FBM_P_ufwd',
            '1s_FBM_S_laft', '1s_FBM_S_lfwd', '1s_FBM_S_uaft', '1s_FBM_S_ufwd',
            '1s_HUL_C_lport', '1s_HUL_C_lstbd', '1s_HUL_C_uport', '1s_HUL_C_ustbd',
            '1s_HUL_P_lport', '1s_HUL_P_lstbd', '1s_HUL_P_uport', '1s_HUL_P_ustbd',
            '1s_HUL_S_lport', '1s_HUL_S_lstbd', '1s_HUL_S_uport', '1s_HUL_S_ustbd',
            '1s_Foil_B_P_01_i', '1s_Foil_B_P_01_o',
            '1s_Foil_B_S_01_i', '1s_Foil_B_S_01_o',
            '1s_Foil_ELE_C_01_p', '1s_Foil_ELE_C_01_s',
            '1s_Foil_ELE_LOAD_P', '1s_Foil_ELE_LOAD_S']

# Reduce different sensors from the same location to the same columns and print the result.
transformed_df = utils.transform(df.copy(deep=True), avg_cols, '.*{}.*')
utils.print_data(transformed_df.head(10), 7)

# Find the correlation between the speed of the boat with different sensors.
utils.print_corr(utils.find_corr_of(transformed_df, 'WTP_SelBoatSpd'))

# Plot the correlation matrix.
utils.plot_corr(transformed_df)
