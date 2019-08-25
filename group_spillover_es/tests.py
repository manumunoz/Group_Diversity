from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield (pages.Begin_es)

            if self.player.treat == 1:
                yield (pages.IntroCoord_es,
                       {'q_samegroup': 2, 'q_option': 3, 'q_points': 4, 'q_rounds': 3, 'q_coord': 1, 'q_dollars': 3})
            elif self.player.treat == 2:
                yield (pages.IntroCoord_es,
                       {'q_samegroup': 2, 'q_option': 3, 'q_points': 2, 'q_rounds': 3, 'q_coord': 1, 'q_dollars': 3})
            elif self.player.treat == 3:
                yield (pages.IntroCoord_es,
                       {'q_samegroup': 2, 'q_option': 3, 'q_points': 3, 'q_rounds': 3, 'q_coord': 1, 'q_dollars': 3})

        yield (pages.Start_es)

        yield (pages.FirstSignal_es,
               {'first': random.choice([1,2,3,4])})

        yield (pages.SecondSignal_es,
               {'second': random.choice([1,2,3,4])})

        yield (pages.Action_es,
               {'action': random.choice([1,2,3,4])})

        if self.round_number == Constants.num_rounds:
            yield (pages.LastPage_es)

            yield (pages.Results_es)


# otree test low_diversity_es --export=test_low_diversity_es
# otree test medium_diversity_es --export=test_medium_diversity_es
# otree test high_diversity_es --export=test_high_diversity_es

# otree test low_diversity
