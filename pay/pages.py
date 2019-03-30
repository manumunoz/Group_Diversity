from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class RandomPayWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.round_payoffs()
        self.group.payoff_value()


class RandomPay(Page):
    pass


page_sequence = [
    RandomPayWP,
    RandomPay,
]
