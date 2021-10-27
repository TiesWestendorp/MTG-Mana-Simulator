"""
Defines the Trace class which models the gathered measurements in each playthrough
"""

from typing import List, Optional
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.helpers import running_maximum

class Trace:
    """
    Container class for measurements done during a single playthrough
    """

    def __init__(self, turns: int, *,
            mana: Optional[List[int]] = None,
            draw: Optional[List[int]] = None,
            max_mana: Optional[List[int]] = None,
            max_draw: Optional[List[int]] = None) -> None:
        self.mana = mana if mana is not None else turns*[0]
        self.draw = draw if draw is not None else turns*[0]
        self.max_mana = max_mana if max_mana is not None else turns*[0]
        self.max_draw = max_draw if max_draw is not None else turns*[0]

    def update(self, turn: int, context: Context) -> None:
        """Update measurements in trace according to given turn and context"""
        self.mana[turn]     = max(self.mana[turn], context.mana + context.gold)
        self.draw[turn]     = max(self.draw[turn], context.draw)
        self.max_mana[turn] = max(self.max_mana[turn], context.max_mana())
        self.max_draw[turn] = max(self.max_draw[turn], context.max_draw())

    def finalize(self) -> "Trace":
        """Replace certain measurements by their running maxima"""
        # Replace max_mana and max_draw by their running maxima. It was possible
        # for the AI to not do something this turn, but to postpone it to a later
        # turn. This is relevant to decrease variance when cards like Dark Ritual
        # appear in a deck, or divination appear in a deck.
        self.max_mana = running_maximum(self.max_mana)
        self.max_draw = running_maximum(self.max_draw)
        return self
