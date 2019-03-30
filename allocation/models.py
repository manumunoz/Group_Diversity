from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json

author = 'Manu Munoz'

doc = """
Allocation
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
    players = len(names)
    pie = 100
    #------------------------------------------


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
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
            self.get_player_by_id(1).alloc_received = Constants.pie - self.get_player_by_id(1).alloc
        elif self.session.vars['chosen_player'] == 2:
            self.get_player_by_id(4).alloc_received = self.get_player_by_id(2).alloc
            self.get_player_by_id(2).alloc_received = Constants.pie - self.get_player_by_id(2).alloc
        elif self.session.vars['chosen_player'] == 3:
            self.get_player_by_id(2).alloc_received = self.get_player_by_id(3).alloc
            self.get_player_by_id(3).alloc_received = Constants.pie - self.get_player_by_id(3).alloc
        else:
            self.get_player_by_id(1).alloc_received = self.get_player_by_id(4).alloc
            self.get_player_by_id(4).alloc_received = Constants.pie - self.get_player_by_id(4).alloc

    def set_pairs(self):
        if self.session.vars['chosen_player'] == 1:
            self.get_player_by_id(1).chosen_pair = 1
            self.get_player_by_id(3).chosen_pair = 1
            self.get_player_by_id(1).chosen_role = 1
        elif self.session.vars['chosen_player'] == 2:
            self.get_player_by_id(2).chosen_pair = 1
            self.get_player_by_id(4).chosen_pair = 1
            self.get_player_by_id(2).chosen_role = 1
        elif self.session.vars['chosen_player'] == 3:
            self.get_player_by_id(2).chosen_pair = 1
            self.get_player_by_id(3).chosen_pair = 1
            self.get_player_by_id(3).chosen_role = 1
        else:
            self.get_player_by_id(1).chosen_pair = 1
            self.get_player_by_id(4).chosen_pair = 1
            self.get_player_by_id(4).chosen_role = 1

    def round_payoffs(self):
        for player in self.get_players():
            player.points_alloc = player.alloc_received
            player.payoff = player.points_alloc


class Player(BasePlayer):
    alloc_received = models.IntegerField(initial=0)
    points_alloc = models.IntegerField()
    gender = models.IntegerField()
    age = models.IntegerField(min=18, max=100)
    chosen_pair = models.IntegerField(initial=0)
    chosen_role = models.IntegerField(initial=0)

    alloc = models.PositiveIntegerField(min=0, max=Constants.pie)

    def var_between_apps(self):
        self.participant.vars['part_alloc_payoff'] = self.points_alloc
        self.participant.vars['chosen_pair'] = self.chosen_pair
        self.participant.vars['chosen_role'] = self.chosen_role