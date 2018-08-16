# turn the weekly scores from 2014 - 2017 into csvs per player
import nflgame as nfl
from ff_fleaflicker_ruleset import FleaFlickerRuleset
from ff_cbs_ruleset import CBSRuleset
from collections import defaultdict

import pandas as pd

def generate_fleaflicker_scores(year=2017):
    print("Generating FleaFlicker year {}".format(year))
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
    score_df.to_csv("FLEAFLICKER_YEAR_{}.csv".format(year))


def generate_cbs_scores(year=2017):
    print("Generating CBS year {}".format(year))
    c = CBSRuleset()
    score_df = pd.DataFrame()

    for i in range(1, 18, 1):
        print("Week {}".format(i))
        week = nfl.games(year, week=i)
        week_dict = c.eval_week(week)
        
        score_df["WEEK_{}".format(i)] = pd.Series(week_dict)

    score_df.fillna(0, inplace=True)
    score_df.to_csv("CBS_YEAR_{}.csv".format(year))
        
for y in range(2014, 2018, 1):
    generate_fleaflicker_scores(y)
    generate_cbs_scores(y)
