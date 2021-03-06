# List of relevant features and axis names.
identifier_features = [
    ('Date', 'Date'),
    ('Hour', 'Hour'),
    ('VarFilter_WTP_GPS1_lat', 'Latitude'),
    ('VarFilter_WTP_GPS1_long', 'Longitude')
]
fiber_optics_structure_features = [
    ('Max_1s_FBM_P_TEMP', 'Max_Front_Beam_Temp_Port'),
    ('Max_1s_FBM_P_TEMP_To', 'Max_Front_Beam_Temp_To_Port'),
    ('Max_1s_FBM_P_To', 'Max_Front_Beam_To_Port'),
    ('Max_1s_FBM_P_laft', 'Max_Front_Beam_Lower_Aft_Rake_Port'),
    ('Max_1s_FBM_P_laft', 'Max_Front_Beam_Lower_Forward_Rake_Port'),
    ('Max_1s_FBM_P_uaft', 'Max_Front_Beam_Upper_Aft_Rake_Port'),
    ('Max_1s_FBM_P_uaft', 'Max_Front_Beam_Upper_Forward_Rake_Port'),
    ('Max_1s_FBM_S_TEMP', 'Max_Front_Beam_Temp_Starboard'),
    ('Max_1s_FBM_S_TEMP_To', 'Max_Front_Beam_Temp_To_Starboard'),
    ('Max_1s_FBM_S_To', 'Max_Front_Beam_To_Starboard'),
    ('Max_1s_FBM_S_laft', 'Max_Front_Beam_Lower_Aft_Rake_Starboard'),
    ('Max_1s_FBM_S_laft', 'Max_Front_Beam_Lower_Forward_Rake_Starboard'),
    ('Max_1s_FBM_S_uaft', 'Max_Front_Beam_Upper_Aft_Rake_Starboard'),
    ('Max_1s_FBM_S_uaft', 'Max_Front_Beam_Upper_Forward_Rake_Starboard'),
    ('Max_1s_HUL_C_TEMP', 'Max_Hull_Temp_Center'),
    ('Max_1s_HUL_C_TEMP_To', 'Max_Hull_Temp_To_Center'),
    ('Max_1s_HUL_C_To', 'Max_Hull_To_Center'),
    ('Max_1s_HUL_C_lport', 'Max_Hull_Lower_Port_Center'),
    ('Max_1s_HUL_C_lstbd', 'Max_Hull_Lower_Starboard_Center'),
    ('Max_1s_HUL_C_uport', 'Max_Hull_Upper_Port_Center'),
    ('Max_1s_HUL_C_ustbd', 'Max_Hull_Upper_Starboard_Center'),
    ('Max_1s_HUL_P_TEMP', 'Max_Hull_Temp_Port'),
    ('Max_1s_HUL_P_TEMP_To', 'Max_Hull_Temp_To_Port'),
    ('Max_1s_HUL_P_To', 'Max_Hull_To_Port'),
    ('Max_1s_HUL_P_lport', 'Max_Hull_Lower_Port_Port'),
    ('Max_1s_HUL_P_lstbd', 'Max_Hull_Lower_Starboard_Port'),
    ('Max_1s_HUL_P_uport', 'Max_Hull_Upper_Port_Port'),
    ('Max_1s_HUL_P_ustbd', 'Max_Hull_Upper_Starboard_Port'),
    ('Max_1s_HUL_S_TEMP', 'Max_Hull_Temp_Starboard'),
    ('Max_1s_HUL_S_TEMP_To', 'Max_Hull_Temp_To_Starboard'),
    ('Max_1s_HUL_S_To', 'Max_Hull_To_Starboard'),
    ('Max_1s_HUL_S_lport', 'Max_Hull_Lower_Port_Starboard'),
    ('Max_1s_HUL_S_lstbd', 'Max_Hull_Lower_Starboard_Starboard'),
    ('Max_1s_HUL_S_uport', 'Max_Hull_Upper_Port_Starboard'),
    ('Max_1s_HUL_S_ustbd', 'Max_Hull_Upper_Starboard_Starboard'),
    ('Min_1s_FBM_P_TEMP', 'Min_Front_Beam_Temp_Port'),
    ('Min_1s_FBM_P_TEMP_To', 'Min_Front_Beam_Temp_To_Port'),
    ('Min_1s_FBM_P_To', 'Min_Front_Beam_To_Port'),
    ('Min_1s_FBM_P_laft', 'Min_Front_Beam_Lower_Aft_Rake_Port'),
    ('Min_1s_FBM_P_laft', 'Min_Front_Beam_Lower_Forward_Rake_Port'),
    ('Min_1s_FBM_P_uaft', 'Min_Front_Beam_Upper_Aft_Rake_Port'),
    ('Min_1s_FBM_P_uaft', 'Min_Front_Beam_Upper_Forward_Rake_Port'),
    ('Min_1s_FBM_S_TEMP', 'Min_Front_Beam_Temp_Starboard'),
    ('Min_1s_FBM_S_TEMP_To', 'Min_Front_Beam_Temp_To_Starboard'),
    ('Min_1s_FBM_S_To', 'Min_Front_Beam_To_Starboard'),
    ('Min_1s_FBM_S_laft', 'Min_Front_Beam_Lower_Aft_Rake_Starboard'),
    ('Min_1s_FBM_S_laft', 'Min_Front_Beam_Lower_Forward_Rake_Starboard'),
    ('Min_1s_FBM_S_uaft', 'Min_Front_Beam_Upper_Aft_Rake_Starboard'),
    ('Min_1s_FBM_S_uaft', 'Min_Front_Beam_Upper_Forward_Rake_Starboard'),
    ('Min_1s_HUL_C_TEMP', 'Min_Hull_Temp_Center'),
    ('Min_1s_HUL_C_TEMP_To', 'Min_Hull_Temp_To_Center'),
    ('Min_1s_HUL_C_To', 'Min_Hull_To_Center'),
    ('Min_1s_HUL_C_lport', 'Min_Hull_Lower_Port_Center'),
    ('Min_1s_HUL_C_lstbd', 'Min_Hull_Lower_Starboard_Center'),
    ('Min_1s_HUL_C_uport', 'Min_Hull_Upper_Port_Center'),
    ('Min_1s_HUL_C_ustbd', 'Min_Hull_Upper_Starboard_Center'),
    ('Min_1s_HUL_P_TEMP', 'Min_Hull_Temp_Port'),
    ('Min_1s_HUL_P_TEMP_To', 'Min_Hull_Temp_To_Port'),
    ('Min_1s_HUL_P_To', 'Min_Hull_To_Port'),
    ('Min_1s_HUL_P_lport', 'Min_Hull_Lower_Port_Port'),
    ('Min_1s_HUL_P_lstbd', 'Min_Hull_Lower_Starboard_Port'),
    ('Min_1s_HUL_P_uport', 'Min_Hull_Upper_Port_Port'),
    ('Min_1s_HUL_P_ustbd', 'Min_Hull_Upper_Starboard_Port'),
    ('Min_1s_HUL_S_TEMP', 'Min_Hull_Temp_Starboard'),
    ('Min_1s_HUL_S_TEMP_To', 'Min_Hull_Temp_To_Starboard'),
    ('Min_1s_HUL_S_To', 'Min_Hull_To_Starboard'),
    ('Min_1s_HUL_S_lport', 'Min_Hull_Lower_Port_Starboard'),
    ('Min_1s_HUL_S_lstbd', 'Min_Hull_Lower_Starboard_Starboard'),
    ('Min_1s_HUL_S_uport', 'Min_Hull_Upper_Port_Starboard'),
    ('Min_1s_HUL_S_ustbd', 'Min_Hull_Upper_Starboard_Starboard')
]
fiber_optics_appendix_features = [
    ('Max_1s_Foil_B_P_1_TEMP', 'Max_Board_Temp_Port'),
    ('Max_1s_Foil_B_P_1_TEMP_To', 'Max_Board_Temp_To_Port'),
    ('Max_1s_Foil_B_P_1_To', 'Max_Board_To_Port'),
    ('Max_1s_Foil_B_P_1_i', 'Max_Board_Deformation_Inside_Port'),
    ('Max_1s_Foil_B_P_1_o', 'Max_Board_Deformation_Outside_Port'),
    ('Max_1s_Foil_B_S_1_TEMP', 'Max_Board_Temp_Starboard'),
    ('Max_1s_Foil_B_S_1_TEMP_To', 'Max_Board_Temp_To_Starboard'),
    ('Max_1s_Foil_B_S_1_To', 'Max_Board_To_Starboard'),
    ('Max_1s_Foil_B_S_1_i', 'Max_Board_Deformation_Inside_Starboard'),
    ('Max_1s_Foil_B_S_1_o', 'Max_Board_Deformation_Outside_Starboard'),
    ('Max_1s_Foil_RUD_C_1_TEMP', 'Max_Board_Temp_Center'),
    ('Max_1s_Foil_RUD_C_1_TEMP_To', 'Max_Board_Temp_To_Center'),
    ('Max_1s_Foil_RUD_C_To', 'Max_Board_To_Center'),
    ('Max_1s_Foil_RUD_C_1_e_0_P', 'Max_Rudder_Port_Center'),
    ('Max_1s_Foil_RUD_C_1_e_0_S', 'Max_Rudder_Starboard_Center'),
    ('Min_1s_Foil_B_P_1_TEMP', 'Min_Board_Temp_Port'),
    ('Min_1s_Foil_B_P_1_TEMP_To', 'Min_Board_Temp_To_Port'),
    ('Min_1s_Foil_B_P_1_To', 'Min_Board_To_Port'),
    ('Min_1s_Foil_B_P_1_i', 'Min_Board_Deformation_Inside_Port'),
    ('Min_1s_Foil_B_P_1_o', 'Min_Board_Deformation_Outside_Port'),
    ('Min_1s_Foil_B_S_1_TEMP', 'Min_Board_Temp_Starboard'),
    ('Min_1s_Foil_B_S_1_TEMP_To', 'Min_Board_Temp_To_Starboard'),
    ('Min_1s_Foil_B_S_1_To', 'Min_Board_To_Starboard'),
    ('Min_1s_Foil_B_S_1_i', 'Min_Board_Deformation_Inside_Starboard'),
    ('Min_1s_Foil_B_S_1_o', 'Min_Board_Deformation_Outside_Starboard'),
    ('Min_1s_Foil_RUD_C_1_TEMP', 'Min_Board_Temp_Center'),
    ('Min_1s_Foil_RUD_C_1_TEMP_To', 'Min_Board_Temp_To_Center'),
    ('Min_1s_Foil_RUD_C_To', 'Min_Board_To_Center'),
    ('Min_1s_Foil_RUD_C_1_e_0_P', 'Min_Rudder_Port_Center'),
    ('Min_1s_Foil_RUD_C_1_e_0_S', 'Min_Rudder_Starboard_Center')
]
other_sensor_features = [
    ('IxBlue_Heading', 'IxB_Heading'),
    ('IxBlue_Heave', 'IxB_Heave'),
    ('IxBlue_HeaveAccel', 'IxB_Heave_Accel'),
    ('IxBlue_Pitch', 'IxB_Pitch'),
    ('IxBlue_PitchRate', 'IxB_Pitch_Rate'),
    ('IxBlue_Roll', 'IxB_Roll'),
    ('IxBlue_RollRate', 'IxB_Roll_Rate'),
    ('IxBlue_SurgeAccel', 'IxB_Surge_Accel'),
    ('IxBlue_SwayAccel', 'IxB_Sway_Accel'),
    ('IxBlue_YawRate', 'IxB_Yaw_Rate'),
    ('RM_RM', 'Righting_Moment'),
    ('VarFilter_sirius_b2_ 1', 'Mainsail_2'),
    ('VarFilter_sirius_b2_ 2', 'Mainsail_1'),
    ('VarFilter_sirius_b2_ 3', 'Mainsail_Full'),
    ('VarFilter_WTP_Mainsheet_Load', 'Mainsail_Load'),
    ('VarFilter_WTP_Forestay_0_Load', 'Forestay_Load_J0'),
    ('VarFilter_WTP_Forestay_1_Load', 'Forestay_Load_J1'),
    ('VarFilter_WTP_Forestay_2_Load', 'Forestay_Load_J2'),
    ('VarFilter_WTP_MastRot', 'Mast_Rotation_Angle'),
    ('VarFilter_WTP_CBoard_Elevator_angle', 'Board_Elevator_Angle_Center'),
    ('VarFilter_WTP_CBoard_Trimmer_angle_norm', 'Board_Trimmer_Angle_Center'),
    ('VarFilter_WTP_Cboard_Extension', 'Board_Extension_Center'),
    ('VarFilter_WTP_Cboard_Load', 'Board_Load_Center'),
    ('VarFilter_WTP_Foil_Prt_Extension', 'Board_Extension_Port'),
    ('VarFilter_WTP_Foil_Prt_Rake', 'Board_Rake_Port'),
    ('VarFilter_WTP_Foil_Stb_Extension', 'Board_Extension_Starboard'),
    ('VarFilter_WTP_Foil_Stb_Rake', 'Board_Rake_Starboard'),
    ('VarFilter_WTP_Rudder_Angle_CC', 'Rudder_Angle_Center'),
    ('VarFilter_WTP_Rudder_CC_Elevator_angle', 'Rudder_Elevator_Angle_Center'),
    ('VarFilter_WTP_Rudder_Angle_Prt', 'Rudder_Angle_Port'),
    ('VarFilter_WTP_Rudder_Prt_Elevator_angle', 'Rudder_Elevator_Angle_Port'),
    ('VarFilter_WTP_Rudder_Prt_Load_I', 'Rudder_Inside_Load_Port'),
    ('VarFilter_WTP_Rudder_Prt_Load_O', 'Rudder_Outside_Load_Port'),
    ('VarFilter_WTP_Rudder_Angle_Stb', 'Rudder_Angle_Starboard'),
    ('VarFilter_WTP_Rudder_Stb_Elevator_angle', 'Rudder_Elevator_Angle_Starboard'),
    ('VarFilter_WTP_Rudder_Stb_Load_I', 'Rudder_Inside_Load_Starboard'),
    ('VarFilter_WTP_Rudder_Stb_Load_O', 'Rudder_Outside_Load_Starboard'),
    ('VarFilter_WTP_Shroud_Prt_Load', 'Shroud_Load_Port'),
    ('VarFilter_WTP_Shroud_Stb_Load', 'Shroud_Load_Starboard')
]
wind_features = [
    ('VarFilter_WTP_TW_angle', 'Wind_Angle'),
    ('VarFilter_WTP_TW_speed', 'Wind_Speed')
]
boat_speed_feature = ('VarFilter_WTP_SelBoatSpd', 'Boat_Speed')
bins_axis_names = ['Wind Angle (˚)', 'Wind Speed (knots)']
boxplot_axis_name = 'Boat Speed (knots)'
coc_feature_name = 'Feature'

# Regular expressions.
feature_regex = r'.*{}.*'
bin_dimensions_regex = r'[+-]?\d+'

# Other features.
statistics_features = ['Feature', 'Corr']
