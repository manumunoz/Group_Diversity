from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
from collections import OrderedDict
import json
import itertools


class StartWP(WaitPage):
    wait_for_all_groups = True


class Start(Page):
    pass


class BeforeSignalWP(WaitPage):
    def after_all_players_arrive(self):
        for player in self.group.get_players():
            if self.round_number > 1:
                player.old_action = player.in_round(self.round_number - 1).action
                player.old_points = player.in_round(self.round_number - 1).points
                player.old_total_points = player.in_round(self.round_number - 1).total_points
            else:
                player.old_action = 0
                player.old_points = 0
                player.old_total_points = 0

        self.group.displaying_network()
        if self.round_number > 1:
            self.group.old_coordination = self.group.in_round(self.round_number - 1).coordination
            self.group.old_total_coordination = self.group.in_round(self.round_number - 1).total_coordination
            self.group.old_goal_achieved = self.group.in_round(self.round_number - 1).goal_achieved
            self.group.old_win = self.group.in_round(self.round_number - 1).win
            self.group.old_total_win_one = self.group.in_round(self.round_number - 1).total_win_one
            self.group.old_total_win_two = self.group.in_round(self.round_number - 1).total_win_two
            self.group.old_total_win_three = self.group.in_round(self.round_number - 1).total_win_three
            self.group.old_total_win_four = self.group.in_round(self.round_number - 1).total_win_four
            self.group.old_group_total_points = self.group.in_round(self.round_number - 1).group_total_points
        else:
            self.group.old_coordination = 0
            self.group.old_total_coordination = 0
            self.group.old_goal_achieved = 0
            self.group.old_group_total_points = 0
            self.group.old_win = 0
            self.group.old_total_win_one = 0
            self.group.old_total_win_two = 0
            self.group.old_total_win_three = 0
            self.group.old_total_win_four = 0


class FirstSignal(Page):
    form_model = 'player'
    form_fields = ['first']


class BeforeSecondSignalWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.displaying_network()


class SecondSignal(Page):
    form_model = 'player'
    form_fields = ['second']


class BeforeActionlWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.displaying_network()


class Action(Page):
    form_model = 'player'
    form_fields = ['action']

    def before_next_page(self):
        self.player.choice_value()

        group = self.group
        players = group.get_players()
        ones = [p.action_one for p in players]
        group.total_one = sum(ones)
        twos = [p.action_two for p in players]
        group.total_two = sum(twos)
        threes = [p.action_three for p in players]
        group.total_three = sum(threes)
        fours = [p.action_four for p in players]
        group.total_four = sum(fours)


class LastPageWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.displaying_network()
        self.group.determine_win()
        self.group.set_coordination()
        self.group.total_points()
        self.group.play_payment_rounds()
        self.group.grp_payment_rounds()
        self.group.total_values()
        self.group.goal_achievement()
        self.group.finalpay_value()
        # self.group.payoff_value()


class LastPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.var_between_apps()


page_sequence = [
    StartWP,
    Start,
    BeforeSignalWP,
    FirstSignal,
    BeforeSecondSignalWP,
    SecondSignal,
    BeforeActionlWP,
    Action,
    LastPageWaitPage,
    LastPage,
    ResultsWaitPage,
    Results
]
