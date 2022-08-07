"""
Defines the Repository dictionary, which maps names to Cards
"""

from collections import defaultdict
from mtg_mana_simulator.actions import basic_tapped_into_play, basic_to_hand
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.sequence import Sequence

Repository = defaultdict(lambda: Card.filler)
Repository['Arcane Signet'] =   Card.untapped_rock(2, 1)
Repository['Azorius Signet'] =  Card.untapped_rock(2, 1)
Repository['Boros Signet'] =    Card.untapped_rock(2, 1)
Repository['Golgari Signet'] =  Card.untapped_rock(2, 1)
Repository['Gruul Signet'] =    Card.untapped_rock(2, 1)
Repository['Izzet Signet'] =    Card.untapped_rock(2, 1)
Repository['Dimir Signet'] =    Card.untapped_rock(2, 1)
Repository['Orzhov Signet'] =   Card.untapped_rock(2, 1)
Repository['Rakdos Signet'] =   Card.untapped_rock(2, 1)
Repository['Selesnya Signet'] = Card.untapped_rock(2, 1)
Repository['Simic Signet'] =    Card.untapped_rock(2, 1)
Repository['Azorius Locket'] =  Card.untapped_rock(3, 1)
Repository['Boros Locket'] =    Card.untapped_rock(3, 1)
Repository['Golgari Locket'] =  Card.untapped_rock(3, 1)
Repository['Gruul Locket'] =    Card.untapped_rock(3, 1)
Repository['Izzet Locket'] =    Card.untapped_rock(3, 1)
Repository['Dimir Locket'] =    Card.untapped_rock(3, 1)
Repository['Orzhov Locket'] =   Card.untapped_rock(3, 1)
Repository['Rakdos Locket'] =   Card.untapped_rock(3, 1)
Repository['Selesnya Locket'] = Card.untapped_rock(3, 1)
Repository['Simic Locket'] =    Card.untapped_rock(3, 1)
Repository['Azusa, Lost but Seeking'] = Card(cost=3, land_sequence=Sequence.repeat(2))
Repository['Dark Ritual'] = Card(cost=1, mana_sequence=Sequence.once(3))
Repository['Gitaxian Probe'] = Card.draw_spell(0, 1)
Repository['Illusion of Choice'] = Card.cantrip
Repository['Peek'] = Card.cantrip
Repository['Phyrexian Arena'] = Card(cost=3, draw_sequence=Sequence.one.prefixed_by([0]))
Repository['Reach Through Mists'] = Card.cantrip
Repository['Plains'] =          Card.untapped_land
Repository['Island'] =          Card.untapped_land
Repository['Swamp'] =           Card.untapped_land
Repository['Mountain'] =        Card.untapped_land
Repository['Forest'] =          Card.untapped_land
Repository['Azorius Guildgate'] =  Card.tapped_land
Repository['Boros Guildgate'] =    Card.tapped_land
Repository['Golgari Guildgate'] =  Card.tapped_land
Repository['Gruul Guildgate'] =    Card.tapped_land
Repository['Izzet Guildgate'] =    Card.tapped_land
Repository['Dimir Guildgate'] =    Card.tapped_land
Repository['Orzhov Guildgate'] =   Card.tapped_land
Repository['Rakdos Guildgate'] =   Card.tapped_land
Repository['Selesnya Guildgate'] = Card.tapped_land
Repository['Simic Guildgate'] =    Card.tapped_land
Repository['Arcane Sanctum'] =       Card.tapped_land
Repository['Crumbling Necropolis'] = Card.tapped_land
Repository['Frontier Bivouac'] =     Card.tapped_land
Repository['Jungle Shrine'] =        Card.tapped_land
Repository['Mystic Monastery'] =     Card.tapped_land
Repository['Nomad Outpost'] =        Card.tapped_land
Repository['Opulent Palace'] =       Card.tapped_land
Repository['Sandsteppe Citadel'] =   Card.tapped_land
Repository['Savage Lands'] =         Card.tapped_land
Repository['Seaside Citadel'] =      Card.tapped_land
Repository['Akoum Refuge'] =      Card.tapped_land
Repository['Bloodfell Caves'] =   Card.tapped_land
Repository['Blossoming Sands'] =  Card.tapped_land
Repository['Dismal Backwater'] =  Card.tapped_land
Repository['Graypelt Refuge'] =   Card.tapped_land
Repository['Jungle Hollow'] =     Card.tapped_land
Repository['Jwar Isle Refuge'] =  Card.tapped_land
Repository['Kazandu Refuge'] =    Card.tapped_land
Repository['Rugged Highlands'] =  Card.tapped_land
Repository['Scoured Barrens'] =   Card.tapped_land
Repository['Sejiri Refuge'] =     Card.tapped_land
Repository['Swiftwater Cliffs'] = Card.tapped_land
Repository['Thornwood Falls'] =   Card.tapped_land
Repository['Tranquil Cove'] =     Card.tapped_land
Repository['Wind-Scarred Crag'] = Card.tapped_land

Repository["Nature's Lore"] = Card(
    "Nature's Lore",
    cost=2,
    transform=[basic_tapped_into_play]
)
Repository['Cultivate'] = Card(
    "Cultivate",
    cost=3,
    transform=[basic_tapped_into_play, basic_to_hand]
)
