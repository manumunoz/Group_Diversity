from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Manu Munoz-Herrera'

doc = """
Minimum Effort game, with a range between 1 and 60, gains of 2 and cost of 1, and a calculator.
"""


class Constants(BaseConstants):
    name_in_url = 'min_effort_2_es'
    names = ['1', '2', '3', '4']
    players_per_group = len(names)
    num_rounds = 1
    # instructions_template = 'group_spillover/Instructions.html'
    #==================================
    # PAYOFFS
    gain = 2
    cost = 1.5
    fix = 90
    attempts = 5
    #==================================
    # Treatment & Group parameters
    part_pre_min = 1
    part_coord = 2
    part_post_min = 3
    part_alloc = 4
    exp_currency = "dólares experimentales"
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
            # player.payoff = player.round_gains


class Player(BasePlayer):
    effort_a = models.IntegerField()
    effort_b = models.IntegerField()
    effort_c = models.IntegerField()
    effort_d = models.IntegerField()
    old_effort_a = models.IntegerField()
    old_effort_b = models.IntegerField()
    old_effort_c = models.IntegerField()
    old_effort_d = models.IntegerField()
    test_effort = models.IntegerField(min=1, max=60, blank=True)

    test_minimum = models.IntegerField(min=1, max=60, blank=True)

    effort = models.IntegerField(min=1, max=60)

    old_effort = models.IntegerField()
    round_gains = models.FloatField()
    old_round_gains = models.FloatField()


    q_samegroup = models.PositiveIntegerField(
        choices=[
            [1, 'Sí'],
            [2, 'No'],
        ],
        widget=widgets.RadioSelect
    )

    q_min = models.PositiveIntegerField(
        choices=[
            [1, '36'],
            [2, '25'],
            [3, '49'],
            [4, '19'],
        ],
        widget=widgets.RadioSelect
    )

    q_pay = models.PositiveIntegerField(
        choices=[
            [1, '90 – (1.5 x 25) + (2 x 19) = 90.5'],
            [2, '90 + (1.5 x 19) – (2 x 25) = 68.5'],
            [3, '90 + (1.5 x 25) – (2 x 19) = 89.5'],
            [4, '90 – (1.5 x 19) + (2 x 25) = 111.5'],
        ],
        widget=widgets.RadioSelect
    )

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