from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class BeforeAllocationWP(WaitPage):
    wait_for_all_groups = True


class Allocation(Page):
    form_model = 'player'
    form_fields = ['alloc']


class AllocationWP(WaitPage):
    # wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.group.chosen_allocation()
        self.group.set_allocations()
        self.group.round_payoffs()
        # self.group.total_payoff()


class ClosingPage(Page):
    form_model = 'player'
    form_fields = ['gender','age']


page_sequence = [
    BeforeAllocationWP,
    Allocation,
    AllocationWP,
    ClosingPage,
]
