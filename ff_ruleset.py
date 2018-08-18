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
        scored = 0
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

            if scored is None:
                scored = 0

            if self.debug:
                print("Evalauted rule{} for {} points".format(" " + self.rule_name, scored))
            return scored
        else:
            return 0

class Ruleset:
    @staticmethod
    def offensive_players():
        return ['QB', 'RB', 'FB', 'WR', 'TE', 'K']
    @staticmethod
    def defensive_players():
        return ['CB', 'DB', 'DE', 'DT', 'FS', 'ILB', 'LB', 'MLB', 'NT', 'OLB', 'SS', 'SAF']
    def __init__(self, debug=False):
        self.debug = debug

        # create the rulesets
        self.rule_list = list()
        self.offensive_players = ['QB', 'RB', 'FB', 'WR', 'TE', 'K']
        self.d_sp_players = ['CB', 'DB', 'DE', 'DT', 'FS', 'ILB', 'LB', 'MLB', 'NT', 'OLB', 'SS', 'SAF']
        self.all_players = self.offensive_players + self.d_sp_players

    def add_rule(self, affected_positions, points, parameter, rule_name=None, alt_eval_function=None, alt_rule_list=None):
        if alt_rule_list is None:
            self.rule_list.append(
                Rule(affected_positions, points, parameter, debug=self.debug, 
                    rule_name=rule_name, alt_eval_function=alt_eval_function)
            )
        else:
            alt_rule_list.append(
                Rule(affected_positions, points, parameter, debug=self.debug, 
                    rule_name=rule_name, alt_eval_function=alt_eval_function)
            )

    def eval_player(self, player_stats, alt_rule_list=None):
        score = 0
        if alt_rule_list is None:
            tmp_rule_list = self.rule_list
        else:
            tmp_rule_list = alt_rule_list
        if self.debug:
            print(player_stats)
        for rule in tmp_rule_list:
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


