# NBA More Minutes

## Which NBA players deserve more playing time?

This project analyzes 2022–2023 NBA player statistics to identify players who produced strong statistical results while receiving relatively limited playing time.

The goal is not to determine who should receive more minutes with absolute certainty. Instead, this analysis explores whether statistical production can be used to identify potential candidates for increased playing time.

Playing time in the NBA is influenced by many factors that traditional box-score statistics cannot fully capture. Coaching decisions, team needs, player roles, defensive assignments, injuries, matchups, lineup combinations, experience, and many other factors can all influence how many minutes a player receives.

Because of this, the rankings produced by this project should be viewed as analytical indicators rather than definitive recommendations.

## Data Prep

The original dataset contains statistics for active NBA players during the 2022–2023 season.

Several preprocessing steps were performed before analyzing player performance:

- Removed statistics that were not needed for the analysis.
- Removed "TOT" team entries, which represent combined statistics for players who were traded during the season.
- Limited the dataset to players who appeared in at least 20 games to reduce the influence of small-sample outliers.

## Per Minute Metrics

Raw totals can be misleading when comparing players who receive different amounts of playing time.

For example, a player receiving 30 minutes per game will naturally have more opportunities to accumulate points, rebounds, and assists than a player receiving 10 minutes.

To make player production more comparable, several per-minute metrics were calculated:

- Points per minute
- Assists per minute
- Rebounds per minute
- Steals per minute
- Blocks per minute
- Turnovers per minute
- Personal fouls per minute
- Starting rate

A simple initial TOT_VALUE metric was also created by combining points, assists, and rebounds per minute.

data["PTS_PER_MIN"] = (data["PTS"] / data["MP"]).round(2)
data["AST_PER_MIN"] = (data["AST"] / data["MP"]).round(2)
data["REB_PER_MIN"] = (data["TRB"] / data["MP"]).round(2)

This initial ranking provided a useful starting point, but it also revealed a limitation: not all statistics contribute equally to a player's overall value.

## Building a Balanced Score

Simply adding points, assists, and rebounds gives more weight to players who score more frequently. However, scoring alone does not necessarily indicate that a player is more deserving of playing time.

A player can contribute in many different ways.

To create a more balanced comparison, the analysis incorporates:

Positive Metrics:
- Points per minute
- Assists per minute
- Rebounds per minute
- Steals per minute
- Blocks per minute
- Effective field goal percentage
- Negative Metrics
- Turnovers per minute
- Personal fouls per minute

Because these metrics operate on different scales, each metric was standardized using its mean and standard deviation.

The final BALANCED_SCORE rewards players for positive statistical production while penalizing turnovers and fouls.

## Minute Pools

Because players receiving different amounts of playing time have different opportunities to produce, the 5–20 minute range was divided into three groups:

Minute Pool	Minutes Per Game:
Lower Pool:	5–10
Middle Pool:	10–15
Upper Pool:	15–20

Players are ranked within each pool based on their BALANCED_SCORE.

This allows the analysis to ask a more specific question:
Which players are performing well relative to other players receiving a similar amount of playing time?

## Position Pools

It's natural for positional statistics to vary. For example, a guard is most likely going to score the ball more than a center. 
Because of this, players were compared to their positional peers in the following pools:

Guards: Point Guard, Shooting Guard
Forwards: Small Forward, Power Forward
Centers: Center

For positional analysis minute pools were abandoned. Additionally, only players averaging 5-15 Minutes per game were compared. I made this decision due to players with 15+ minutes dominating the upper results.

## Visuals

more_min_scatter.png: This scatter plot compares minutes per game with the initial total statistical value for players with 5-20 MPG
balanced_candidate png's: The analysis then produces rankings based on the standardized balanced score.
Seperate visuals are also generated for the minute pools and positional pools.

## Data Results

The analysis produces ranked CSV files containing the players identified as the strongest statistical candidates for additional playing time.
The rankings can be viewed at the overall 5–20 MPG level, within each individual minute pool, and within each positional pool.
The project intentionally focuses on identifying candidates rather than declaring definitive answers.

According to our analysis the following players averaging 5-15 MPG are candidates for elevated minutes:
- PG's: Jeff Dowtin, TyTy Washington, Kennedy Chandler
- SG's: Lindy Waters, Peyton Watson, Garrett Temple
- SF's: Matisse Thybulle, Javonte Green, Matt Ryan
- PF's: Derrick Jones, Davis Bertans, Juancho Hernangomez
- C's: Udoka Azubuike, Luke Kornet, Mike Muscala

## Real World Results

Because our dataset is in the past we can look at future stats to verify our analysis. Let's ask the question, "Did the players we identify actually get increased minutes in the following years?". 
Let's look at the 2023-2024 season data for the players we listed above. +- will be listed alongside player names. This will indicate the change in minutes from the 22-23 season to the 24-25 season.
Players will be grabbed in order of their ranking in positional dataset .csv files. Players who did not play during the 24-25 season are skipped, and the next player in line pulled up.

- PG's: Jeff Dowtin (+1.8), TyTy Washington (-8.9), Miles Mcbride (+7.6)
- SG's: Lindy Waters (-5.6), Peyton Watson (+10.5), Garrett Temple (+4.2)
- SF's: Matisse Thybulle (+15.6), Javonte Green (+10.6), Jalen Johnson (+18.8)
- PF's: Derrick Jones (+11.5), Davis Bertans (+11.9), Chimezie Metu (+19)
- C's: Udoka Azubuike (-2.9), Luke Kornet (+3.9), Mike Muscala (+7.5)

WOAH! I did not expect our analysis to hold up so well in the real world. Look at all those players who got the minutes they deserved in the following year! 
Albeit, some of these players switched teams the following year and received an eleveated role. However, that does not dismiss the validity of our analysis!
Different teams were willing to give these players more minutes based on their efficiency on the court with restrained minutes.
  
## Tech used:
- Python
- Pandas
- NumPy
- Matplotlib
- .CSV



































