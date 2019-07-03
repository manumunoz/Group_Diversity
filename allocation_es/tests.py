from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Allocation_es,
               {'alloc': random.choice([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])})

        yield (pages.ClosingPage_es,
               {'age': random.choice([18,90]),
                'gender': random.choice([0, 1])})


# App Test
# otree test sticky_es --export=test_sticky_es