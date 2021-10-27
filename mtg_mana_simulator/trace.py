"""
Defines the Trace class which models the gathered statistics in each playthrough
"""

from typing import List, Optional
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.helpers import running_maximum

class Trace:
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
        self.mana[turn] = max(self.mana[turn], context.mana + context.gold)
        self.draw[turn] = max(self.draw[turn], context.draw)
        self.max_mana[turn] = max(self.max_mana[turn], context.max_mana())
        self.max_draw[turn] = max(self.max_draw[turn], context.max_draw())

    def finalize(self) -> None:
        self.max_mana = running_maximum(self.max_mana)
        self.max_draw = running_maximum(self.max_draw)
