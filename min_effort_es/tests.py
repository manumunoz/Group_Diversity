from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Start_es)

        yield (pages.IntroEffort_es,
               {'q_min': 2, 'q_pay': 2})

        yield (pages.Effort_es,
               {'effort': random.choice(range(1,60,1))})

        yield (pages.PostEffort_es)


# otree test min_effort_calc
