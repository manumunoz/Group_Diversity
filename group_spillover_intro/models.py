from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from collections import OrderedDict
import json
import itertools


author = 'Manu Munoz'

doc = """
Group Spillovers Instructions
"""


class Constants(BaseConstants):
    name_in_url = 'group_spillover_intro'
    names = ['1', '2', '3', '4']
    players_per_group = len(names)
    num_rounds = 1
    # instructions_template = 'group_spillover_intro/Instructions.html'
    #==================================
    # PAYOFFS
    highpay = 3
    lowpay = 1
    nopay = 0
    show_up = 5
    total_group_pay = 800
    total_group_no_pay = 0
    #==================================
    # CHOSEN ROUNDS
    chosen_num_rounds = 12
    goal_value = 8
    pay_rounds = [2,4,6,7,8,9,12,13,14,15,17,20]
    #==================================
    # Treatment & Group parameters
    part_pre_min = 1
    part_coord = 2
    part_post_min = 3
    part_alloc = 4
    exp_currency = "dólares experimentales"
    #------------------------------------------
    low_fav = [1,2,3,4]
    med_fav_1 = [1,3]
    med_fav_2 = [2,4]
    high_fav_1 = [1]
    high_fav_2 = [2]
    high_fav_3 = [3]
    high_fav_4 = [4]
    #------------------------------------------

class Subsession(BaseSubsession):
    def creating_session(self):
        treat = itertools.cycle([1, 2, 3])
        # for p in self.get_players():
        #     p.treat = next(treat)
        for p in self.get_players():
            if 'treatment' in self.session.config:
                # demo mode
                p.treat = self.session.config['treatment']
            else:
                # live experiment mode
                p.treat = next(treat)

            if p.treat == 1:
                p.type = 1

            elif p.treat == 2:
                if p.id_in_group == 1 or p.id_in_group == 2:
                    p.type = 1
                else:
                    p.type = 2
            else:
                if p.id_in_group == 1:
                    p.type = 1
                elif p.id_in_group == 2:
                    p.type = 2
                elif p.id_in_group == 3:
                    p.type = 3
                else:
                    p.type = 4

        num_players_err = 'Too many participants for such a short name list'
        # the following may create issues with mTurk sessions where num participants is doubled
        assert len(Constants.names) <= self.session.num_participants, num_players_err
        for g in self.get_groups():
            cur_names = Constants.names.copy()
            # random.shuffle(cur_names)
            for i, p in enumerate(g.get_players()):
                p.name = cur_names[i]


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treat = models.IntegerField() # Treatments from 1 to 3
    type = models.IntegerField()

    q_samegroup = models.PositiveIntegerField(
        choices=[
            [1, 'Sí'],
            [2, 'No'],
        ],
        widget=widgets.RadioSelect
    )

    q_option = models.PositiveIntegerField(
        choices=[
            [1, 'Envía el mismo primer mensaje que los demás participantes en su grupo en la Etapa 1'],
            [2, 'Envía el mismo segundo mensaje en la Etapa 2 que el primer mensaje que envía en la Etapa 1'],
            [3, 'Elige la misma opción que los demás participantes en su grupo en la Etapa 3'],
            [4, 'Elige la misma opción en la Etapa 3 que el mensaje que usted envió en la Etapa 2'],
        ],
        widget=widgets.RadioSelect
    )

    q_points = models.PositiveIntegerField(
        choices=[
            [1, 'Los participantes 1 y 2 ganan tres puntos y los participantes 3 y 4 ganan un punto'],
            [2, 'Los participantes 1 y 2 ganan un punto y los participantes 3 y 4 ganan tres puntos'],
            [3, 'El participante 3 gana tres puntos y los participantes 1, 2 y 4 ganan un punto'],
            [4, 'Todos los participantes ganan tres puntos'],
        ],
        widget=widgets.RadioSelect
    )

    q_rounds = models.PositiveIntegerField(
        choices=[
            [1, '8'],
            [2, '20'],
            [3, '12'],
            [4, '10'],
        ],
        widget=widgets.RadioSelect
    )

    q_coord = models.PositiveIntegerField(
        choices=[
            [1, '8'],
            [2, '20'],
            [3, '12'],
            [4, '10'],
        ],
        widget=widgets.RadioSelect
    )

    q_dollars = models.PositiveIntegerField(
        choices=[
            [1, '800 x (55/11) = 4000'],
            [2, '800 + (55-11) = 844'],
            [3, '800 x (11/55) = 160'],
            [4, '800 = 800'],
        ],
        widget=widgets.RadioSelect
    )

    name = models.StringField()