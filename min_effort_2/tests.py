from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Effort,
               {'effort': random.choice(range(1,60,1))})

        yield (pages.PostEffort)


# otree test min_effort_2
