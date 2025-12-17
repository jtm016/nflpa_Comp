import nfl_data_py as nfl 
import pandas as pd

years_pulled = [2024]

# Step 1: Import the weekly data which includes the calculated 'snaps' column
weekly_stats_df = nfl.import_weekly_data(years_pulled)

print(weekly_stats_df.columns)



# # Step 2: Select the columns needed for ACWR calculation
# acwr_ready_df = weekly_stats_df[[
#     'player_id', 
#     'player_display_name', 
#     'week', 
#     'position', 
#     'snaps'
# ]].copy() # Use .copy() to avoid SettingWithCopyWarning

# print("Data ready for ACWR calculation. Head of DataFrame:")
# print(acwr_ready_df.head())