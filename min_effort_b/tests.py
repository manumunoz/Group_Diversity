from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Effort,
               {'effort': random.choice([1,2,3,4,5,6,7])})

        yield (pages.PostEffort)
