from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
from collections import OrderedDict
import json
import itertools

class ResultsWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.new_vars()

class Results_es(Page):
    pass
    # def before_next_page(self):
    #     self.player.var_between_apps()


page_sequence = [
    ResultsWP,
    Results_es
]
