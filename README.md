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

## Visuals

more_min_scatter.png: This scatter plot compares minutes per game with the initial total statistical value.
balanced_candidate png's: The analysis then produces rankings based on the standardized balanced score.
Seperate visuals are also generated for the minute pools

## Results

The analysis produces ranked CSV files containing the players identified as the strongest statistical candidates for additional playing time.
The rankings can be viewed at both the overall 5–20 MPG level and within each individual minute pool.
The project intentionally focuses on identifying candidates rather than declaring definitive answers.

## Tech used:
- Python
- Pandas
- NumPy
- Matplotlib
- .CSV



































