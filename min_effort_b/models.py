from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'min_effort_b'
    players_per_group = 4
    num_rounds = 1
    gain = 20
    cost = 10
    fix = 50
    # names = ['A','B','C','D',]
    # highpay = c(3)
    # lowpay = c(1)
    # nopay = c(0)
    # Treatment & Group parameters
    part_pre_min = 1
    part_coord = 2
    part_post_min = 3
    #------------------------------------------

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    min_effort = models.IntegerField()
    old_min_effort = models.IntegerField()

    def set_effort(self):
        for player in self.get_players():
            player.effort_a = self.get_player_by_role('1').effort
            player.effort_b = self.get_player_by_role('2').effort
            player.effort_c = self.get_player_by_role('3').effort
            player.effort_d = self.get_player_by_role('4').effort

    def set_min_effort(self):
        players = self.get_players()
        efforts = sorted([p.effort for p in players])
        self.min_effort = efforts[0]

    def round_gains(self):
        for player in self.get_players():
            player.round_gains = (Constants.gain * self.min_effort) - (Constants.cost * player.effort) + Constants.fix
            player.payoff = player.round_gains


class Player(BasePlayer):
    effort_a = models.IntegerField()
    effort_b = models.IntegerField()
    effort_c = models.IntegerField()
    effort_d = models.IntegerField()
    old_effort_a = models.IntegerField()
    old_effort_b = models.IntegerField()
    old_effort_c = models.IntegerField()
    old_effort_d = models.IntegerField()

    effort = models.IntegerField(
        choices=[
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'A'],
            [6, 'B'],
            [7, 'C']
        ]
    )

    old_effort = models.IntegerField()
    round_gains = models.IntegerField()
    old_round_gains = models.IntegerField()

    def role(self):
        return {1: '1', 2: '2', 3: '3', 4: '4'}[self.id_in_group]

    def var_between_apps(self):
        self.participant.vars['effort_a_2'] = self.effort_a
        self.participant.vars['effort_b_2'] = self.effort_b
        self.participant.vars['effort_c_2'] = self.effort_c
        self.participant.vars['effort_d_2'] = self.effort_d
        self.participant.vars['effort_2'] = self.effort
        self.participant.vars['min_effort_2'] = self.group.min_effort
        self.participant.vars['effort_points_2'] = self.round_gains