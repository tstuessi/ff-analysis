from ff_ruleset import Ruleset

from collections import defaultdict

import nflgame as nfl
from copy import copy

# CBS ruleset is a bit different. It needs to take into account
# the stats of the actual play, not just the overall metrics;
# therefore, it needs to work on a play by play basis, iterating
# over all the plays of the week and keeping track of the aggregates.
# Luckily, nflgame makes this relatively simple, as the API for 
# all of this is the same. There shouldn't be any additional changes
# to the underlying ruleset object; we will just overwrite the evaluation
# code to only evaluate weeks at a time.

# helper functions
def eval_rushing_yds(player_stats):
    if 'rushing_yds' in player_stats.__dict__:
        score = 0
        if player_stats.player.position == "RB" or player_stats.player.position == "WR":
            score = 0.5 * (player_stats.__dict__["rushing_yds"] // 10)
        if player_stats.player.position == "QB" or player_stats.player.position == "RB":
            if player_stats.__dict__["rushing_yds"] >= 100:
                score += 6
        return score
    else:
        return 0

def eval_field_goal(player_stats):
    if 'kicking_fgm_yds' in player_stats.__dict__ and 'kicking_fgm' in player_stats.__dict__:
        yds = player_stats.__dict__["kicking_fgm_yds"]
        fgm = player_stats.__dict__["kicking_fgm"]

        if fgm > 1:
            raise ValueError("Evaluate this on plays only (kicking_fgm > 1)")
        if yds >= 0 and yds < 40:
            return fgm * 3
        elif yds >= 40 and yds < 50:
            return fgm * 4
        else:
            return fgm * 6
    else:
        return 0

def eval_kick_return(player_stats):
    if 'kickret_yds' in player_stats.__dict__ and 'kickret_tds' in player_stats.__dict__:
        yds = player_stats.__dict__["kickret_yds"]
        tds = player_stats.__dict__["kickret_tds"]

        if tds > 1:
            raise ValueError("Evaluate this on plays only (kickret_tds > 1)")

        if yds < 10:
            return tds * 6
        elif yds < 40:
            return tds * 9
        elif yds < 80:
            return tds * 12
        else:
            return tds * 15

def eval_punt_return(player_stats):
    if 'puntret_yds' in player_stats.__dict__ and 'puntret_tds' in player_stats.__dict__:
        yds = player_stats.__dict__["puntret_yds"]
        tds = player_stats.__dict__["puntret_tds"]

        if tds > 1:
            raise ValueError("Evaluate this on plays only (puntret_tds > 1)")

        if yds < 10:
            return tds * 6
        elif yds < 40:
            return tds * 9
        elif yds < 80:
            return tds * 12
        else:
            return tds * 15

def eval_passing_tds(player_stats):
    score = 0
    if 'passing_yds' in player_stats.__dict__ and 'passing_tds' in player_stats.__dict__:
        yds = player_stats.__dict__["passing_yds"]
        tds = player_stats.__dict__["passing_tds"]

        if tds > 1:
            raise ValueError("Evaluate this on plays only (passing_tds > 1)")
        
        if yds < 10:
            score = 4 * tds
        elif yds < 40:
            score = 7 * tds
        elif yds < 80:
            score = 10 * tds
        else:
            score = 13 * tds

        if player_stats.player.position != 'QB':
            score *= 2
        
        return score
    else:
        return 0

def eval_passing_yds(player_stats):
    if 'passing_yds' in player_stats.__dict__:
        if player_stats.__dict__["passing_yds"] > 300:
            return 6
        else:
            return 0

def eval_receiving_tds(player_stats):
    score = 0
    if 'receiving_yds' in player_stats.__dict__ and 'receiving_tds' in player_stats.__dict__:
        yds = player_stats.__dict__["receiving_yds"]
        tds = player_stats.__dict__["receiving_tds"]

        if tds > 1:
            raise ValueError("Evaluate this on plays only (receiving_tds > 1)")

        if yds < 10:
            score = tds * 6
        elif yds < 40:
            score = tds * 9
        elif yds < 80:
            score = tds * 12
        else:
            score = tds * 15

        if player_stats.player.position != 'WR' and player_stats.player.position != 'TE':
            score *= 2

        return score
    else:
        return 0

def eval_receiving_yds(player_stats):
    if 'receiving_yds' in player_stats.__dict__:
        yds = player_stats.__dict__["receiving_yds"]
        score = 0.5 * (yds // 10)
        if yds >= 100:
            score += 6
        return score
    else:
        return 0

def eval_rushing_tds(player_stats):
    score = 0
    if 'rushing_yds' in player_stats.__dict__ and 'rushing_tds' in player_stats.__dict__:
        yds = player_stats.__dict__["rushing_yds"]
        tds = player_stats.__dict__["rushing_tds"]

        if tds > 1:
            raise ValueError("Evaluate this on plays only (rushing_tds > 1)")

        if yds < 10:
            score = tds * 6
        elif yds < 40:
            score = tds * 9
        elif yds < 80:
            score = tds * 12
        else:
            score = tds * 15

        if player_stats.player.position != 'RB':
            score *= 2

        return score
    else:
        return 0


class CBSRuleset(Ruleset):
    def __init__(self, debug=False):
        super().__init__(debug=debug)

        self.non_play_rules = list()

        # field goals


        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Field Goals Made",
                        alt_eval_function=eval_field_goal)
        
        self.add_rule(self.offensive_players, 1, 'kicking_xpmade', rule_name="XP Made")

        # two point conversion rules
        self.add_rule(self.offensive_players, 2, 'rushing_2ptm', rule_name="Rushing 2pt made")
        self.add_rule(self.offensive_players, 2, 'passing_2ptm', rule_name="Passing 2pt made")
        self.add_rule(self.offensive_players, 2, 'receiving_2ptm', rule_name="Receiving 2pt made")

        # kick/punt return rules

        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Kick Return TD",
                        alt_eval_function=eval_kick_return)


        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Punt Return TD",
                        alt_eval_function=eval_punt_return)

        # passing rules


        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Passing TDs",
                        alt_eval_function=eval_passing_tds)


        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Passing yds bonus",
                        alt_eval_function=eval_passing_yds,
                        alt_rule_list=self.non_play_rules)

        # receiving rules

        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Receiving TDs",
                        alt_eval_function=eval_receiving_tds)


        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Receiving yds",
                        alt_eval_function=eval_receiving_yds,
                        alt_rule_list=self.non_play_rules)

        # rushing rules
    
        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Rushing tds",
                        alt_eval_function=eval_rushing_tds)


        self.add_rule(self.offensive_players, 0, '',
                        rule_name="Rushing yds",
                        alt_eval_function=eval_rushing_yds,
                        alt_rule_list=self.non_play_rules)
    
    def eval_game(self, game):
        master_player_scores_dict = defaultdict(float)
        combined_games = nfl.combine([game])
        for drive in game.drives:
            for play in drive.plays:
                for player in play.players:
                    if player.player is not None:
                        scored = self.eval_player(player)
                        master_player_scores_dict["{}_{}".format(player.player.playerid, player.player.name)] += scored
        
        for player_stats in combined_games:
            scored = self.eval_player(player_stats, alt_rule_list=self.non_play_rules)
            master_player_scores_dict["{}_{}".format(player_stats.player.playerid, player_stats.player.name)] += scored
        return master_player_scores_dict

    def eval_week(self, week):
        score_dict = {}
        for game in week:
            score_dict = {**score_dict, **self.eval_game(game)}
        return score_dict

