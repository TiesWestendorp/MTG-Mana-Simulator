from typing import TYPE_CHECKING
from random import shuffle
if TYPE_CHECKING:
    from mtg_mana_simulator.context import Context

def shuffle_library(context: "Context") -> None:
    shuffle(context.zones["deck"])

def basic_untapped_into_play(context: "Context") -> None:
    library = context.zones["deck"]
    indices = [index for index in range(len(library)) if library[index].name == "Basic land"]
    if len(indices) > 0:
        context.play_card("deck", indices[0])
        context.land += 1 # Searching a basic doesn't count as playing a land
        shuffle_library(context)

def basic_tapped_into_play(context: "Context") -> None:
    library = context.zones["deck"]
    indices = [index for index in range(len(library)) if library[index].name == "Basic land"]
    if len(indices) > 0:
        context.play_card("deck", indices[0])
        context.mana -= 1 # It came into play tapped, so didn't give mana this turn
        context.land += 1 # Searching a basic doesn't count as playing a land
        shuffle_library(context)

def basic_to_hand(context: "Context") -> None:
    library = context.zones["deck"]
    indices = [index for index in range(len(library)) if library[index].name == "Basic land"]
    if len(indices) > 0:
        context.zones["hand"].append(library.pop(indices[0]))
        shuffle_library(context)
