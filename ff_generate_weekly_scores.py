# turn the weekly scores from 2014 - 2017 into csvs per player
import nflgame as nfl
from ff_score import FleaFlickerRuleset
from collections import defaultdict

import pandas as pd

def generate_fleaflicker_scores(year=2017):
    f = FleaFlickerRuleset()
    score_df = pd.DataFrame()

    for i in range(1, 18, 1):
        print("Week {}".format(i))
        games = nfl.games(year, week=i)
        players = nfl.combine(games)
        player_scores = dict()
        for player in players:
            player_scores["{}_{}".format(player.playerid, player.name)] = f.eval_player(player)
        score_df["WEEK_{}".format(i)] = pd.Series(player_scores)

    score_df.fillna(0, inplace=True)
    score_df["SUM"] = score_df.sum(axis=1)
    score_df.sort_values("SUM", ascending=False, inplace=True)
    score_df.to_csv("YEAR_{}.csv".format(year))

        
for y in range(2014, 2018, 1):
    generate_fleaflicker_scores(y)
