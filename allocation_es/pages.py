from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class StartWP(WaitPage):
    wait_for_all_groups = True

class Start_es(Page):
    pass

class BeforeIntroAlloctWP(WaitPage):
    wait_for_all_groups = True


class IntroAlloc_es(Page):
    form_model = 'player'
    form_fields = ['q_samegroup','q_implement','q_gains']

    def q_samegroup_error_message(self, value):
        if value != 1:
            return 'El grupo de participantes con el que usted interactúa en la Parte 4 es igual al grupo de la Parte 3'

    def q_implement_error_message(self, value):
        if value != 4:
            return 'El computador elegirá aleatoriamente la asignación de uno de los cuatro participantes para implementar'

    def q_gains_error_message(self, value):
        if value != 3:
            return 'Si su asignación es implementada, los dólares que usted envíe irán a su pareja y la cantidad restante será para usted'


class BeforeAllocationWP(WaitPage):
    wait_for_all_groups = True


class Allocation_es(Page):
    form_model = 'player'
    form_fields = ['alloc']


class AllocationWP(WaitPage):
    # wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.group.chosen_allocation()
        self.group.set_allocations()
        self.group.set_pairs()
        self.group.round_payoffs()
        # self.group.total_payoff()


class ClosingPage_es(Page):
    form_model = 'player'
    form_fields = ['gender','age']

    def before_next_page(self):
        self.player.var_between_apps()


page_sequence = [
    StartWP,
    Start_es,
    BeforeIntroAlloctWP,
    IntroAlloc_es,
    BeforeAllocationWP,
    Allocation_es,
    AllocationWP,
    ClosingPage_es,
]
