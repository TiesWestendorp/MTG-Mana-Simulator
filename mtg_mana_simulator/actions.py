from random import choice, shuffle
if TYPE_CHECKING:
    from mtg_mana_simulator.context import Context

def shuffle_library(context: "Context") -> None:
    shuffle(context.zones["deck"])

def basic_untapped_into_play(context: "Context") -> None:
    library = context.zones["deck"]
    indices = [index for index in range(len(library)) if library[index].name == "Basic land"]
    if len(indices) > 0:
        context.play_card("deck", choice(indices))

def basic_tapped_into_play(context: "Context") -> None:
    # To do
    library = context.zones["deck"]
    indices = [index for index in range(len(library)) if library[index].name == "Basic land"]
    if len(indices) > 0:
        context.play_card("deck", choice(indices))
