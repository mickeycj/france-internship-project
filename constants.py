# List of relevant features and axis names.
identifier_features = [
    ('Date', 'Date'),
    ('Hour', 'Hour'),
    ('VarFilter_WTP_GPS1_lat', 'Latitude'),
    ('VarFilter_WTP_GPS1_long', 'Longitude')
]
fiber_optics_structure_features = [
    ('1s_FBM_P_TEMP', 'Front_Beam_Temp_Port'),
    ('1s_FBM_P_TEMP_To', 'Front_Beam_Temp_To_Port'),
    ('1s_FBM_P_To', 'Front_Beam_To_Port'),
    ('1s_FBM_P_laft', 'Front_Beam_Lower_Aft_Rake_Port'),
    ('1s_FBM_P_laft', 'Front_Beam_Lower_Forward_Rake_Port'),
    ('1s_FBM_P_uaft', 'Front_Beam_Upper_Aft_Rake_Port'),
    ('1s_FBM_P_uaft', 'Front_Beam_Upper_Forward_Rake_Port'),
    ('1s_FBM_S_TEMP', 'Front_Beam_Temp_Starboard'),
    ('1s_FBM_S_TEMP_To', 'Front_Beam_Temp_To_Starboard'),
    ('1s_FBM_S_To', 'Front_Beam_To_Starboard'),
    ('1s_FBM_S_laft', 'Front_Beam_Lower_Aft_Rake_Starboard'),
    ('1s_FBM_S_laft', 'Front_Beam_Lower_Forward_Rake_Starboard'),
    ('1s_FBM_S_uaft', 'Front_Beam_Upper_Aft_Rake_Starboard'),
    ('1s_FBM_S_uaft', 'Front_Beam_Upper_Forward_Rake_Starboard'),
    ('1s_HUL_C_TEMP', 'Hull_Temp_Center'),
    ('1s_HUL_C_TEMP_To', 'Hull_Temp_To_Center'),
    ('1s_HUL_C_To', 'Hull_To_Center'),
    ('1s_HUL_C_lport', 'Hull_Lower_Port_Center'),
    ('1s_HUL_C_lstbd', 'Hull_Lower_Starboard_Center'),
    ('1s_HUL_C_uport', 'Hull_Upper_Port_Center'),
    ('1s_HUL_C_ustbd', 'Hull_Upper_Starboard_Center'),
    ('1s_HUL_P_TEMP', 'Hull_Temp_Port'),
    ('1s_HUL_P_TEMP_To', 'Hull_Temp_To_Port'),
    ('1s_HUL_P_To', 'Hull_To_Port'),
    ('1s_HUL_P_lport', 'Hull_Lower_Port_Port'),
    ('1s_HUL_P_lstbd', 'Hull_Lower_Starboard_Port'),
    ('1s_HUL_P_uport', 'Hull_Upper_Port_Port'),
    ('1s_HUL_P_ustbd', 'Hull_Upper_Starboard_Port'),
    ('1s_HUL_S_TEMP', 'Hull_Temp_Starboard'),
    ('1s_HUL_S_TEMP_To', 'Hull_Temp_To_Starboard'),
    ('1s_HUL_S_To', 'Hull_To_Starboard'),
    ('1s_HUL_S_lport', 'Hull_Lower_Port_Starboard'),
    ('1s_HUL_S_lstbd', 'Hull_Lower_Starboard_Starboard'),
    ('1s_HUL_S_uport', 'Hull_Upper_Port_Starboard'),
    ('1s_HUL_S_ustbd', 'Hull_Upper_Starboard_Starboard')
]
fiber_optics_appendix_features = [
    ('1s_Foil_B_P_1_TEMP', 'Board_Temp_Port'),
    ('1s_Foil_B_P_1_TEMP_To', 'Board_Temp_To_Port'),
    ('1s_Foil_B_P_1_To', 'Board_To_Port'),
    ('1s_Foil_B_P_1_i', 'Board_Deformation_Inside_Port'),
    ('1s_Foil_B_P_1_o', 'Board_Deformation_Outside_Port'),
    ('1s_Foil_B_S_1_TEMP', 'Board_Temp_Starboard'),
    ('1s_Foil_B_S_1_TEMP_To', 'Board_Temp_To_Starboard'),
    ('1s_Foil_B_S_1_To', 'Board_To_Starboard'),
    ('1s_Foil_B_S_1_i', 'Board_Deformation_Inside_Starboard'),
    ('1s_Foil_B_S_1_o', 'Board_Deformation_Outside_Starboard'),
    ('1s_Foil_RUD_C_1_TEMP', 'Board_Temp_Center'),
    ('1s_Foil_RUD_C_1_TEMP_To', 'Board_Temp_To_Center'),
    ('1s_Foil_RUD_C_To', 'Board_To_Center'),
    ('1s_Foil_RUD_C_1_e_0_P', 'Rudder_Port_Center'),
    ('1s_Foil_RUD_C_1_e_0_S', 'Rudder_Starboard_Center')
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

# Regular expressions.
feature_regex = r'.*{}.*'
bin_dimensions_regex = r'[+-]?\d+'
