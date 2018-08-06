# scores based on fantasy football rules
class Rule:
    def __init__(self, affected_positions, points, parameter, debug=None, rule_name=None, alt_eval_function=None):
        self.affected_positions = affected_positions
        self.points = points
        self.parameter = parameter
        self.alt_eval_function = alt_eval_function
        self.rule_name = rule_name
        self.debug = debug
    
    # nflgame player object
    def eval_player(self, player_stats):
        if player_stats.player is None:
            return 0
        if player_stats.player.position in self.affected_positions:
            if self.alt_eval_function is not None:
                scored = self.alt_eval_function(player_stats)
            else:
                if self.parameter in player_stats.__dict__:
                    scored = player_stats.__dict__[self.parameter] * self.points
                else:
                    scored = 0

            if self.debug:
                print("Evalauted rule{} for {} points".format(" " + self.rule_name, scored))
            return scored
        else:
            return 0

class FleaFlickerRuleset:
    def __init__(self, debug=False):
        self.debug = debug

        # create the rulesets
        self.rule_list = list()

        offensive_players = ['QB', 'RB', 'FB', 'WR', 'TE', 'K']

        d_sp_players = ['CB', 'DB', 'DE', 'DT', 'FS', 'ILB', 'LB', 'MLB', 'NT', 'OLB', 'SS', 'SAF']

        all_players = offensive_players + d_sp_players

        # passing rules
        self.rule_list.append(
            Rule(offensive_players, 0.04, 'passing_yds', rule_name="Passing Yards", debug=self.debug) 
        )

        self.rule_list.append(
            Rule(offensive_players, 4, 'passing_tds', rule_name="Passing TDs", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 2, 'passing_twoptm', rule_name="Passing 2pt Made", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, -2, 'passing_int', rule_name="Passing INTs", debug=self.debug)
        )

        # rushing rules
        self.rule_list.append(
            Rule(offensive_players, 0.1, 'rushing_yds', rule_name="Rushing Yards", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 2, 'rushing_twoptm', rule_name="Rushing 2pt Made", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 6, 'rushing_tds', rule_name="Rushing TDs", debug=self.debug)
        )

        # receiving rules
        self.rule_list.append(
            Rule(offensive_players, 0.5, 'receiving_rec', rule_name="Receiving Receptions", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 0.1, 'receiving_yds', rule_name="Receiving Yards", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 2, 'receiving_twoptm', rule_name="Receiving 2pt Made", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 6, 'receiving_tds', rule_name="Receiving TDs", debug=self.debug)
        )

        # Misc
        self.rule_list.append(
            Rule(offensive_players, -2, 'fumble_lost', rule_name="Fumble Lost", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 6, 'fumble_rec_tds', rule_name="Offensive Fumble Recovery TDs", debug=self.debug)
        )

        # kicking rules
        self.rule_list.append(
            Rule(offensive_players, 3, 'kicking_fgm', rule_name="Field Goal Made", debug=self.debug)
        )

        def eval_extra_yardage_kicking_rule(player_stats):
            if ('kicking_fgm' in player_stats.__dict__) and ('kicking_fgm_yds' in player_stats.__dict__):
                num_kicks = player_stats.__dict__['kicking_fgm']
                extra_yards = player_stats.__dict__['kicking_fgm_yds'] - (num_kicks * 30)
                return extra_yards * 0.1
            else:
                return 0

        self.rule_list.append(
            Rule(offensive_players, 0, '', rule_name="Extra Yards for Field Goal Over 30 Yards", 
                 debug=self.debug, alt_eval_function=eval_extra_yardage_kicking_rule)
        )

        self.rule_list.append(
            Rule(offensive_players, -1, 'kicking_fgmissed', rule_name="Field Goal Missed", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, 1, 'kicking_xpmade', rule_name="XP Made", debug=self.debug)
        )

        self.rule_list.append(
            Rule(offensive_players, -1, 'kicking_xpmissed', rule_name="XP Missed", debug=self.debug)
        )

        # Returning rules
        self.rule_list.append(
            Rule(all_players, 6, 'kickret_tds', rule_name="Kick Return TDs", debug=self.debug)
        )

        self.rule_list.append(
            Rule(all_players, 6, 'puntret_tds', rule_name="Punt Return TDs", debug=self.debug)
        )

        # Defensive rules
        """
        self.rule_list.append(
            Rule(all_players, 2, 'defense_int')
        )

        self.rule_list.append(
            Rule(all_players, 1, 'defense_sk')
        )

        self.rule_list.append(
            Rule(all_players, 1, 'defense_ffum')
        )

        self.rule_list.append(
            Rule(d_sp_players, 1, 'defense_frec')
        )

        self.rule_list.append(
            Rule(all_players, 2, 'defense_safe')
        )

        self.rule_list.append(
            Rule(all_players, 6, 'defense_tds')
        )

        self.rule_list.append(
            Rule(all_players, 2, 'defense_xpblk')
        )

        self.rule_list.append(
            Rule(all_players, 2, 'defense_fgblk')
        )

        self.rule_list.append(
            Rule(all_players, 2, 'defense_puntblk')
        )

        # forgetting the conversion return rule -- outlier anyways
        # self.rule_list.append(
        #    Rule(all_players, 2, )
        # )

        self.rule_list.append(
            
        )
        """

    def eval_player(self, player_stats):
        score = 0
        if self.debug:
            print(player_stats)
        for rule in self.rule_list:
            score += rule.eval_player(player_stats)

        return score

    def eval_team(self, team):
        score = 0
        ind_scores = []
        for player in team:
            if self.debug:
                print(player)
            ind_scores.append(self.eval_player(player))
        return sum(ind_scores), ind_scores


