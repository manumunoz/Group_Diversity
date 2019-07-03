from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Manu Munoz'

doc = """
Group Spillovers: Pay
"""


class Constants(BaseConstants):
    #------------------------------------------
    name_in_url = 'pay'
    names = ['1', '2', '3', '4']
    players_per_group = len(names)
    periods = 1
    num_rounds = periods
    #------------------------------------------
    # PAYOFFS
    highpay = 3
    lowpay = 1
    nopay = 0
    show_up = 5
    total_group_pay = 800 # Value in dollars for total group earnings
    total_group_no_pay = 0
    #==================================
    # CHOSEN ROUNDS
    chosen_num_rounds = 12
    goal_value = 8
    pay_rounds = [1,2,4,6,7,8,9,12,13,14,15,17]
    #==================================
    # Treatment & Group parameters
    others = len(names) - 1
    part_pre_min = 1
    part_coord = 2
    part_post_min = 3
    part_alloc = 4
    #------------------------------------------
    # Payoffs
    exp_currency = "experimental dollars"
    currency = "pesos"
    currency_exchange = 80
    points_exchange = 1
    min_pay = 10000
    min_points = 10
    currency_min_pay = c(10000)
    #------------------------------------------


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def round_payoffs(self):
        for player in self.get_players():
            #======================================
            player.first_effort_a = player.participant.vars['effort_a']
            player.first_effort_b = player.participant.vars['effort_b']
            player.first_effort_c = player.participant.vars['effort_c']
            player.first_effort_d = player.participant.vars['effort_d']
            player.first_effort = player.participant.vars['effort']
            player.first_min_effort = player.participant.vars['min_effort']
            player.first_my_points = player.participant.vars['effort_points']
            #======================================
            player.win_one = player.participant.vars['win_one']
            player.win_two = player.participant.vars['win_two']
            player.win_three = player.participant.vars['win_three']
            player.win_four = player.participant.vars['win_four']
            player.group_points = player.participant.vars['group_points']
            player.my_points = player.participant.vars['points']
            player.coordination = player.participant.vars['coordinations']
            player.coord_points = player.participant.vars['coord_point']
            #======================================
            player.second_effort_a = player.participant.vars['effort_a_2']
            player.second_effort_b = player.participant.vars['effort_b_2']
            player.second_effort_c = player.participant.vars['effort_c_2']
            player.second_effort_d = player.participant.vars['effort_d_2']
            player.second_effort = player.participant.vars['effort_2']
            player.second_min_effort = player.participant.vars['min_effort_2']
            player.second_my_points = player.participant.vars['effort_points_2']
            # ======================================
            player.chosen_pair = player.participant.vars['chosen_pair']
            player.chosen_role = player.participant.vars['chosen_role']
            player.alloc_points = player.participant.vars['part_alloc_payoff']
            # ======================================
            player.total_points = player.first_my_points + player.coord_points + player.second_my_points + player.alloc_points
            # ======================================

    def payoff_value(self):
        for player in self.get_players():
            player.payoff = player.total_points

class Player(BasePlayer):
    first_effort_a = models.IntegerField()
    first_effort_b = models.IntegerField()
    first_effort_c = models.IntegerField()
    first_effort_d = models.IntegerField()
    first_effort = models.IntegerField()
    first_min_effort = models.IntegerField()
    first_my_points = models.IntegerField()
    #======================================
    win_one = models.IntegerField()
    win_two = models.IntegerField()
    win_three = models.IntegerField()
    win_four = models.IntegerField()
    group_points = models.IntegerField()
    my_points = models.IntegerField()
    coordination = models.IntegerField()
    coord_points = models.FloatField()
    #======================================
    second_effort_a = models.IntegerField()
    second_effort_b = models.IntegerField()
    second_effort_c = models.IntegerField()
    second_effort_d = models.IntegerField()
    second_effort = models.IntegerField()
    second_min_effort = models.IntegerField()
    second_my_points = models.IntegerField()
    #======================================
    chosen_pair = models.IntegerField()
    chosen_role = models.IntegerField()
    alloc_points = models.IntegerField()
    #======================================
    total_points = models.CurrencyField()
    payoff = models.FloatField()
    #======================================
