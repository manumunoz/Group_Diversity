from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Start_es)

        yield (pages.IntroEffort_es,
               {'q_samegroup': 1, 'q_min': 4, 'q_pay': 1})

        yield (pages.Effort_es,
               {'effort': random.choice(range(1,60,1))})

        yield (pages.PostEffort_es)


# otree test min_effort_calc
