from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.FirstSignal,
               {'first': random.choice([1,2,3,4])})
        yield (pages.SecondSignal,
               {'second': random.choice([1,2,3,4])})
        yield (pages.Action,
               {'action': random.choice([1,2,3,4])})
        if self.round_number == Constants.num_rounds:
            yield (pages.LastPage)
            yield (pages.Results)


# otree test low_diversity --export=test_low_diversity
# otree test medium_diversity --export=test_medium_diversity
# otree test high_diversity --export=test_high_diversity

# otree test min_effort_calc
