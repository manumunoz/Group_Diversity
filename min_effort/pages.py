from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
from collections import OrderedDict
import json


class BeforeEffortWP(WaitPage):
    wait_for_all_groups = True


class Effort(Page):
    form_model = 'player'
    form_fields = ['effort']


class BeforeNextRoundWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_effort()
        self.group.set_min_effort()
        self.group.round_gains()


class PostEffort(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.var_between_apps()


page_sequence = [
    BeforeEffortWP,
    Effort,
    BeforeNextRoundWP,
    PostEffort
]
