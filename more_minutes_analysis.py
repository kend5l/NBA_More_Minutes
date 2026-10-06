# 2022-2023 NBA Season Data (all active players)
# Question: Which players deserve more playing time?

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read in our csv file
data = pd.read_csv("nba_data_processed.csv")

# Drop columns we don't need for this analysis
drop_columns = ['Age', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB']
data.drop(drop_columns, axis='columns', inplace=True)

# Delete all player entries playing for the team "TOT". this is a total stat line for players traded mid season. we can do without this
data = data[data["Tm"] != "TOT"]

# For our analysis we want players with at least 20 Games Played. This will help clean up some outliers
data = data[data["G"] >= 20]

# Create Stats Per Minute Metrics
data["PTS_PER_MIN"] = (data["PTS"] / data["MP"]).round(2)
data["AST_PER_MIN"] = (data["AST"] / data["MP"]).round(2)
data["REB_PER_MIN"] = (data["TRB"] / data["MP"]).round(2)
# We will use the following metrics later on
data["STL_PER_MIN"] = (data["STL"] / data["MP"]).round(3)
data["BLK_PER_MIN"] = (data["BLK"] / data["MP"]).round(3)
data["TOV_PER_MIN"] = (data["TOV"] / data["MP"]).round(3)
data["PF_PER_MIN"] = (data["PF"] / data["MP"]).round(3)
data["START_RATE"] = (data["GS"] / data["G"]).round(2)

# Simple total value metric to determine how much statistical value a player brings per minute
data["TOT_VALUE"] = (data["PTS_PER_MIN"] + data["AST_PER_MIN"] + data["REB_PER_MIN"]).round(2)

# Let's sort by total value for players averaging 5-20 MPG (usually role players average 5-20 mpg)
more_min_data = data.sort_values("TOT_VALUE", ascending=False, inplace=False)
more_min_data = more_min_data[more_min_data["MP"].between(5, 20)]
more_min_data.to_csv("more_minutes_ranked.csv", index=False)

# Now we'll create a scatter plot for a visual
fig, ax = plt.subplots(figsize=(11,7))
points = ax.scatter(
    more_min_data["MP"],
    more_min_data["TOT_VALUE"],
    alpha=0.7,
)
# Label the top 10 players
for _, player in more_min_data.head(10).iterrows():
    ax.annotate(
        player["Player"],
        (player["MP"], player["TOT_VALUE"]),
        xytext=(-10,5),
        textcoords="offset points",
        fontsize=8,
    )
ax.set_title("Total Statistical Value vs. Minutes Played (MP 5-20)")
ax.set_xlabel("Minutes Per Game")
ax.set_ylabel("Total Statistical Value")
ax.grid(True, alpha=.3)
fig.tight_layout()
fig.savefig("more_min_scatter.png", dpi=150)

# Let's deepen our analysis. Stats in basketball are not the same, points weight heavily while steals and blocks weight less
# We want all stats to be equal in play. Currently if a player scores more then they're valued higher
# Any ball player will tell you this is not the truth. So Let's do some calculations to upgrade our analysis
# Additionally, we are not currently taking in other factors of play like fouls and turnovers
# Let's add some more metrics to our analysis to give us a better feel for if a player is really deserving of more minutes.

# Compare the 5-20 MPG candidates using standardized rates so percentages and per-minute stats
# contribute on the same scale. Turnovers and fouls count against the score.
candidate_data = data[data["MP"].between(5,20)].copy()

# Metrics we will reward the player for
positive_metrics = [
    "PTS_PER_MIN",
    "AST_PER_MIN",
    "REB_PER_MIN",
    "STL_PER_MIN",
    "BLK_PER_MIN",
    "eFG%",
]

# Metrics we will penalize the player for
negative_metrics = [
    "TOV_PER_MIN",
    "PF_PER_MIN",
]

score_metrics = positive_metrics + negative_metrics
candidate_metrics = candidate_data[score_metrics]

# Compute the standard deviation of each metric and standardize
metric_scales = candidate_metrics.std(ddof=0).replace(0, 1)
standardized_metrics = (candidate_metrics - candidate_metrics.mean()) / metric_scales

# Create a balanced score as positive metrics - negative metrics
candidate_data["BALANCED_SCORE"] = (
    standardized_metrics[positive_metrics].mean(axis=1)
    - standardized_metrics[negative_metrics].mean(axis=1)
).round(2)

# Sort our dataset by balanced_score and create .csv and bar graph for viewing
candidate_data = candidate_data.sort_values("BALANCED_SCORE", ascending=False)
candidate_data.to_csv("more_minutes_balanced_ranked.csv", index=False)

# Games played and starting rate add context
top_candidates = candidate_data.head(15)
fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(top_candidates["Player"], top_candidates["BALANCED_SCORE"])
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Balanced Candidate Score (5-20 MPG)")
ax.set_xlabel("Standardized production")
ax.set_ylabel("Player")
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig("more_minutes_balanced_candidates.png", dpi=150)

# Now, our dataset looks vastly different. This is due to our new metrics and standardization 
# It's likely that our top performers prior to our standardization were players who scored the ball more
# and like I stated previously, just because a player scores more doesn't mean they're "better" or more deserving of minutes

# Since 5-20 minutes is a broad range, and more minutes = more opportunities let's section off our players into minute pools. 
# This will help us determine if a player deserves to be elevated into a higher minute pool based on statistics
# Lower Pool: Players with 5-10 Minutes Per Game
# Mid Pool: Players with 10-15 Minutes Per Game
# Upper Pool: Players with 15-20 Minutes Per Game
# We're going to cap our analysis at 20 minutes per game 

lower_pool = candidate_data[(candidate_data["MP"] >= 5) & (candidate_data["MP"] < 10)].copy()
mid_pool = candidate_data[(candidate_data["MP"] >= 10) & (candidate_data["MP"] < 15)].copy()
upper_pool = candidate_data[(candidate_data["MP"] >= 15) & (candidate_data["MP"] <= 20)].copy()

# Sort our pools and create a .csv and bar graphs for viewing
lower_pool = lower_pool.sort_values("BALANCED_SCORE", ascending=False, inplace=False)
lower_pool.to_csv("lower_pool_ranked.csv", index=False)

mid_pool = mid_pool.sort_values("BALANCED_SCORE", ascending=False, inplace=False)
mid_pool.to_csv("middle_pool_ranked.csv", index=False)

upper_pool = upper_pool.sort_values("BALANCED_SCORE", ascending=False, inplace=False)
upper_pool.to_csv("upper_pool_ranked.csv", index=False)

# Lower Pool Graph
top_candidates = lower_pool.head(15)
fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(top_candidates["Player"], top_candidates["BALANCED_SCORE"])
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Balanced Candidate Score (Lower Pool, 5-10 MPG)")
ax.set_xlabel("Standardized production")
ax.set_ylabel("Player")
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig("lower_pool_balanced_candidates.png", dpi=150)

# Mid Pool Graph
top_candidates = mid_pool.head(15)
fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(top_candidates["Player"], top_candidates["BALANCED_SCORE"])
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Balanced Candidate Score (Middle Pool, 10-15 MPG)")
ax.set_xlabel("Standardized production")
ax.set_ylabel("Player")
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig("middle_pool_balanced_candidates.png", dpi=150)

# Lower Pool Graph
top_candidates = upper_pool.head(15)
fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(top_candidates["Player"], top_candidates["BALANCED_SCORE"])
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Balanced Candidate Score (Upper Pool, 15-20 MPG)")
ax.set_xlabel("Standardized production")
ax.set_ylabel("Player")
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig("upper_pool_balanced_candidates.png", dpi=150)

