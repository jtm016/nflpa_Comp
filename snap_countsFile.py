import nfl_data_py as nfl
import pandas as pd

snap_counts_df = pd.read_csv("snap_counts.csv") 

# 1. Data Cleaning and Preparation 

# Create the Total Snaps Column
snap_counts_df['total_snaps'] = (
    snap_counts_df['offense_snaps'].fillna(0) + 
    snap_counts_df['defense_snaps'].fillna(0) + 
    snap_counts_df['st_snaps'].fillna(0)
)

# Rename the PFR ID to a standard 'player_id'
snap_counts_df.rename(columns={'pfr_player_id': 'player_id'}, inplace=True)

acwr_ready_df = snap_counts_df[['player_id', 'player', 'week', 'position', 'total_snaps']].copy() 

# 2. Calculate the ACWR 

acwr_ready_df = acwr_ready_df.sort_values(by=['player_id', 'week'])

# Chronic Load (Rolling 4-week mean of total_snaps, lagged by 1 week)
acwr_ready_df['chronic_load'] = acwr_ready_df.groupby('player_id')['total_snaps'].transform(
    lambda x: x.shift(1).rolling(window=4, min_periods=1).mean()
)
#Calculate Acute Load (lagged by a week, for week 5, look at week 4 and below. )
acwr_ready_df['acute_load'] = acwr_ready_df.groupby('player_id')['total_snaps'].shift(1)

# ACWR: Acute Load / Chronic Load
acwr_ready_df['ACWR'] = acwr_ready_df['acute_load'] / acwr_ready_df['chronic_load']

print("ACWR Calculation Complete. Ready to merge with Injury Data.")
print(acwr_ready_df[['player', 'week', 'total_snaps', 'chronic_load', 'ACWR']].tail(5))

# 3. Assign Risk Levels using pd.cut
risk_bins_awcr = [-float('inf'), 0.8, 1.3, 1.5, float('inf')]
risk_labels = ['Under-trained','Perfect','High Workload', 'Danger Zone']
acwr_ready_df['risk_level'] = pd.cut(acwr_ready_df['ACWR'], bins = risk_bins_awcr, labels = risk_labels)


# 4. Generate and Sort the Weekly Risk Summary (The Fix)
# Group by week and risk level, count the players in each, and unstack to pivot the risk levels into columns.
weekly_risk_summary = acwr_ready_df.groupby(['week', 'risk_level'], observed=False).size().unstack(fill_value=0)

# Sort the summary by the 'Danger Zone' count in descending order
weekly_risk_summary_sorted = weekly_risk_summary.sort_values(by='Danger Zone', ascending=False)

print("\nWeekly Risk Level Distribution Sorted by Danger Zone:")
print(weekly_risk_summary_sorted)

acwr_ready_df.to_csv("nfl_player_workload_acwr.csv", index=False)
weekly_risk_summary_sorted.to_csv("weekly_risk_summary.csv")

print("\nthis is a successful run")