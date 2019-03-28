from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json

author = 'Manu Munoz'

doc = """
Identity Switch - ALLOCATION
"""


class Constants(BaseConstants):
    #------------------------------------------
    name_in_url = 'allocation'
    names = ['1', '2', '3', '4']
    players_per_group = len(names)
    num_rounds = 1
    # instructions_template = 'group_spillover/Instructions.html'
    #==================================
    # PAYOFFS
    gain = 2
    cost = 1
    fix = 60
    #==================================
    # Treatment & Group parameters
    part_pre_min = 1
    part_coord = 2
    part_post_min = 3
    part_alloc = 4
    exp_currency = "experimental dollars"
    #------------------------------------------
    # Dictator
    pie = 10
    #------------------------------------------



class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.given_type = int(Constants.attribute[p.id_in_group - 1])

        if self.round_number == 1:
            chosen_player = random.randint(1, Constants.players)
            self.session.vars['chosen_player'] = chosen_player


class Group(BaseGroup):
    chosen_player = models.IntegerField()

    def chosen_allocation(self):
        self.chosen_player = self.session.vars['chosen_player']

    def set_allocations(self):
        if self.session.vars['chosen_player'] == 1:
            self.get_player_by_id(3).alloc_received = self.get_player_by_id(1).alloc
            self.get_player_by_id(2).alloc_received = Constants.pie - self.get_player_by_id(1).alloc
        elif self.session.vars['chosen_player'] == 2:
            self.get_player_by_id(3).alloc_received = self.get_player_by_id(2).alloc
            self.get_player_by_id(4).alloc_received = Constants.pie - self.get_player_by_id(2).alloc
        elif self.session.vars['chosen_player'] == 3:
            self.get_player_by_id(5).alloc_received = self.get_player_by_id(3).alloc
            self.get_player_by_id(4).alloc_received = Constants.pie - self.get_player_by_id(3).alloc
        elif self.session.vars['chosen_player'] == 4:
            self.get_player_by_id(5).alloc_received = self.get_player_by_id(4).alloc
            self.get_player_by_id(7).alloc_received = Constants.pie - self.get_player_by_id(4).alloc
        elif self.session.vars['chosen_player'] == 5:
            self.get_player_by_id(6).alloc_received = self.get_player_by_id(5).alloc
            self.get_player_by_id(7).alloc_received = Constants.pie - self.get_player_by_id(5).alloc
        elif self.session.vars['chosen_player'] == 6:
            self.get_player_by_id(1).alloc_received = self.get_player_by_id(6).alloc
            self.get_player_by_id(2).alloc_received = Constants.pie - self.get_player_by_id(6).alloc
        else:
            self.get_player_by_id(6).alloc_received = self.get_player_by_id(7).alloc
            self.get_player_by_id(2).alloc_received = Constants.pie - self.get_player_by_id(7).alloc

    def round_payoffs(self):
        for player in self.get_players():
            player.points_alloc = player.alloc_received
            player.payoff = player.points_alloc
            # player.total_points = {{ Constants.currency_exchange}} * (player.participant.vars['part_fixed_payoff'] + player.participant.vars['part_fluid_payoff'] + player.participant.vars['part_alloc_payoff'])

    # def total_payoff(self):
    #     for player in self.get_players():
    #         if player.participant.payoff >= Constants.min_pay_pesos:
    #             player.participant.payoff = player.participant.payoff
    #         else:
    #             player.participant.payoff = Constants.min_pay_pesos


class Player(BasePlayer):
    given_type = models.IntegerField() # combination of symbol and preference
    alloc_received = models.IntegerField(initial=0)
    points_alloc = models.IntegerField()
    gender = models.IntegerField()

    alloc = models.PositiveIntegerField(
        choices=[0,1,2,3,4,5,6,7,8,9,10]
    )

    def vars_for_template(self):
        return {
            'circles_name': self.participant.vars['circles_name'],
            'triangles_name': self.participant.vars['triangles_name'],
            'circles_label': self.participant.vars['circles_label'],
            'triangles_label': self.participant.vars['triangles_label'],
        }

    def var_between_apps(self):
        self.participant.vars['part_alloc_payoff'] = self.points_alloc
