from ff_ruleset import Ruleset, Rule

class FleaFlickerRuleset(Ruleset):
    def __init__(self, debug=False):
        super().__init__(debug)
        # passing rules
        self.add_rule(self.offensive_players, 0.04, 'passing_yds', rule_name="Passing Yards")
        self.add_rule(self.offensive_players, 4, 'passing_tds', rule_name="Passing TDs")
        self.add_rule(self.offensive_players, 2, 'passing_twoptm', rule_name="Passing 2pt Made")
        self.add_rule(self.offensive_players, -2, 'passing_ints', rule_name="Passing INTs")

        # rushing rules
        self.add_rule(self.offensive_players, 0.1, 'rushing_yds', rule_name="Rushing Yards")
        self.add_rule(self.offensive_players, 2, 'rushing_twoptm', rule_name="Rushing 2pt Made")
        self.add_rule(self.offensive_players, 6, 'rushing_tds', rule_name="Rushing TDs")

        # receiving rules
        self.add_rule(self.offensive_players, 0.5, 'receiving_rec', rule_name="Receiving Receptions")
        self.add_rule(self.offensive_players, 0.1, 'receiving_yds', rule_name="Receiving Yards")
        self.add_rule(self.offensive_players, 2, 'receiving_twoptm', rule_name="Receiving 2pt Made")
        self.add_rule(self.offensive_players, 6, 'receiving_tds', rule_name="Receiving TDs")

        # Misc
        self.add_rule(self.offensive_players, -2, 'fumbles_lost', rule_name="Fumble Lost")
        self.add_rule(self.offensive_players, 6, 'fumbles_rec_tds', rule_name="Offensive Fumble Recovery TDs")

        # kicking rules
        self.add_rule(self.offensive_players, 3, 'kicking_fgm', rule_name="Field Goal Made")

        def eval_extra_yardage_kicking_rule(player_stats):
            if ('kicking_fgm' in player_stats.__dict__) and ('kicking_fgm_yds' in player_stats.__dict__):
                num_kicks = player_stats.__dict__['kicking_fgm']
                extra_yards = player_stats.__dict__['kicking_fgm_yds'] - (num_kicks * 30)
                return extra_yards * 0.1
            else:
                return 0

        self.add_rule(self.offensive_players, 0, '', 
                      rule_name="Extra Yards for Field Goal Over 30 Yards", 
                      alt_eval_function=eval_extra_yardage_kicking_rule)

        self.add_rule(self.offensive_players, -1, 'kicking_fgmissed', rule_name="Field Goal Missed")
        self.add_rule(self.offensive_players, 1, 'kicking_xpmade', rule_name="XP Made")
        self.add_rule(self.offensive_players, -1, 'kicking_xpmissed', rule_name="XP Missed")
        
        # Returning rules
        self.add_rule(self.all_players, 6, 'kickret_tds', rule_name="Kick Return TDs")
        self.add_rule(self.all_players, 6, 'puntret_tds', rule_name="Punt Return TDs")

        # Defensive rules
        """
        self.add_rule(self.all_players, 2, 'defense_int')
        self.add_rule(self.all_players, 1, 'defense_sk')
        self.add_rule(self.all_players, 1, 'defense_ffum')
        self.add_rule(d_sp_players, 1, 'defense_frec')
        self.add_rule(self.all_players, 2, 'defense_safe')
        self.add_rule(self.all_players, 6, 'defense_tds')
        self.add_rule(self.all_players, 2, 'defense_xpblk')
        self.add_rule(self.all_players, 2, 'defense_fgblk')
        self.add_rule(self.all_players, 2, 'defense_puntblk')
        """
