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
Group Spillovers
"""


class Constants(BaseConstants):
    name_in_url = 'group_spillover_es'
    names = ['1', '2', '3', '4']
    players_per_group = len(names)
    num_rounds = 20
    # instructions_template = 'group_spillover/Instructions.html'
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
    total_one = models.IntegerField()
    total_two = models.IntegerField()
    total_three = models.IntegerField()
    total_four = models.IntegerField()
    coordination = models.IntegerField(initial=0)
    old_coordination = models.IntegerField(initial=0)
    total_coordination = models.IntegerField(initial=0)
    old_total_coordination = models.IntegerField(initial=0)
    network_data = models.LongStringField()
    win = models.IntegerField(initial=0)
    old_win = models.IntegerField()
    win_one = models.IntegerField(initial=0)
    win_two = models.IntegerField(initial=0)
    win_three = models.IntegerField(initial=0)
    win_four = models.IntegerField(initial=0)
    goal_achieved = models.IntegerField(initial=0)
    old_goal_achieved = models.IntegerField(initial=0)
    group_points = models.IntegerField(initial=0)
    group_total_points = models.IntegerField(initial=0)
    old_group_total_points = models.IntegerField(initial=0)
    total_win_one = models.IntegerField(initial=0)
    total_win_two = models.IntegerField(initial=0)
    total_win_three = models.IntegerField(initial=0)
    total_win_four = models.IntegerField(initial=0)
    old_total_win_one = models.IntegerField(initial=0)
    old_total_win_two = models.IntegerField(initial=0)
    old_total_win_three = models.IntegerField(initial=0)
    old_total_win_four = models.IntegerField(initial=0)
    # Selected rounds:
    chosen_coordination = models.IntegerField(initial=0)
    chosen_total_coordination = models.IntegerField(initial=0)
    chosen_group_points = models.IntegerField(initial=0)
    chosen_group_total_points = models.IntegerField(initial=0)
    chosen_win_one = models.IntegerField(initial=0)
    chosen_win_two = models.IntegerField(initial=0)
    chosen_win_three = models.IntegerField(initial=0)
    chosen_win_four = models.IntegerField(initial=0)
    chosen_total_win_one = models.IntegerField(initial=0)
    chosen_total_win_two = models.IntegerField(initial=0)
    chosen_total_win_three = models.IntegerField(initial=0)
    chosen_total_win_four = models.IntegerField(initial=0)

    def determine_win(self):
        if self.total_one == 4:
            self.win = 1
        elif self.total_two == 4:
            self.win = 2
        elif self.total_three == 4:
            self.win = 3
        elif self.total_four == 4:
            self.win = 4
        if self.win == 1:
            self.win_one = 1
        elif self.win == 2:
            self.win_two = 1
        elif self.win == 3:
            self.win_three = 1
        elif self.win == 4:
            self.win_four = 1
        if self.win != 0:
            self.coordination = 1

    def set_coordination(self):
        a = self.get_player_by_role('1')
        b = self.get_player_by_role('2')
        c = self.get_player_by_role('3')
        d = self.get_player_by_role('4')

        for player in [a, b, c, d]:
            if player.treat == 1:
                if self.coordination == 1 and player.action in Constants.low_fav:
                    player.is_winner = True
                else:
                    player.is_winner = False
            elif player.treat == 2:
                if self.coordination == 1 and player.action in Constants.med_fav_1:
                    if player.type == 1:
                        player.is_winner = True
                    elif player.type == 2:
                        player.is_winner = False
                elif self.coordination == 1 and player.action in Constants.med_fav_2:
                    if player.type == 1:
                        player.is_winner = False
                    elif player.type == 2:
                        player.is_winner = True
            else:
                if self.coordination == 1 and player.action in Constants.high_fav_1:
                    if player.type == 1:
                        player.is_winner = True
                    else:
                        player.is_winner = False
                elif self.coordination == 1 and player.action in Constants.high_fav_2:
                    if player.type == 2:
                        player.is_winner = True
                    else:
                        player.is_winner = False
                elif self.coordination == 1 and player.action in Constants.high_fav_3:
                    if player.type == 3:
                        player.is_winner = True
                    else:
                        player.is_winner = False
                elif self.coordination == 1 and player.action in Constants.high_fav_4:
                    if player.type == 4:
                        player.is_winner = True
                    else:
                        player.is_winner = False

        for player in [a, b, c, d]:
            if self.coordination == 1:
                if player.is_winner is True:
                    player.points = Constants.highpay
                else:
                    player.points = Constants.lowpay
            else:
                player.points = Constants.nopay

        for player in [a, b, c, d]:
            player.total_points = sum([player.points for player in player.in_all_rounds()])

    def total_points(self):
        players = self.get_players()
        point = [p.points for p in players]
        self.group_points = sum(point)

    def play_payment_rounds(self):
        for player in self.get_players():
            if self.round_number in Constants.pay_rounds:
                player.chosen_points = player.points
            else:
                player.chosen_points = 0

        for player in self.get_players():
            player.chosen_total_points = sum([player.chosen_points for player in player.in_all_rounds()])

    def grp_payment_rounds(self):
        if self.round_number in Constants.pay_rounds:
            self.chosen_coordination = self.coordination
            self.chosen_group_points = self.group_points
            self.chosen_win_one = self.win_one
            self.chosen_win_two = self.win_two
            self.chosen_win_three = self.win_three
            self.chosen_win_four = self.win_four
        else:
            self.chosen_coordination = 0
            self.chosen_group_points = 0
            self.chosen_win_one = 0
            self.chosen_win_two = 0
            self.chosen_win_three = 0
            self.chosen_win_four = 0

    def total_values(self):
        self.total_coordination = sum([g.coordination for g in self.in_all_rounds()])
        self.group_total_points = sum([g.group_points for g in self.in_all_rounds()])
        self.total_win_one = sum([g.win_one for g in self.in_all_rounds()])
        self.total_win_two = sum([g.win_two for g in self.in_all_rounds()])
        self.total_win_three = sum([g.win_three for g in self.in_all_rounds()])
        self.total_win_four = sum([g.win_four for g in self.in_all_rounds()])
        self.chosen_total_coordination = sum([g.chosen_coordination for g in self.in_all_rounds()])
        self.chosen_group_total_points = sum([g.chosen_group_points for g in self.in_all_rounds()])
        self.chosen_total_win_one = sum([g.chosen_win_one for g in self.in_all_rounds()])
        self.chosen_total_win_two = sum([g.chosen_win_two for g in self.in_all_rounds()])
        self.chosen_total_win_three = sum([g.chosen_win_three for g in self.in_all_rounds()])
        self.chosen_total_win_four = sum([g.chosen_win_four for g in self.in_all_rounds()])

    def goal_achievement(self):
        if self.chosen_total_coordination >= Constants.goal_value:
            self.goal_achieved = 1
        else:
            self.goal_achieved = 0

    def finalpay_value(self):
        for player in self.get_players():
            if self.goal_achieved == 1:
                if self.round_number == Constants.num_rounds:
                    player.final_pay = (player.chosen_total_points * Constants.total_group_pay)/self.chosen_group_total_points
            else:
                player.final_pay = 0

    def displaying_network(self):
        nodes = [{'data': {'id': i, 'name': i, 'first': self.get_player_by_id(i).first, 'second': self.get_player_by_id(i).second,
                           'action': self.get_player_by_id(i).action, 'old_action': self.get_player_by_id(i).old_action},  'group': 'nodes'} for i in Constants.names]
        edges = []
        elements = nodes + edges
        style = [{'selector': 'node', 'style': {'content': 'data(name)'}}]
        self.network_data = json.dumps({'elements': elements,
                                        'style': style,
                                        })


class Player(BasePlayer):
    treat = models.IntegerField() # Treatments from 1 to 3
    old_action = models.PositiveIntegerField()
    action_one = models.IntegerField(initial=0)
    action_two = models.IntegerField(initial=0)
    action_three = models.IntegerField(initial=0)
    action_four = models.IntegerField(initial=0)
    points = models.IntegerField()
    old_points = models.IntegerField(initial=0)
    total_points = models.IntegerField(initial=0)
    old_total_points = models.IntegerField(initial=0)
    is_winner = models.BooleanField()
    # favorite = models.IntegerField()
    type = models.IntegerField()
    final_pay = models.FloatField()
    chosen_coord = models.IntegerField()
    chosen_points = models.IntegerField()
    chosen_total_points = models.IntegerField(initial=0)

    first = models.PositiveIntegerField(
        choices=[
            [1, 'orange'],
            [2, 'green'],
            [3, 'blue'],
            [4, 'red']
        ],
        widget=widgets.RadioSelect
    )
    second = models.PositiveIntegerField(
        choices=[
            [1, 'orange'],
            [2, 'green'],
            [3, 'blue'],
            [4, 'red']
        ],
        widget=widgets.RadioSelect
    )
    action = models.PositiveIntegerField(
        choices=[
            [1, 'orange'],
            [2, 'green'],
            [3, 'blue'],
            [4, 'red']
        ],
        widget=widgets.RadioSelect
    )

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


    def role(self):
        return {1: '1', 2: '2', 3: '3', 4: '4'}[self.id_in_group]

    def choice_value(self):
        if self.action == 1:
            self.action_one = 1
        elif self.action == 2:
            self.action_two = 1
        elif self.action == 3:
            self.action_three = 1
        else:
            self.action_four = 1


    name = models.StringField()
    friends = models.LongStringField()

# for i in Constants.names:
#     Player.add_to_class(i, models.BooleanField(widget=widgets.CheckboxInput, blank=True))

    def var_between_apps(self):
        self.participant.vars['win_one'] = self.group.chosen_total_win_one
        self.participant.vars['win_two'] = self.group.chosen_total_win_two
        self.participant.vars['win_three'] = self.group.chosen_total_win_three
        self.participant.vars['win_four'] = self.group.chosen_total_win_four
        self.participant.vars['group_points'] = self.group.chosen_group_total_points
        self.participant.vars['points'] = self.chosen_total_points
        self.participant.vars['coordinations'] = self.group.chosen_total_coordination
        self.participant.vars['coord_point'] = self.final_pay
