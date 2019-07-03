from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.RandomPay)

# App Test
# otree test pay_es --export=test_pay_es
# Treatment Test
# otree test sticky_es --export=test_sticky_es
# otree test blurry_es --export=test_blurry_es
# otree test blurry_cost_es --export=test_blurry_cost_es