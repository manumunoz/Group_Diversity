from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
from collections import OrderedDict
import json


class StartWP(WaitPage):
    wait_for_all_groups = True


class Start_es(Page):
    pass

class BeforeIntroEffortWP(WaitPage):
    wait_for_all_groups = True


class IntroEffort_es(Page):
    form_model = 'player'
    form_fields = ['q_min','q_pay']

    def q_min_error_message(self, value):
        if value != 2:
            return 'Usted no eligió el menor número entre las opciones'

    def q_pay_error_message(self, value):
        if value != 2:
            return 'Recuerde que usted paga un costo de 1 multiplicado por el número que seleccione y recibe 2 por el ' \
                   'menor número elegido en su grupo'


class BeforeEffortWP(WaitPage):
    wait_for_all_groups = True


class Effort_es(Page):
    form_model = 'player'
    form_fields = ['effort', 'test_effort', 'test_minimum']


class BeforeNextRoundWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_effort()
        self.group.set_min_effort()
        self.group.round_gains()


class PostEffort_es(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.var_between_apps()


page_sequence = [
    StartWP,
    Start_es,
    BeforeIntroEffortWP,
    IntroEffort_es,
    BeforeEffortWP,
    Effort_es,
    BeforeNextRoundWP,
    PostEffort_es
]
