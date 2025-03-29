from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Set, Union

from BaseClasses import CollectionState, MultiWorld

from .data import RegionData
from .locations import PokemonCrystalLocation
from .options import LevelScaling, JohtoOnly
from .regions import RegionData
from .utils import bound

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


@dataclass
class ScalingData:
    name: str # name of the data set, aka johto_trainer_data
    region: str # should be identical to regions.json
    type: Optional[str] # Trainer Scaling, Static Scaling, or Wild Scaling
    connections: Optional[List[str]] # to other regions, from regions.json. will become important when wilds logic
    data_ids: Union[str, List[str]] # name: name that we use only here, data id: [ADDRESS_LABEL]


# pretty sure this is unnecessary now; it existed to create the data to be used to create the plando
# locations, but since i just added the trainers to the regions inherently, this data doesn't need to
# be created because it already exists.  once the plandos are made, the data doesn't get used again.
def create_scaling_data(world: "PokemonCrystalWorld"):

# All this data will probably be trashed, since I'm housing it within regions.json itself

    johto_trainer_data = {
        "REGION_CHERRYGROVE_CITY": [
            {"name": "Cherrygrove City Rival", "type": "Trainer Scaling", "data_ids": ["RIVAL_CHERRYGROVE_CHIKORITA", "RIVAL_CHERRYGROVE_CYNDAQUIL", "RIVAL_CHERRYGROVE_TOTODILE"]}
        ],
        "REGION_ROUTE_30": [
            {"name": "Youngster Joey", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_JOEY_1"]},
            {"name": "Youngster Mikey", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_MIKEY"]},
            {"name": "Bug Catcher Don", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_DONE"]}
        ],
#        "REGION_POKEGEAR_1": [
#            {"name": "Youngster Joey - Rematch 1", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_JOEY_2"]},
#            {"name": "Youngster Joey - Rematch 2", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_JOEY_3"]},
#            {"name": "Youngster Joey - Rematch 3", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_JOEY_4"]},
#            {"name": "Youngster Joey - Rematch 4", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_JOEYE_5"]}
#        ],
#       "REGION_POKEGEAR_2": [
#       requires player to have reached goldenrod; ENGINE_FLYPOINT_GOLDENROD
#       ]
        "REGION_ROUTE_31": [
            {"name": "Bug Catcher Wade", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_WADE_1"]}
        ],
        "REGION_SPROUT_TOWER_1F": [
            {"name": "Sage Chow", "type": "Trainer Scaling", "data_ids": ["SAGE_CHOW"]}
        ],
        "REGION_SPROUT_TOWER_2F": [
            {"name": "Sage Nico", "type": "Trainer Scaling", "data_ids": ["SAGE_NICO"]},
            {"name": "Sage Edmond", "type": "Trainer Scaling", "data_ids": ["SAGE_EDMOND"]}
        ],
        "REGION_SPROUT_TOWER_3F": [
            {"name": "Sage Jin", "type": "Trainer Scaling", "data_ids": ["SAGE_JIN"]},
            {"name": "Sage Neal", "type": "Trainer Scaling", "data_ids": ["SAGE_NEAL"]},
            {"name": "Sage Troy", "type": "Trainer Scaling", "data_ids": ["SAGE_TROY"]},
            {"name": "Sage Li", "type": "Trainer Scaling", "data_ids": ["SAGE_LI"]}
        ],
        "REGION_VIOLET_GYM": [
            {"name": "Bird Keeper Abe", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_ABE"]},
            {"name": "Bird Keeper Rod", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_ROD"]},
            {"name": "Leader Falkner", "type": "Trainer Scaling", "data_ids": ["LEADER_FALKNER"]}
        ],
        "REGION_ROUTE_32:SOUTH": [
            {"name": "Camper Roland", "type": "Trainer Scaling", "data_ids": ["CAMPER_ROLAND"]},
            {"name": "Fisher Justin", "type": "Trainer Scaling", "data_ids": ["FISHER_JUSTIN"]},
            {"name": "Fisher Ralph", "type": "Trainer Scaling", "data_ids": ["FISHER_RALPH"]},
            {"name": "Fisher Henry", "type": "Trainer Scaling", "data_ids": ["FISHER_HENRY"]},
            {"name": "Picnicker Liz", "type": "Trainer Scaling", "data_ids": ["PICNICKER_LIZ"]},
            {"name": "Youngster Albert", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_ALBERT"]},
            {"name": "Youngster Gordon", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_GORDON"]},
            {"name": "Bird Keeper Peter", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_PETER"]}
        ],
        "REGION_RUINS_OF_ALPH_OUTSIDE:TRAINER": [
            {"name": "Psychic Nathan", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_NATHAN"]}
        ],
        "REGION_UNION_CAVE_1F": [
            {"name": "Hiker Russell", "type": "Trainer Scaling", "data_ids": ["HIKER_RUSSELL"]},
            {"name": "Hiker Daniel", "type": "Trainer Scaling", "data_ids": ["HIKER_DANIEL"]},
            {"name": "Fire Breather Bill", "type": "Trainer Scaling", "data_ids": ["FIREBREATHER_BILL"]},
            {"name": "Poke Maniac Larry", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_LARRY"]},
            {"name": "Fire Breather Ray", "type": "Trainer Scaling", "data_ids": ["FIREBREATHER_RAY"]}
        ],
        "REGION_UNION_CAVE_B1F:NORTH": [
            {"name": "Hiker Phillip", "type": "Trainer Scaling", "data_ids": ["HIKER_PHILLIP"]},
            {"name": "Hiker Leonard", "type": "Trainer Scaling", "data_ids": ["HIKER_LEONARD"]}
        ],
        "REGION_UNION_CAVE_B1F:SOUTH": [
            {"name": "Poke Maniac Andrew", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_ANDREW"]},
            {"name": "Poke Maniac Calvin", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_CALVIN"]}
        ],
        "REGION_UNION_CAVE_B2F": [
            {"name": "Cool Trainer Nick", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_NICK"]},
            {"name": "Cool Trainer Gwen", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_GWEN"]},
            {"name": "Cool Trainer Emma", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_EMMA"]}
        ],
        "REGION_ROUTE_33": [
            {"name": "Hiker Anthony", "type": "Trainer Scaling", "data_ids": ["HIKER_ANTHONY"]}
        ],
        "REGION_SLOWPOKE_WELL_B1F": [
            {"name": "Rocket Grunt Slowpoke Well 1", "type": "Trainer Scaling", "data_ids": ["GRUNTM_SLOWPOKE_WELL_1"]},
            {"name": "Rocket Grunt Slowpoke Well 2", "type": "Trainer Scaling", "data_ids": ["GRUNTF_SLOWPOKE_WELL_2"]},
            {"name": "Rocket Grunt Slowpoke Well 3", "type": "Trainer Scaling", "data_ids": ["GRUNTM_SLOWPOKE_WELL_3"]},
            {"name": "Rocket Grunt Slowpoke Well Boss", "type": "Trainer Scaling", "data_ids": ["GRUNTM_SLOWPOKE_WELL_4"]}
        ],
        "REGION_AZALEA_TOWN": [
            {"name": "Azalea Town Rival", "type": "Trainer Scaling", "data_ids": ["RIVAL_AZALEA_BAYLEEF", "RIVAL_AZALEA_QUILAVA", "RIVAL_AZALEA_CROCONAW"]}
        ],
        "REGION_AZALEA_GYM": [
            {"name": "Twins Amy and May", "type": "Trainer Scaling", "data_ids": ["TWINS_ANY_MAY_1", "TWINS_AMY_MAY_2"]},
            {"name": "Bug Catcher Benny", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_BENNY"]},
            {"name": "Bug Catcher Josh", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_JOSH"]},
            {"name": "Bug Catcher Al", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_AL"]},
            {"name": "Leader Bugsy", "type": "Trainer Scaling", "data_ids": ["LEADER_BUGSY"]}
        ],
        "REGION_ILEX_FOREST:NORTH": [
            {"name": "Bug Catcher Wayne", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_WAYNE"]}
        ],
        "REGION_ROUTE_34": [
            {"name": "Camper Todd", "type": "Trainer Scaling", "data_ids": ["CAMPER_TODD_1"]},
            {"name": "Picnicker Gina", "type": "Trainer Scaling", "data_ids": ["PICNICKER_GINA_1"]},
            {"name": "Youngster Samuel", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_SAMUEL"]},
            {"name": "Youngster Ian", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_IAN"]},
            {"name": "Poke Fan Brandon", "type": "Trainer Scaling", "data_ids": ["POKEFANM_BRANDON"]},
            {"name": "Officer Keith", "type": "Trainer Scaling", "data_ids": ["OFFICER_KEITH"]}
        ],
        "REGION_ROUTE_34:WATER": [
            {"name": "Cool Trainer Irene", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_IRENE"]},
            {"name": "Cool Trainer Jenn", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_JENN"]},
            {"name": "Cool Trainer Kate", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_KATE"]}
        ],
        "REGION_GOLDENROD_UNDERGROUND": [
            {"name": "Super Nerd Eric", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_ERIC"]},
            {"name": "Super Nerd Teru", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_TERU"]},
            {"name": "Poke Maniac Issac", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_ISSAC"]},
            {"name": "Poke Maniac Donald", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_DONALD"]}
        ],
        "REGION_GOLDENROD_GYM": [
            {"name": "Beauty Victoria", "type": "Trainer Scaling", "data_ids": ["BEAUTY_VICTORIA"]},
            {"name": "Beauty Samantha", "type": "Trainer Scaling", "data_ids": ["BEAUTY_SAMANTHA"]},
            {"name": "Lass Carrie", "type": "Trainer Scaling", "data_ids": ["LASS_CARRIE"]},
            {"name": "Lass Bridget", "type": "Trainer Scaling", "data_ids": ["LASS_BRIDGET"]},
            {"name": "Leader Whitney", "type": "Trainer Scaling", "data_ids": ["LEADER_WHITNEY"]}
        ],
        "REGION_ROUTE_35": [
            {"name": "Bird Keeper Bryan", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_BRYAN"]},
            {"name": "Juggler Irwin", "type": "Trainer Scaling", "data_ids": ["JUGGLER_IRWIN_1"]},
            {"name": "Camper Ivan", "type": "Trainer Scaling", "data_ids": ["CAMPER_IVAN"]},
            {"name": "Camper Elliot", "type": "Trainer Scaling", "data_ids": ["CAMPER_ELLIOT"]},
            {"name": "Picnicker Brooke", "type": "Trainer Scaling", "data_ids": ["PICNICKER_BROOKE"]},
            {"name": "Picnicker Kim", "type": "Trainer Scaling", "data_ids": ["PICNICKER_KIM"]},
            {"name": "Bug Catcher Arnie", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_ARNIE_1"]},
            {"name": "Fire Breather Walt", "type": "Trainer Scaling", "data_ids": ["FIREBREATHER_WALT"]},
            {"name": "Officer Dirk", "type": "Trainer Scaling", "data_ids": ["OFFICER_DIRK"]}
        ],
        "REGION_NATIONAL_PARK": [
            {"name": "School Boy Jack", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_JACK"]},
            {"name": "Poke Fan William", "type": "Trainer Scaling", "data_ids": ["POKEFANM_WILLIAM"]},
            {"name": "Poke Fan Beverly", "type": "Trainer Scaling", "data_ids": ["POKEFANF_BEVERLY_1"]},
            {"name": "Lass Krise", "type": "Trainer Scaling", "data_ids": ["LASS_KRISE"]}
        ],
        "REGION_ROUTE_36:WEST": [
            {"name": "School Boy Alan", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_ALAN_1"]},
            {"name": "Psychic Mark", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_MARK"]}
        ],
        "REGION_ROUTE_37": [
            {"name": "Twins Ann and Anne", "type": "Trainer Scaling", "data_ids": ["TWINS_ANN_ANNE_1", "TWINS_ANN_ANNE_2"]},
            {"name": "Psychic Greg", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_GREG"]}
        ],
        "REGION_BURNED_TOWER_1F": [
            {"name": "Burned Tower Rival", "type": "Trainer Scaling", "data_ids": ["RIVAL_ECRUTEAK_BAYLEEF", "RIVAL_ECRUTEAK_QUILAVA", "RIVAL_ECRUTEAK_CROCONAW"]}
        ],
        "REGION_DANCE_THEATER": [
            {"name": "Kimono Girl Naoko", "type": "Trainer Scaling", "data_ids": ["KIMONO_GIRL_NAOKO"]},
            {"name": "Kimono Girl Sayo", "type": "Trainer Scaling", "data_ids": ["KIMONO_GIRL_SAYO"]},
            {"name": "Kimono Girl Zuki", "type": "Trainer Scaling", "data_ids": ["KIMONO_GIRL_ZUKI"]},
            {"name": "Kimono Girl Kuni", "type": "Trainer Scaling", "data_ids": ["KIMONO_GIRL_KUNI"]},
            {"name": "Kimono Girl Miki", "type": "Trainer Scaling", "data_ids": ["KIMONO_GIRL_MIKI"]}
        ],
        "REGION_ECRUTEAK_GYM": [
            {"name": "Safe Jeffrey", "type": "Trainer Scaling", "data_ids": ["SAGE_JEFFREY"]},
            {"name": "Sage Ping", "type": "Trainer Scaling", "data_ids": ["SAGE_PING"]},
            {"name": "Medium Martha", "type": "Trainer Scaling", "data_ids": ["MEDIUM_MARTHA"]},
            {"name": "Medium Grace", "type": "Trainer Scaling", "data_ids": ["MEDIUM_GRACE"]},
            {"name": "Leader Morty", "type": "Trainer Scaling", "data_ids": ["LEADER_MORTY"]}
        ],
        "REGION_WISE_TRIOS_ROOM": [
            {"name": "Sage Gaku", "type": "Trainer Scaling", "data_ids": ["SAGE_GAKU"]},
            {"name": "Sage Masa", "type": "Trainer Scaling", "data_ids": ["SAGE_MASA"]},
            {"name": "Sage Koji", "type": "Trainer Scaling", "data_ids": ["SAGE_KOJI"]}
        ],
        "REGION_ROUTE_38": [
            {"name": "Bird Keeper Toby", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_TOBY"]},
            {"name": "Sailor Harry", "type": "Trainer Scaling", "data_ids": ["SAILOR_HARRY"]},
            {"name": "Lass Dana", "type": "Trainer Scaling", "data_ids": ["LASS_DANA_1"]},
            {"name": "School Boy Chad", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_CHAD_1"]},
            {"name": "Beauty Valerie", "type": "Trainer Scaling", "data_ids": ["BEAUTY_VALERIE"]},
            {"name": "Beauty Olivia", "type": "Trainer Scaling", "data_ids": ["BEAUTY_OLIVIA"]}
        ],
        "REGION_ROUTE_39": [
            {"name": "Psychic Norman", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_NORMAN"]},
            {"name": "Poke Fan Ruth", "type": "Trainer Scaling", "data_ids": ["POKEFANF_RUTH"]},
            {"name": "Poke Fan Derek", "type": "Trainer Scaling", "data_ids": ["POKEFANM_DEREK_1"]},
            {"name": "Sailor Eugene", "type": "Trainer Scaling", "data_ids": ["SAILOR_EUGENE"]},
            {"name": "Poke Fan Jaime", "type": "Trainer Scaling", "data_ids": ["POKEFANF_JAIME"]}
        ],
        "REGION_OLIVINE_LIGHTHOUSE_2F": [
            {"name": "Gentleman Alfred", "type": "Trainer Scaling", "data_ids": ["GENTLEMAN_ALFRED"]},
            {"name": "Sailor Huey", "type": "Trainer Scaling", "data_ids": ["SAILOR_HUEY_1"]}
        ],
        "REGION_OLIVINE_LIGHTHOUSE_3F": [
            {"name": "Bird Keeper Theo", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_THEO"]},
            {"name": "Gentleman Preston", "type": "Trainer Scaling", "data_ids": ["GENTLEMAN_PRESTON"]},
            {"name": "Sialor Terrell", "type": "Trainer Scaling", "data_ids": ["SAILOR_TERRELL"]}
        ],
        "REGION_OLIVINE_LIGHTHOUSE_4F": [
            {"name": "Lass Connie", "type": "Trainer Scaling", "data_ids": ["LASS_CONNIE"]},
            {"name": "Sailor Kent", "type": "Trainer Scaling", "data_ids": ["SAILOR_KENT"]}
        ],
        "REGION_OLIVINE_LIGHTHOUSE_5F": [
            {"name": "Bird Keeper Denis", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_DENIS"]},
            {"name": "Sailor Ernest", "type": "Trainer Scaling", "data_ids": ["SAILOR_ERNEST"]}
        ],
        "REGION_ROUTE_40:WATER": [
            {"name": "Swimmer Elaine", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_ELAINE"]},
            {"name": "Swimmer Paula", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_PAULA"]},
            {"name": "Swimmer Simon", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_SIMON"]},
            {"name": "Swimmer Randall", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_RANDALL"]}
        ],
        "REGION_ROUTE_41": [
            {"name": "Swimmer Kaylee", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_KAYLEE"]},
            {"name": "Swimmer Susie", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_SUSIE"]},
            {"name": "Swimmer Denise", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_DENISE"]},
            {"name": "Swimmer Kara", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_KARA"]},
            {"name": "Swimmer Wendy", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_WENDY"]},
            {"name": "Swimmer Charlie", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_CHARLIE"]},
            {"name": "Swimmer George", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_GEORGE"]},
            {"name": "Swimmer Berke", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_BERKE"]},
            {"name": "Swimmer Kirk", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_KIRK"]},
            {"name": "Swimmer Mathew", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_MATHEW"]}
        ],
        "REGION_CIANWOOD_CITY": [
            {"name": "Mystical Man Eusine", "type": "Trainer Scaling", "data_ids": ["MYSTICALMAN_EUSINE"]}
        ],
        "REGION_CIANWOOD_GYM": [
            {"name": "Blackbelt Yoshi", "type": "Trainer Scaling", "data_ids": ["BLACKBELT_YOSHI"]},
            {"name": "Blackbelt Lao", "type": "Trainer Scaling", "data_ids": ["BLACKBELT_LAO"]},
            {"name": "Blackbelt Nob", "type": "Trainer Scaling", "data_ids": ["BLACKBELT_NOB"]}
        ],
        "REGION_CIANWOOD GYM:STRENGTH": [
            {"name": "Blackbelt Lung", "type": "Trainer Scaling", "data_ids": ["BLACKBELT_LUNG"]},
            {"name": "Leader Chuck", "type": "Trainer Scaling", "data_ids": ["LEADER_CHUCK"]}
        ],
        "REGION_OLIVINE_GYM": [
            {"name": "Leader Jasmine", "type": "Trainer Scaling", "data_ids": ["LEADER_JASMINE"]}
        ],
        "REGION_MOUNT_MORTAR_1F_INSIDE:FRONT": [
            {"name": "Poke Maniac Miller", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_MILLER"]}
        ],
        "REGION_MOUNT_MORTAR_1F_INSIDE:STRENGTH": [
            {"name": "Super Nerd Markus", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_MARKUS"]}
        ],
        "REGION_MOUNT_MORTAR_B1F:BACK": [
            {"name": "Blackbelt Kiyo", "type": "Trainer Scaling", "data_ids": ["BLACKBELT_KIYO"]}
        ],
        "REGION_MOUNT_MORTAR_2F_INSIDE": [
            {"name": "Super Nerd Hugh", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_HUGH"]}
        ],
        "REGION_ROUTE_42:EAST": [
            {"name": "Fisher Tully", "type": "Trainer Scaling", "data_ids": ["FISHER_TULLY_1"]},
            {"name": "Poke Maniac Shane", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_SHANE"]},
            {"name": "Hiker Benjamin", "type": "Trainer Scaling", "data_ids": ["HIKER_BENJAMIN"]}
        ],
        "REGION_ROUTE_43": [
            {"name": "Camper Spencer", "type": "Trainer Scaling", "data_ids": ["CAMPER_SPENCER"]},
            {"name": "Picnicker Tiffany", "type": "Trainer Scaling", "data_ids": ["PICNICKER_TIFFANY_1"]},
            {"name": "Poke Maniac Ben", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_BEN"]},
            {"name": "Poke Maniac Brent", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_BRENT"]},
            {"name": "Poke Maniac Ron", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_RON"]},
            {"name": "Fisher Marvin", "type": "Trainer Scaling", "data_ids": ["FISHER_MARVIN"]}
        ],
        "REGION_LAKE_OF_RAGE": [
            {"name": "Fisher Andre", "type": "Trainer Scaling", "data_ids": ["FISHER_ANDRE"]},
            {"name": "Fisher Raymond", "type": "Trainer Scaling", "data_ids": ["FISHER_RAYMOND"]},
            {"name": "Cool Trainer Lois", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_LOIS"]}
        ],
        "REGION_LAKE_OF_RAGE:CUT": [
            {"name": "Cool Trainer Aaron", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_AARON"]}
        ],
        "REGION_TEAM_ROCKET_BASE_B1F": [
            {"name": "Rocket Grunt", "type": "Trainer Scaling", "data_ids": ["GRUNTM_ROCKET_HQ_B1F"]},
            {"name": "Scientist Jed", "type": "Trainer Scaling", "data_ids": ["SCIENTIST_JED"]}
        ],
        "REGION_TEAM_ROCKET_BASE_B2F": [
            {"name": "Rocket Grunt 1", "type": "Trainer Scaling", "data_ids": ["GRUNTM_ROCKET_HQ_B2F_1"]},
            {"name": "Rocket Grunt 2", "type": "Trainer Scaling", "data_ids": ["GRUNTM_ROCKET_HQ_B2F_2"]},
            {"name": "Rocket Grunt 3", "type": "Trainer Scaling", "data_ids": ["GRUNTM_ROCKET_HQ_B2F_3"]},
            {"name": "Rocket Executive", "type": "Trainer Scaling", "data_ids": ["EXECUTIVEF_ROCKET_HQ_B2F"]}
        ],
        "REGION_TEAM_ROCKET_BASE_B3F": [
            {"name": "Rocket Grunt Slowpoke Tail", "type": "Trainer Scaling", "data_ids": ["GRUNTF_ROCKET_HQ_SLOWPOKE_TAIL"]},
            {"name": "Rocket Grunt Raticate Tail", "type": "Trainer Scaling", "data_ids": ["GRUNTM_ROCKET_HQ_RATICATE_TAIL"]},
            {"name": "Scientist Ross", "type": "Trainer Scaling", "data_ids": ["SCIENTIST_ROSS"]},
            {"name": "Scientist Mitch", "type": "Trainer Scaling", "data_ids": ["SCIENTIST_MITCH"]},
            {"name": "Rocket Executive", "type": "Trainer Scaling", "data_ids": ["EXECUTIVEM_ROCKET_HQ_B3F"]}
        ],
        "REGION_MAHOGANY_GYM": [
            {"name": "Skier Roxanne", "type": "Trainer Scaling", "data_ids": ["SKIER_ROXANNE"]},
            {"name": "Skier Clarissa", "type": "Trainer Scaling", "data_ids": ["SKIER_CLARISSA"]},
            {"name": "Boarder Ronald", "type": "Trainer Scaling", "data_ids": ["BOARDER_RONALD"]},
            {"name": "Boarder Brad", "type": "Trainer Scaling", "data_ids": ["BOARDER_BRAD"]},
            {"name": "Boarder Douglas", "type": "Trainer Scaling", "data_ids": ["BOARDER_DOUGLAS"]},
            {"name": "Leader Pryce", "type": "Trainer Scaling", "data_ids": ["LEADER_PRYCE"]}
        ],
        "REGION_RADIO_TOWER_1F": [
            {"name": "Rocker Grunt", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_1F"]}
        ],
        "REGION_RADIO_TOWER_2F": [
            {"name": "Rocket Grunt 2", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_2F_2"]},
            {"name": "Rocket Grunt 3", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_2F_3"]},
            {"name": "Rocket Grunt 4", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_2F_4"]},
            {"name": "Rocket Grunt 1", "type": "Trainer Scaling", "data_ids": ["GRUNTF_RADIO_TOWER_2F_1"]}
        ],
        "REGION_RADIO_TOWER_3F:NOCARDKEY": [
            {"name": "Rocket Grunt 1", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_3F_1"]},
            {"name": "Rocket Grunt 2", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_3F_2"]},
            {"name": "Scientist Marc", "type": "Trainer Scaling", "data_ids": ["SCIENTIST_MARC"]}
        ],
        "REGION_RADIO_TOWER_4F:NOCARDKEY": [
            {"name": "Rocket Grunt", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_4F"]},
            {"name": "Scientist Rich", "type": "Trainer Scaling", "data_ids": ["SCIENTIST_RICH"]}
        ],
        "REGION_RADIO_TOWER_5F:NOCARDKEY": [
            {"name": "Rocket Executive False Director", "type": "Trainer Scaling", "data_ids": ["EXECUTIVEM_FALSE_DIRECTOR"]}
        ],
        "REGION_RADIO_TOWER_3F:CARDKEY": [
            {"name": "Rocket Grunt", "type": "Trainer Scaling", "data_ids": ["GRUNTM_RADIO_TOWER_3F_CARD_KEY"]}
        ],
        "REGION_RADIO_TOWER_4F:CARDKEY": [
            {"name": "Rocket Executive M", "type": "Trainer Scaling", "data_ids": ["EXECUTIVEM_RADIO_TOWER_4F"]},
            {"name": "Rocket Grunt", "type": "Trainer Scaling", "data_ids": ["GRUNTF_RADIO_TOWER_4F"]}
        ],
        "REGION_RADIO_TOWER_5F:CARDKEY": [
            {"name": "Rocket Executive F", "type": "Trainer Scaling", "data_ids": ["EXECUTIVEF_RADIO_TOWER_5F"]},
            {"name": "Rocket Executive M", "type": "Trainer Scaling", "data_ids": ["EXECUTIVEM_RADIO_TOWER_5F"]}
        ],
        "REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES": [
            {"name": "Goldenrod Underground Rival", "type": "Trainer Scaling", "data_ids": ["RIVAL_GOLDENROD_MEGANIUM", "RIVAL_GOLDENROD_TYPHLOSION", "RIVAL_GOLDENROD_FERALIGATR"]}
        ],
        "REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES:TAKEOVER": [
            {"name": "Rocket Grunt 1", "type": "Trainer Scaling", "data_ids": ["GRUNTM_GOLDENROD_TUNNEL_1"]},
            {"name": "Rocket Grunt 2", "type": "Trainer Scaling", "data_ids": ["GRUNTM_GOLDENROD_TUNNEL_2"]},
            {"name": "Burglar Duncan", "type": "Trainer Scaling", "data_ids": ["BURGLAR_DUNCAN"]},
            {"name": "Burglar Eddie", "type": "Trainer Scaling", "data_ids": ["BURGLAR_EDDIE"]},
            {"name": "Rocket Grunt 3", "type": "Trainer Scaling", "data_ids": ["GRUNTM_GOLDENROD_UNDERGROUND_3"]},
            {"name": "Rocket Grunt 4", "type": "Trainer Scaling", "data_ids": ["GRUNTF_GOLDENROD_UNDERGROUND_4"]}
        ],
        "REGION_GOLDENROD_UNDERGROUND_WAREHOUSE:TAKEOVER": [
            {"name": "Rocket Grunt 1", "type": "Trainer Scaling", "data_ids": ["GRUNTM_GOLDENROD_WAREHOUSE_1"]},
            {"name": "Rocket Grunt 2", "type": "Trainer Scaling", "data_ids": ["GRUNTM_GOLDENROD_WAREHOUSE_2"]},
            {"name": "Rocket Grunt 3", "type": "Trainer Scaling", "data_ids": ["GRUNTM_GOLDENROD_WAREHOUSE_3"]}
        ],
        "REGION_ROUTE_44": [
            {"name": "Bird Keeper Vance", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_VANCE_1"]},
            {"name": "Psychic Phil", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_PHIL"]},
            {"name": "Fisher Wilton", "type": "Trainer Scaling", "data_ids": ["FISHER_WILTON"]},
            {"name": "Fisher Edgar", "type": "Trainer Scaling", "data_ids": ["FISHER_EDGAR"]},
            {"name": "Cool Trainer Cybil", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_CYBIL"]},
            {"name": "Poke Maniac Zach", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_ZACH"]},
            {"name": "Cool Trainer Allen", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_ALLEN"]}
        ],
        "REGION_BLACKTHORN_GYM_1F": [
            {"name": "Cool Trainer Paul", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_PAUL"]}
        ],
        "REGION_BLACKTHORN_GYM_1F:STRENGTH": [
            {"name": "Cool Trainer Mike", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_MIKE"]},
            {"name": "Cool Trainer Lola", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_LOLA"]},
            {"name": "Leader Clair", "type": "Trainer Scaling", "data_ids": ["LEADER_CLAIR"]}
        ],
        "REGION_BLACKTHORN_GYM_2F": [
            {"name": "Cool Trainer Cody", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_CODY"]},
            {"name": "Cool Trainer Fran", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_FRAN"]}
        ],
        "REGION_DRAGONS_DEN_B1F": [
            {"name": "Cool Trainer Darin", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_DARIN"]}],
        "REGION_DRAGONS_DEN_B1F:WATER": [
            {"name": "Cool Trainer Cara", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_CARA"]},
            {"name": "Twins Lea and Pia", "type": "Trainer Scaling", "data_ids": ["TWINS_LEA_PIA_1", "TWINS_LEA_PIA_2"]}
        ],
        "REGION_ROUTE_45": [
            {"name": "Blackbelt Kenji", "type": "Trainer Scaling", "data_ids": ["BLACKBELT_KENJI_3"]},
            {"name": "Hiker Erik", "type": "Trainer Scaling", "data_ids": ["HIKER_ERIK"]},
            {"name": "Hiker Michael", "type": "Trainer Scaling", "data_ids": ["HIKER_MICHAEL"]},
            {"name": "Hiker Parry", "type": "Trainer Scaling", "data_ids": ["HIKER_PARRY_1"]},
            {"name": "Hiker Timothy", "type": "Trainer Scaling", "data_ids": ["HIKER_TIMOTHY"]},
            {"name": "Cool Trainer Ryan", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_RYAN"]},
            {"name": "Cool Trainer Kelly", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_KELLY"]},
            {"name": "Camper Quentin", "type": "Trainer Scaling", "data_ids": ["CAMPER_QUENTIN"]}
        ],
        "REGION_ROUTE_46": [
            {"name": "Camper Ted", "type": "Trainer Scaling", "data_ids": ["CAMPER_TED"]},
            {"name": "Picnicker Erin", "type": "Trainer Scaling", "data_ids": ["PICNICKER_ERIN_1"]},
            {"name": "Hiker Bailey", "type": "Trainer Scaling", "data_ids": ["HIKER_BAILEY"]}
        ],
        "REGION_ROUTE_27:CENTER": [
            {"name": "Cool Trainer Megan", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_MEGAN"]}
        ],
        "REGION_ROUTE_27:EAST": [
            {"name": "Psychic Gilbert", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_GILBERT"]},
            {"name": "Cool Trainer Blake", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_BLAKE"]},
            {"name": "Cool Trainer Brian", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_BRIAN"]},
            {"name": "Cool Trainer Reena", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_REENA_1"]}
        ],
        "REGION_ROUTE_27:EASTWHIRLPOOL": [
            {"name": "Bird Keeper Jose", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_JOSE_1"]}
        ],
        "REGION_ROUTE_26": [
            {"name": "Cool Trainer Jake", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_JAKE"]},
            {"name": "Cool Trainer Gaven", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_GAVEN"]},
            {"name": "Cool Trainer Joyce", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_JOYCE"]},
            {"name": "Cool Trainer Beth", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_BETH"]},
            {"name": "Psychic Richard", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_RICHARD"]},
            {"name": "Fisher Scott", "type": "Trainer Scaling", "data_ids": ["FISHER_SCOTT"]}
        ],
        "REGION_VICTORY_ROAD": [
            {"name": "Victory Road Rival", "type": "Trainer Scaling", "data_ids": ["RIVAL_VROAD_MEGANIUM", "RIVAL_VROAD_TYPHLOSION", "RIVAL_VROAD_FERALIGATR"]}
        ],
        "REGION_INDIGO_PLATEAU_POKECENTER_1F": [
            {"name": "Indigo Plateau Rival", "type": "Trainer Scaling", "data_ids": ["EVENT_INDIGO_PLATEAU_POKECENTER_RIVAL"]},
            {
                "name": "Pokemon League",
                "type": "Trainer Scaling",
                "connections": [
                    "REGION_WILLS_ROOM",
                    "REGION_KOGAS_ROOM",
                    "REGION_BRUNOS_ROOM",
                    "REGION_KARENS_ROOM",
                    "REGION_LANCES_ROOM"
                ],
                "data_ids": [
                    "ELITE_FOUR_WILL",
                    "ELITE_FOUR_KOGA",
                    "ELITE_FOUR_BRUNO",
                    "ELITE_FOUR_KAREN",
                    "CHAMPION_LANCE"
                ]
            }
        ],
        "REGION_WILLS_ROOM": [
            {"name": "Elite Four Will", "type": "Trainer Scaling", "data_ids": ["ELITE_FOUR_WILL"]}
        ],
        "REGION_KOGAS_ROOM": [
            {"name": "Elite Four Koga", "type": "Trainer Scaling", "data_ids": ["ELITE_FOUR_KOGA"]}
        ],
        "REGION_BRUNOS_ROOM": [
            {"name": "Elite Four Bruno", "type": "Trainer Scaling", "data_ids": ["ELITE_FOUR_BRUNO"]},
        ],
        "REGION_KARENS_ROOM": [
            {"name": "Elite Four Karen", "type": "Trainer Scaling", "data_ids": ["ELITE_FOUR_KAREN"]},
        ],
        "REGION_LANCES_ROOM": [
            {"name": "Champion Lance", "type": "Trainer Scaling", "data_ids": ["CHAMPION_LANCE"]}
        ]
    }

    mt_silver_trainer_data = {
        "REGION_SILVER_CAVE_ROOM_3": [
            {"name": "PKMN Trainer Red", "type": "Trainer Scaling", "data_ids": ["EVENT_BEAT_RED"]}
        ]
    }

    # SS Aqua is part of Kanto, since SS Ticket doesn't exist in Johto Only.
    kanto_trainer_data = {
        "REGION_FAST_SHIP_B1F": [
            {"name": "Sailor Garrett", "type": "Trainer Scaling", "data_ids": ["SAILOR_GARRETT"]},
            {"name": "Fisher Jonah", "type": "Trainer Scaling", "data_ids": ["FISHER_JONAH"]},
            {"name": "Blackbelt Wai", "type": "Trainer Scaling", "data_ids": ["BLACKBELT_WAI"]},
            {"name": "Sailor Kenneth", "type": "Trainer Scaling", "data_ids": ["SAILOR_KENNETH"]},
            {"name": "Teacher Shirley", "type": "Trainer Scaling", "data_ids": ["TEACHER_SHIRLEY"]},
            {"name": "School Boy Nate", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_NATE"]},
            {"name": "School Boy Ricky", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_RICKY"]}
        ],
        "REGION_FAST_SHIP_CABINS_NNW_NNE_NE": [
            {"name": "Cool Trainer Sean", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_SEAN"]},
            {"name": "Cool Trainer Carol", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_CAROL"]},
            {"name": "Poke Maniac Ethan", "type": "Trainer Scaling", "data_ids": ["POKEMANIAC_ETHAN"]},
            {"name": "Gentleman Edward", "type": "Trainer Scaling", "data_ids": ["GENTLEMAN_EDWARD"]},
            {"name": "Burglar Corey", "type": "Trainer Scaling", "data_ids": ["BURGLAR_COREY"]}
        ],
        "REGION_FAST_SHIP_CABINS_SE_SSE_CAPTAINS_CABIN": [
            {"name": "Psychic Rodney", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_RODNEY"]},
            {"name": "Poke Fan Jeremy", "type": "Trainer Scaling", "data_ids": ["POKEFANM_JEREMY"]},
            {"name": "Poke Fan Georgia", "type": "Trainer Scaling", "data_ids": ["POKEFANF_GEORGIA"]},
            {"name": "Super Nerd Shawn", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_SHAWN"]}
        ],
        "REGION_FAST_SHIP_CABINS_SW_SSW_NW": [
            {"name": "Bug Catcher Ken", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_KEN"]},
            {"name": "Beauty Cassie", "type": "Trainer Scaling", "data_ids": ["BEAUTY_CASSIE"]},
            {"name": "Guitarist Clyde", "type": "Trainer Scaling", "data_ids": ["GUITARIST_CLYDE"]}
        ],
        "REGION_VERMILION_GYM": [
            {"name": "Leader Lt. Surge", "type": "Trainer Scaling", "data_ids": ["LEADER_LT_SURGE"]},
            {"name": "Gentleman Gregory", "type": "Trainer Scaling", "data_ids": ["GENTLEMAN_GREGORY"]},
            {"name": "Guitarist Vincent", "type": "Trainer Scaling", "data_ids": ["GUITARIST_VINCENT"]},
            {"name": "Juggler Horton", "type": "Trainer Scaling", "data_ids": ["JUGGLER_HORTON"]}
        ],
        "REGION_ROUTE_6": [
            {"name": "Poke Fan Rex", "type": "Trainer Scaling", "data_ids": ["POKEFANM_REX"]},
            {"name": "Poke Fan Allan", "type": "Trainer Scaling", "data_ids": ["POKEFANM_ALLAN"]}
        ],
        "REGION_SAFFRON_GYM": [
            {"name": "Medium Rebecca", "type": "Trainer Scaling", "data_ids": ["MEDIUM_REBECCA"]},
            {"name": "Psychic Franklin", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_FRANKLIN"]},
            {"name": "Medium Doris", "type": "Trainer Scaling", "data_ids": ["MEDIUM_DORIS"]},
            {"name": "Psychic Jared", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_JARED"]},
            {"name": "Leader Sabrina", "type": "Trainer Scaling", "data_ids": ["LEADER_SABRINA"]}
        ],
        "REGION_ROUTE_25": [
            {"name": "School Boy Dudley", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_DUDLEY"]},
            {"name": "Lass Ellen", "type": "Trainer Scaling", "data_ids": ["LASS_ELLEN"]},
            {"name": "School Boy Joe", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_JOE"]},
            {"name": "Lass Laura", "type": "Trainer Scaling", "data_ids": ["LASS_LAURA"]},
            {"name": "Camper Lloyd", "type": "Trainer Scaling", "data_ids": ["CAMPER_LLOYD"]},
            {"name": "Lass Shannon", "type": "Trainer Scaling", "data_ids": ["LASS_SHANNON"]},
            {"name": "Super Nerd Pat", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_PAT"]},
            {"name": "Cool Trainer Kevin", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERM_KEVIN"]}
        ],
        "REGION_ROUTE_9": [
            {"name": "Camper Dean", "type": "Trainer Scaling", "data_ids": ["CAMPER_DEAN"]},
            {"name": "Picnicker Heidi", "type": "Trainer Scaling", "data_ids": ["PICNICKER_HEIDI"]},
            {"name": "Camper Sid", "type": "Trainer Scaling", "data_ids": ["CAMPER_SID"]},
            {"name": "Picnicker Edna", "type": "Trainer Scaling", "data_ids": ["PICNICKER_EDNA"]},
            {"name": "Hiker Tim", "type": "Trainer Scaling", "data_ids": ["HIKER_TIM"]},
            {"name": "Hiker Sidney", "type": "Trainer Scaling", "data_ids": ["HIKER_SIDNEY"]}
        ],
        "REGION_ROUTE_8": [
            {"name": "Biker Dwayne", "type": "Trainer Scaling", "data_ids": ["BIKER_DWAYNE"]},
            {"name": "Biker Zeke", "type": "Trainer Scaling", "data_ids": ["BIKER_ZEKE"]},
            {"name": "Biker Harris", "type": "Trainer Scaling", "data_ids": ["BIKER_HARRIS"]},
            {"name": "Super Nerd Sam", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_SAM"]},
            {"name": "Super Nerd Tom", "type": "Trainer Scaling", "data_ids": ["SUPER_NERD_TOM"]}
        ],
        "REGION_ROUTE_10_SOUTH": [
            {"name": "Poke Fan Robert", "type": "Trainer Scaling", "data_ids": ["POKEFANM_ROBERT"]},
            {"name": "Hiker Jim", "type": "Trainer Scaling", "data_ids": ["HIKER_JIM"]}
        ],
        "REGION_ROUTE_12": [
            {"name": "Fisher Kyle", "type": "Trainer Scaling", "data_ids": ["FISHER_KYLE"]},
            {"name": "Fisher Martin", "type": "Trainer Scaling", "data_ids": ["FISHER_MARTIN"]},
            {"name": "Fisher Stephen", "type": "Trainer Scaling", "data_ids": ["FISHER_STEPHEN"]},
            {"name": "Fisher Barney", "type": "Trainer Scaling", "data_ids": ["FISHER_BARNEY"]}
        ],
        "REGION_ROUTE_11": [
            {"name": "Youngster Owen", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_OWEN"]},
            {"name": "Youngster Jason", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_JASON"]},
            {"name": "Psychic Herman", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_HERMAN"]},
            {"name": "Psychic Fidel", "type": "Trainer Scaling", "data_ids": ["PSYCHIC_FIDEL"]}
        ],
        "REGION_CELEDON_GYM": [
            {"name": "Twins Jo And Zoe", "type": "Trainer Scaling", "data_ids": ["TWINS_JO_ZOE_1", "TWINS_JO_ZOE_2"]},
            {"name": "Picnicker Tanya", "type": "Trainer Scaling", "data_ids": ["PICNICKER_TANYA"]},
            {"name": "Lass Michelle", "type": "Trainer Scaling", "data_ids": ["LASS_MICHELLE"]},
            {"name": "Beauty Julia", "type": "Trainer Scaling", "data_ids": ["BEAUTY_JULIA"]},
            {"name": "Leader Erika", "type": "Trainer Scaling", "data_ids": ["LEADER_ERIKA"]}
        ],
        "REGION_ROUTE_17": [
            {"name": "Biker Charles", "type": "Trainer Scaling", "data_ids": ["BIKER_CHARLES"]},
            {"name": "Biker Riley", "type": "Trainer Scaling", "data_ids": ["BIKER_RILEY"]},
            {"name": "Biker Joel", "type": "Trainer Scaling", "data_ids": ["BIKER_JOEL"]},
            {"name": "Biker Glenn", "type": "Trainer Scaling", "data_ids": ["BIKER_GLENN"]}
        ],
        "REGION_ROUTE_18": [
            {"name": "Bird Keeper Boris", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_BORIS"]},
            {"name": "Bird Keeper Bob", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_BOB"]}
        ],
        "REGION_FUCHSIA_GYM": [
            {"name": "Lass Linda", "type": "Trainer Scaling", "data_ids": ["LASS_LINDA"]},
            {"name": "Picnicker Cindy", "type": "Trainer Scaling", "data_ids": ["PICNICKER_CINDY"]},
            {"name": "Camper Barry", "type": "Trainer Scaling", "data_ids": ["CAMPER_BARRY"]},
            {"name": "Lass Alice", "type": "Trainer Scaling", "data_ids": ["LASS_ALICE"]},
            {"name": "Leader Janine", "type": "Trainer Scaling", "data_ids": ["LEADER_JANINE"]}
        ],
        "REGION_ROUTE_15": [
            {"name": "Teacher Colette", "type": "Trainer Scaling", "data_ids": ["TEACHER_COLETTE"]},
            {"name": "Teacher Hillary", "type": "Trainer Scaling", "data_ids": ["TEACHER_HILLARY"]},
            {"name": "School Boy Kip", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_KIPP"]},
            {"name": "School Boy Tommy", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_TOMMY"]},
            {"name": "School Boy Johnny", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_JOHNNY"]},
            {"name": "School Boy Billy", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_BILLY"]}
        ],
        "REGION_ROUTE_14": [
            {"name": "Poke Fan Carter", "type": "Trainer Scaling", "data_ids": ["POKEFANM_CARTER"]},
            {"name": "Bird Keeper Roy", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_ROY"]},
            {"name": "Poke Fan Trevor", "type": "Trainer Scaling", "data_ids": ["POKEFANM_TREVOR"]}
        ],
        "REGION_ROUTE_13": [
            {"name": "Poke Fan Alex", "type": "Trainer Scaling", "data_ids": ["POKEFANM_ALEX"]},
            {"name": "Poke Fan Joshua", "type": "Trainer Scaling", "data_ids": ["POKEFANM_JOSHUA"]},
            {"name": "Bird Keeper Perry", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_PERRY"]},
            {"name": "Bird Keeper Bret", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_BRET"]},
            {"name": "Hiker Kenny", "type": "Trainer Scaling", "data_ids": ["HIKER_KENNY"]}
        ],
        "REGION_CERULEAN_GYM": [
            {"name": "Swimmer Parker", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_PARKER"]},
            {"name": "Swimmer Briana", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_BRIANA"]},
            {"name": "Swimmer Diana", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_DIANA"]},
            {"name": "Leader Misty", "type": "Trainer Scaling", "data_ids": ["LEADER_MISTY"]}
        ],
        "REGION_ROUTE_2:WEST": [
            {"name": "Bug Catcher Ed", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_ED"]},
            {"name": "Bug Catcher Rob", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_ROB"]},
            {"name": "Bug Catcher Doug", "type": "Trainer Scaling", "data_ids": ["BUG_CATCHER_DOUG"]}
        ],
        "REGION_PEWTER_GYM": [
            {"name": "Camper Jerry", "type": "Trainer Scaling", "data_ids": ["CAMPER_JERRY"]},
            {"name": "Leader Brock", "type": "Trainer Scaling", "data_ids": ["LEADER_BROCK"]}
        ],
        "REGION_ROUTE_3": [
            {"name": "Fire Breather Otis", "type": "Trainer Scaling", "data_ids": ["FIREBREATHER_OTIS"]},
            {"name": "Youngster Warren", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_WARREN"]},
            {"name": "Youngster Jimmy", "type": "Trainer Scaling", "data_ids": ["YOUNGSTER_JIMMY"]},
            {"name": "Fire Breather Burt", "type": "Trainer Scaling", "data_ids": ["FIREBREATHER_BURT"]}
        ],
        "REGION_MOUNT_MOON": [
            {"name": "Mt. Moon Rival", "type": "Trainer Scaling", "data_ids": ["RIVAL_MT_MOON_MEGANIUM", "RIVAL_MT_MOON_TYPHLOSION", "RIVAL_MT_MOON_FERALIGATR"]}
        ],
        "REGION_ROUTE_4": [
            {"name": "Bird Keeper Hank", "type": "Trainer Scaling", "data_ids": ["BIRD_KEEPER_HANK"]},
            {"name": "Picnicker Hope", "type": "Trainer Scaling", "data_ids": ["PICNICKER_HOPE"]},
            {"name": "Picnicker Sharon", "type": "Trainer Scaling", "data_ids": ["PICNICKER_SHARON"]}
        ],
        "REGION_ROUTE_1": [
            {"name": "School Boy Danny", "type": "Trainer Scaling", "data_ids": ["SCHOOLBOY_DANNY"]},
            {"name": "Cool Trainer Quinn", "type": "Trainer Scaling", "data_ids": ["COOLTRAINERF_QUINN"]}
        ],
        "REGION_ROUTE_21": [
            {"name": "Swimmer Seth", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_SETH"]},
            {"name": "Swimmer Nikki", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_NIKKI"]},
            {"name": "Fisher Arnold", "type": "Trainer Scaling", "data_ids": ["FISHER_ARNOLD"]}
        ],
        "REGION_ROUTE_20": [
            {"name": "Swimmer Nicole", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_NICOLE"]},
            {"name": "Swimmer Lori", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_LORI"]},
            {"name": "Swimmer Cameron", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_CAMERON"]}
        ],
        "REGION_SEAFOAM_GYM": [
            {"name": "Leader Blaine", "type": "Trainer Scaling", "data_ids": ["LEADER_BLAINE"]}
        ],
        "REGION_ROUTE_19": [
            {"name": "Swimmer Dawn", "type": "Trainer Scaling", "data_ids": ["SWIMMERF_DAWN"]},
            {"name": "Swimmer Harold", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_HAROLD"]},
            {"name": "Swimmer Jerome", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_JEROME"]},
            {"name": "Swimmer Tucker", "type": "Trainer Scaling", "data_ids": ["SWIMMERM_TUCKER"]}
        ],
        "REGION_VIRIDIAN_GYM": [
            {"name": "Leader Blue", "type": "Trainer Scaling", "data_ids": ["LEADER_BLUE"]}
        ]
    }

    johto_wild_encounter_data = {
        "Route 29 Land Encounters": [
            {
                "name": "Route 29 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_29"
                ]
            }
        ],
        "Route 30 Land Encounters": [
            {
                "name": "Route 30 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_30"
                ]
            }
        ],
        "Route 30 Water Encounters": [
            {
                "name": "Route 30 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_30"
                ]
            }
        ],
        "Route 31 Land Encounters": [
            {
                "name": "Route 31 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_31"
                ]
            }
        ],
        "Route 31 Water Encounters": [
            {
                "name": "Route 31 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_31"
                ]
            }
        ],
        "Route 32 Land Encounters": [
            {
                "name": "Route 32 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_32"
                ]
            }
        ],
        "Route 32 Water Encounters": [
            {
                "name": "Route 32 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_32"
                ]
            }
        ],
        "Route 33 Land Encounters": [
            {
                "name": "Route 33 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_33"
                ]
            }
        ],
        "Route 34 Land Encounters": [
            {
                "name": "Route 34 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_34"
                ]
            }
        ],
        "Route 34 Water Encounters": [
            {
                "name": "Route 34 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_34"
                ]
            }
        ],
        "Route 35 Land Encounters": [
            {
                "name": "Route 35 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_35"
                ]
            }
        ],
        "Route 35 Water Encounters": [
            {
                "name": "Route 35 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_35"
                ]
            }
        ],
        "Route 36 Land Encounters": [
            {
                "name": "Route 36 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_36"
                ]
            }
        ],
        "Route 37 Land Encounters": [
            {
                "name": "Route 37 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_37"
                ]
            }
        ],
        "Route 38 Land Encounters": [
            {
                "name": "Route 38 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_38"
                ]
            }
        ],
        "Route 39 Land Encounters": [
            {
                "name": "Route 39 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_39"
                ]
            }
        ],
        "Route 40 Water Encounters": [
            {
                "name": "Route 40 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_40"
                ]
            }
        ],
        "Route 41 Water Encounters": [
            {
                "name": "Route 41 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_41"
                ]
            }
        ],
        "Route 42 Land Encounters": [
            {
                "name": "Route 42 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_42"
                ]
            }
        ],
        "Route 42 Water Encounters": [
            {
                "name": "Route 42 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_42"
                ]
            }
        ],
        "Route 43 Land Encounters": [
            {
                "name": "Route 43 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_43"
                ]
            }
        ],
        "Route 43 Water Encounters": [
            {
                "name": "Route 43 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_43"
                ]
            }
        ],
        "Route 44 Land Encounters": [
            {
                "name": "Route 44 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_44"
                ]
            }
        ],
        "Route 44 Water Encounters": [
            {
                "name": "Route 44 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_44"
                ]
            }
        ],
        "Route 45 Land Encounters": [
            {
                "name": "Route 45 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_45"
                ]
            }
        ],
        "Route 45 Water Encounters": [
            {
                "name": "Route 45 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_45"
                ]
            }
        ],
        "Route 46 Land Encounters": [
            {
                "name": "Route 46 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_46"
                ]
            }
        ],
        "Route 26 Land Encounters": [
            {
                "name": "Route 26 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_26"
                ]
            }
        ],
        "Route 26 Water Encounters": [
            {
                "name": "Route 26 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_26"
                ]
            }
        ],
        "Route 27 Land Encounters": [
            {
                "name": "Route 27 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_27"
                ]
            }
        ],
        "Route 27 Water Encounters": [
            {
                "name": "Route 27 Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ROUTE_27"
                ]
            }
        ],
        "Sprout Tower 2F Land Encounters": [
            {
                "name": "Sprout Tower 2F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "SPROUT_TOWER_2F"
                ]
            }
        ],
        "Sprout Tower 3F Land Encounters": [
            {
                "name": "Sprout Tower 3F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "SPROUT_TOWER_3F"
                ]
            }
        ],
        "Tin Tower 2F Land Encounters": [
            {
                "name": "Tin Tower 2F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_2F"
                ]
            }
        ],
        "Tin Tower 3F Land Encounters": [
            {
                "name": "Tin Tower 3F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_3F"
                ]
            }
        ],
        "Tin Tower 4F Land Encounters": [
            {
                "name": "Tin Tower 4F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_4F"
                ]
            }
        ],
        "Tin Tower 5F Land Encounters": [
            {
                "name": "Tin Towerr 5F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_5F"
                ]
            }
        ],
        "Tin Tower 6F Land Encounters": [
            {
                "name": "Tin Tower 6F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_6F"
                ]
            }
        ],
        "Tin Tower 7F Land Encounters": [
            {
                "name": "Tin Tower 7F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_7F"
                ]
            }
        ],
        "Tin Tower 8F Land Encounters": [
            {
                "name": "Tin Tower 8F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_8F"
                ]
            }
        ],
        "Tin Tower 9F Land Encounters": [
            {
                "name": "Tin Tower 9F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TIN_TOWER_9F"
                ]
            }
        ],
        "Burned Tower 1F Land Encounters": [
            {
                "name": "Burned Tower 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "BURNED_TOWER_1F"
                ]
            }
        ],
        "Burned Tower B1F Land Encounters": [
            {
                "name": "Burned Tower B1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "BURNED_TOWER_B1F"
                ]
            }
        ],
        "National Park Land Encounters": [
            {
                "name": "National Park Land Scaling",
                "type": "grass",
                "data_ids": [
                    "NATIONAL_PARK"
                ]
            }
        ],
        "Ruins of Alph Outside Land Encounters": [
            {
                "name": "Ruins of Alph Outside Land Scaling",
                "type": "grass",
                "data_ids": [
                    "RUINS_OF_ALPH_OUTSIDE"
                ]
            }
        ],
        "Ruins of Alph Outside Water Encounters": [
            {
                "name": "Ruins of Alph Outside Water Scaling",
                "type": "grass",
                "data_ids": [
                    "RUINS_OF_ALPH_OUTSIDE"
                ]
            }
        ],
        "Ruins of Alph Inner Chamber Land Encounters": [
            {
                "name": "Ruins of Alph Inner Chamber Land Scaling",
                "type": "grass",
                "data_ids": [
                    "RUINS_OF_ALPH_INNER_CHAMBER"
                ]
            }
        ],
        "Union Cave 1F Land Encounters": [
            {
                "name": "Union Cave 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                        "UNION_CAVE_1F"
                    ]
            }
        ],
        "Union Cave 1F Water Encounters": [
            {
                "name": "Union Cave 1F Water Scaling",
                "type": "grass",
                "data_ids": [
                    "UNION_CAVE_1F"
                ]
            }
        ],
        "Union Cave B1F Land Encounters": [
            {
                "name": "Union Cave B1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "UNION_CAVE_B1F"
                ]
            }
        ],
        "Union Cave B1F Water Encounters": [
            {
                "name": "Union Cave B1F Water Scaling",
                "type": "grass",
                "data_ids": [
                    "UNION_CAVE_B1F"
                ]
            }
        ],
        "Union Cave B2F Land Encounters": [
            {
                "name": "Union Cave B2F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "UNION_CAVE_B2F"
                ]
            }
        ],
        "Union Cave B2F Water Encounters": [
            {
                "name": "Union Cave B2F Water Scaling",
                "type": "grass",
                "data_ids": [
                    "UNION_CAVE_B2F"
                ]
            }
        ],
        "Slowpoke Well B1F Land Encounters": [
            {
                "name": "Slowpoke Well B1f Land Scaling",
                "type": "grass",
                "data_ids": [
                    "SLOWPOKE_WELL_B1F"
                ]
            }
        ],
        "Slowpoke Well B1F Water Encounters": [
            {
                "name": "Slowpoke Well B1F Water Scaling",
                "type": "grass",
                "data_ids": [
                    "SLOWPOKE_WELL_B1F"
                ]
            }
        ],
        "Slowpoke Well B2F Land Encounters": [
            {
                "name": "Slowpoke Well B2F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "SLOWPOKE_WELL_B2F"
                ]
            }
        ],
        "Slowpoke Well B2F Water Encounters": [
            {
                "name": "Slowpoke Well B2F Water Scaling",
                "type": "grass",
                "data_ids": [
                    "SLOWPOKE_WELL_B2F"
                ]
            }
        ],
        "Ilex Forest Land Encounters": [
            {
                "name": "Ilex Forest Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ILEX_FOREST"
                ]
            }
        ],
        "Ilex Forest Water Encounters": [
            {
                "name": "Ilex Forest Water Scaling",
                "type": "grass",
                "data_ids": [
                    "ILEX_FOREST:NORTH"
                ]
            }
        ],
        "Mt. Mortar 1F Outside Land Encounters": [
            {
                "name": "Mt. Mortar 1F Outside Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MOUNT_MORTAR_1F_OUTSIDE"
                ]
            }
        ],
        "Mt. Mortar 1F Outised Water Encounters": [
            {
                "name": "Mt. Mortar 1F Outside Water Scaling",
                "type": "grass",
                "data_ids": [
                    "MOUNT_MORTAR_1F_OUTSIDE"
                ]
            }
        ],
        "Mt. Mortar 1F Inside Land Encounters": [
            {
                "name": "Mt. Mortar 1F Inside Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MOUNT_MORTAR_1F_INSIDE"
                ]
            }
        ],
        "Mt. Mortar 2F Inside Land Encounters": [
            {
                "name": "Mt. Mortar 2F Inside Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MOUNT_MORTAR_2F_INSIDE"
                ]
            }
        ],
        "Mt. Mortar 2F Inside Water Encounters": [
            {
                "name": "Mt. Mortar 2F Inside Water Scaling",
                "type": "grass",
                "data_ids": [
                    "MOUNT_MORTAR_2F_INSIDE"
                ]
            }
        ],
        "Mt. Mortar B1F Land Encounters": [
            {
                "name": "Mt. Mortar B1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MOUNT_MORTAR_B1F"
                ]
            }
        ],
        "Mt. Mortar B1F Water Encounters": [
            {
                "name": "Mt. Mortar B1F Water Scaling",
                "type": "grass",
                "data_ids": [
                    "MOUNT_MORTAR_B1F"
                ]
            }
        ],
        "Ice Path 1F Land Encounters": [
            {
                "name": "Ice Path 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ICE_PATH_1F"
                ]
            }
        ],
        "Ice Path B1F Land Encounters": [
            {
                "name": "Ice Path B1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ICE_PATH_B1F"
                ]
            }
        ],
        "Ice Path B2F Mahogany Side Land Encounters": [
            {
                "name": "Ice Path B2F Mahogany Side Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ICE_PATH_B2F_MAHOGANY_SIDE"
                ]
            }
        ],
        "Ice Path B2F Blackthorn Side Land Encounters": [
            {
                "name": "Ice Path B2F Blackthorn Side Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ICE_PATH_B2F_BLACKTHORN_SIDE"
                ]
            }
        ],
        "Ice Path B3F Land Encounters": [
            {
                "name": "Ice Path B3F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "ICE_PATH_B3F"
                ]
            }
        ],
        "Whirl Island NW Land Encounters": [
            {
                "name": "Whirl Island NW Land Scaling",
                "type": "grass",
                "data_ids": [
                    "WHIRL_ISLAND_NW"
                ]
            }
        ],
        "Whirl Island NE Land Encounters": [
            {
                "name": "Whirl Island NE Land Scaling",
                "type": "grass",
                "data_ids": [
                    "WHIRL_ISLAND_NE"
                ]
            }
        ],
        "Whirl Island SW Water Encounters": [
            {
                "name": "Whirl Island SW Water Scaling",
                "type": "water",
                "data_ids": [
                    "WHIRL_ISLAND_SW"
                ]
            }
        ],
        "Whirl Island B2F Water Encounters": [
            {
                "name": "Whirl Island B2F Water Scaling",
                "type": "water",
                "data_ids": [
                    "WHIRL_ISLAND_B2F"
                ]
            }
        ],
        "Whirl Island Lugia Chamber Land Encounters": [
            {
                "name": "Whirl Island Lugia Chamber Land Scaling",
                "type": "grass",
                "data_ids": [
                    "WHIRL_ISLAND_LUGIA_CHAMBER"
                ]
            }
        ],
        "Whirl Island Lugia Chamber Water Encounters": [
            {
                "name": "Whirl Island Lugia Chamber Water Scaling",
                "type": "water",
                "data_ids": [
                    "WHIRL_ISLAND_LUGIA_CHAMBER"
                ]
            }
        ],
        "Dark Cave Violet Land Encounters": [
            {
                "name": "Dark Cave Violet Land Scaling",
                "type": "grass",
                "data_ids": [
                    "DARK_CAVE_VIOLET"
                ]
            }
        ],
        "Dark Cave Violet Water Encounters": [
            {
                "name": "Dark Cave Violet Water Scaling",
                "type": "water",
                "data_ids": [
                    "DARK_CAVE_VIOLET"
                ]
            }
        ],
        "Dark Cave Blackthorn Land Encounters": [
            {
                "name": "Dark Cave Blackthorn Land Scaling",
                "type": "grass",
                "data_ids": [
                    "DARK_CAVE_BLACKTHORN"
                ]
            }
        ],
        "Dark Cave Blackthorn Water Encounters": [
            {
                "name": "Dark Cave Blackthorn Scaling",
                "type": "water",
                "data_ids": [
                    "DARK_CAVE_BLACKTHORN"
                ]
            }
        ],
        "Dragon's Den B1F Water Encounters": [
            {
                "name": "Dragon's Den B1F Water Scaling",
                "type": "water",
                "data_ids": [
                    "DRAGONS_DEN_B1F"
                ]
            }
        ],
        "Victory Road Land Encounters": [
            {
                "name": "Victory Road Land Scaling",
                "type": "grass",
                "data_ids": [
                    "VICTORY_ROAD"
                ]
            }
        ],
        "Tohjo Falls Land Encounters": [
            {
                "name": "Tohjo Falls Land Scaling",
                "type": "grass",
                "data_ids": [
                    "TOHJO_FALLS"
                ]
            }
        ],
        "Tohjo Falls Water Encounters": [
            {
                "name": "Tohjo Falls Water Scaling",
                "type": "water",
                "data_ids": [
                    "TOHJO_FALLS"
                ]
            }
        ],
        "New Bark Town Water Encounters": [
            {
                "name": "New Bark Town Water Scaling",
                "type": "water",
                "data_ids": [
                    "NEW_BARK_TOWN"
                ]
            }
        ],
        "Cherrygrove City Water Encounters": [
            {
                "name": "Cherrygrove City Water Scaling",
                "type": "water",
                "data_ids": [
                    "CHERRYGROVE_CITY"
                ]
            }
        ],
        "Violet City Water Encounters": [
            {
                "name": "Violet City Water Scaling",
                "type": "water",
                "data_ids": [
                    "VIOLET_CITY"
                ]
            }
        ],
        "Ecruteak City Water Encounters": [
            {
                "name": "Ecruteak City Water Scaling",
                "type": "water",
                "data_ids": [
                    "ECRUTEAK_CITY"
                ]
            }
        ],
        "Olivine City Water Encounters": [
            {
                "name": "Olivine City Water Scaling",
                "type": "water",
                "data_ids": [
                    "OLIVINE_CITY"
                ]
            }
        ],
        "Olivine Port Water Encounters": [
            {
                "name": "Olivine Port Water Scaling",
                "type": "grass",
                "data_ids": [
                    "OLIVINE_PORT"
                ]
            }
        ],
        "Cianwood City Water Encounters": [
            {
                "name": "Cianwood City Water Scaling",
                "type": "water",
                "data_ids": [
                    "CIANWOOD_CITY"
                ]
            }
        ],
        "Lake of Rage Water Encounters": [
            {
                "name": "Lake of Rage Water Scaling",
                "type": "water",
                "data_ids": [
                    "LAKE_OF_RAGE"
                ]
            }
        ],
        "Blackthorn City Water Encounters": [
            {
                "name": "Blackthorn City Water Scaling",
                "type": "water",
                "data_ids": [
                    "BLACKTHORN_CITY"
                ]
            }
        ],
        "Fishing Encounters": [
            {
                "name": "Fishing Scaling",
                "type": "fish",
                "connections": [
                    "Route 30 Fishing Encounters",
                    "Route 31 Fishing Encounters",
                    "Route 32 Fishing Encounters",
                    "Route 34 Fishing Encounters",
                    "Route 35 Fishing Encounters",
                    "Route 40 Fishing Encounters",
                    "Route 41 Fishing Encounters",
                    "Route 42 Fishing Encounters",
                    "Route 43 Fishing Encounters",
                    "Route 44 Fishing Encounters",
                    "Route 45 Fishing Encounters",
                    "Route 26 Fishing Encounters",
                    "Route 27 Fishing Encounters",
                    "Dark Cave Violet Fishing Encounters",
                    "Dark Cave Blackthorn Fishing Encounters",
                    "Union Cave 1F Fishing Encounters",
                    "Union Cave B1F Fishing Encounters",
                    "Union Cave B2F Fishing Encounters",
                    "Slowpoke Well B1F Fishing Encounters",
                    "Slowpoke Well B2F Fishing Encounters",
                    "Ilex Forest North Fishing Encounters",
                    "Whirl Islands NE Fishing Encounters",
                    " Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters",
                    "Slowpoke Fishing Encounters"
                ],
                "data_ids": [
                    ""
                ]
            }
        ]
    }

    kanto_wild_encounter_data = {
        "Route 1 Land Encounters": [
        {
            "name": "Route 1 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_1"
            ]
        }
    ],
        "Route 2 Land Encounters": [
        {
            "name": "Route 2 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_2"
            ]
        }
    ],
        "Route 3 Land Encounters": [
        {
            "name": "Route 3 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_3"
            ]
        }
    ],
        "Route 4 Land Encounters": [
        {
            "name": "Route 4 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_4"
            ]
        }
    ],
        "Route 4 Water Encounters": [
        {
            "name": "Route 4 Water Scaling",
            "type": "water",
            "data_ids": [
                "region_route_4"
            ]
        }
    ],
        "Route 5 Land Encounters": [
        {
            "name": "Route 5 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_5"
            ]
        }
    ],
        "Route 6 Land Encounters": [
            {
                "name": "Route 6 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "region_route_6"
                ]
            }
        ],
        "Route 6 Water Encounters": [
        {
            "name": "Route 6 Water Scaling",
            "type": "water",
            "data_ids": [
                "region_route_6"
            ]
        }
    ],
        "Route 7 Land Encounters": [
        {
            "name": "Route 7 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_7"
            ]
        }
    ],
        "Route 8 Land Encounters": [
        {
            "name": "Route 8 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_8"
            ]
        }
    ],
        "Route 9 Land Encounters": [
        {
            "name": "Route 9 Land Scaling",
            "type": "grass",
            "data_ids": [
                "region_route_9"
            ]
        }
    ],
        "Route 10 Land Encounters": [
            {
                "name": "Route 10 Land Scaling",
                "type": "grass",
                "data_ids": [
                    "region_route_10"
                ]
            }
        ],
        "Route 10 Water Encounters": [
        {
            "name": "Route 11 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE11"
            ]
        }
    ],
        "Route 11 Land Encounters": [
        {
            "name": "Diglett's Cave B1F Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_DIGLETTS_CAVE_B1F"
            ]
        }
    ],
        "Route 12 Land Encounters": [
        {
            "name": "Route 9 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE9"
            ]
        }
    ],
        "Route 12 Water Encounters": [
            {
                "name": "Icefall Cave 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F"
                ]
            }
        ],
        "Route 13 Land Encounters": [
        {
            "name": "Route 10 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE10"
            ]
        }
    ],
        "Route 13 Water Encounters": [
            {
                "name": "Icefall Cave 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F"
                ]
            }
        ],
        "Route 14 Land Encounters": [
        {
            "name": "Rock Tunnel 1F Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROCK_TUNNEL_1F"
            ]
        }
    ],
        "Route 15 Land Encounters": [
        {
            "name": "Rock Tunnel B1F Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROCK_TUNNEL_B1F"
            ]
        }
    ],
        "Route 16 Land Encounters": [
        {
            "name": "Route 8 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE8"
            ]
        }
    ],
        "Route 17 Land Encounters": [
        {
            "name": "Route 7 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE7"
            ]
        }
    ],
        "Route 18 Land Encounters": [
        {
            "name": "Route 12 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE12"
            ]
        }
    ],
        "Route 19 Water Encounters": [
            {
                "name": "Icefall Cave 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F"
                ]
            }
        ],
        "Route 20 Water Encounters": [
        {
            "name": "Route 13 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE13"
            ]
        }
    ],
        "Route 21 Land Encounters": [
            {
                "name": "Icefall Cave 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F"
                ]
            }
        ],
        "Route 21 Water Encounters": [
        {
            "name": "Route 14 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE14"
            ]
        }
    ],
        "Route 22 Land Encounters": [
        {
            "name": "Route 15 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE15"
            ]
        }
    ],
        "Route 22 Water Encounters": [
        {
            "name": "Route 16 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE16"
            ]
        }
    ],
        "Mt. Moon Land Encounters": [
        {
            "name": "Route 17 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE17"
            ]
        }
    ],
        "Pallet Town Water Encounters": [
        {
            "name": "Route 18 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE18"
            ]
        }
    ],
        "Viridian City Water Encounters": [
        {
            "name": "Route 21 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE21_NORTH",
                "MAP_ROUTE21_SOUTH"
            ]
        }
    ],
        "Cerulean City Water Encounters": [
        {
            "name": "Route 23 Land Scaling",
            "type": "grass",
            "data_ids": [
                "MAP_ROUTE23"
            ]
        }
    ],
        "Vermilion City Water Encounters": [
        {
            "name": "Pallet/Cinnabar/Rt 19,20,21 Water Scaling",
            "type": "water",
            "connections": [
                "Pallet Town Water Encounters",
                "Cinnabar Island Water Encounters",
                "Route 19 Water Encounters",
                "Route 20 Water Encounters",
                "Route 21 Water Encounters"
            ],
            "data_ids": [
                "MAP_PALLET_TOWN",
                "MAP_CINNABAR_ISLAND",
                "MAP_ROUTE19",
                "MAP_ROUTE20",
                "MAP_ROUTE21_NORTH",
                "MAP_ROUTE21_SOUTH"
            ]
        }
    ],
        "Vermilion Port Water Encounters": [
        {
            "name": "Viridian/Rt 22 Water Scaling",
            "type": "water",
            "connections": [
                "Viridian City Water Encounters",
                "Route 22 Water Encounters"
            ],
            "data_ids": [
                "MAP_VIRIDIAN_CITY",
                "MAP_ROUTE22"
            ]
        }
    ],
        "Celadon City Water Encounters": [
        {
            "name": "Cerulean/Rt 4,24 Water Scaling",
            "type": "water",
            "connections": [
                "Cerulean City Water Encounters",
                "Route 4 Water Encounters",
                "Route 24 Water Encounters"
            ],
            "data_ids": [
                "MAP_CERULEAN_CITY",
                "MAP_ROUTE4",
                "MAP_ROUTE24"
            ]
        }
    ],
        "Fuchsia City Water Encounters": [
        {
            "name": "Route 25 Water Scaling",
            "type": "water",
            "data_ids": [
                "MAP_ROUTE25"
            ]
        }
    ],
        "Cinnabar Island Water Encounters": [
        {
            "name": "Route 6 Water Scaling",
            "type": "water",
            "data_ids": [
                "MAP_ROUTE6"
            ]
        }
    ],
        "Fishing Encounters": [
        {
            "name": "Fishing Scaling",
            "type": "fish",
            "connections": [
                "Pallet Town Fishing Encounters",
                "Viridian City Fishing Encounters",
                "Cerulean City Fishing Encounters",
                "Vermilion City Fishing Encounters",
                "Celadon City Fishing Encounters",
                "Fuchsia City Fishing Encounters",
                "Cinnabar Island Fishing Encounters",
                "S.S. Anne Exterior Fishing Encounters",
                "Safari Zone Center Area Fishing Encounters",
                "Safari Zone East Area Fishing Encounters",
                "Safari Zone North Area Fishing Encounters",
                "Safari Zone West Area Fishing Encounters",
                "Seafoam Islands B3F Fishing Encounters",
                "Seafoam Islands B4F Fishing Encounters",
                "Cerulean Cave 1F Fishing Encounters",
                "Cerulean Cave B1F Fishing Encounters",
                "Route 4 Fishing Encounters",
                "Route 6 Fishing Encounters",
                "Route 10 Fishing Encounters",
                "Route 11 Fishing Encounters",
                "Route 12 Fishing Encounters",
                "Route 13 Fishing Encounters",
                "Route 19 Fishing Encounters",
                "Route 20 Fishing Encounters",
                "Route 21 Fishing Encounters",
                "Route 22 Fishing Encounters",
                "Route 23 Fishing Encounters",
                "Route 24 Fishing Encounters",
                "Route 25 Fishing Encounters"
            ],
            "data_ids": [
                "MAP_PALLET_TOWN",
                "MAP_VIRIDIAN_CITY",
                "MAP_CERULEAN_CITY",
                "MAP_VERMILION_CITY",
                "MAP_CELADON_CITY",
                "MAP_FUCHSIA_CITY",
                "MAP_CINNABAR_ISLAND",
                "MAP_SSANNE_EXTERIOR",
                "MAP_SAFARI_ZONE_CENTER",
                "MAP_SAFARI_ZONE_EAST",
                "MAP_SAFARI_ZONE_NORTH",
                "MAP_SAFARI_ZONE_WEST",
                "MAP_SEAFOAM_ISLANDS_B3F",
                "MAP_SEAFOAM_ISLANDS_B4F",
                "MAP_CERULEAN_CAVE_1F",
                "MAP_CERULEAN_CAVE_B1F",
                "MAP_ROUTE4",
                "MAP_ROUTE6",
                "MAP_ROUTE10",
                "MAP_ROUTE11",
                "MAP_ROUTE12",
                "MAP_ROUTE13",
                "MAP_ROUTE19",
                "MAP_ROUTE20",
                "MAP_ROUTE21_NORTH",
                "MAP_ROUTE21_SOUTH",
                "MAP_ROUTE22",
                "MAP_ROUTE23",
                "MAP_ROUTE24",
                "MAP_ROUTE25"
            ]
        }
    ]
}

    mt_silver_wild_encounter_data = {
        "Route 28 Land Encounters": [
            {
                "name": "Treasure Beach Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_ONE_ISLAND_TREASURE_BEACH"
                ]
            }
        ],
        "Silver Cave Outside Land Encounters": [
            {
                "name": "Mt. Ember Summit Path 3F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_MT_EMBER_SUMMIT_PATH_3F"
                ]
            }
        ],
        "Silver Cave Outside Water Encounters": [
            {
                "name": "Mt. Ember Summit Path 3F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_MT_EMBER_SUMMIT_PATH_3F"
                ]
            }
        ],
        "Silver Cave Room 1 Land Encounters": [
            {
                "name": "Kindle Road Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_ONE_ISLAND_KINDLE_ROAD"
                ]
            }
        ],
        "Silver Cave Room 2 Land Encounters": [
            {
                "name": "Mt. Ember Exterior Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_MT_EMBER_EXTERIOR"
                ]
            }
        ],
        "Silver Cave Room 2 Water Encounters": [
            {
                "name": "Icefall Cave 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F"
                ]
            }
        ],
        "Silver Cave Room 3 Land Encounters": [
            {
                "name": "Mt. Ember Summit Path 1F Land Scaling",
                "type": "grass",
                "data_ids": [
                    "MAP_MT_EMBER_SUMMIT_PATH_1F"
                ]
            }
        ],
        "Silver Cave Item Rooms Land Encounters": [
            {
                "name": "NAME",
                "type": "grass",
                "data_ids": [
                    "DATA"
                ]
            }
        ],
    }

    # we are only grabbing the address that holds the level data.
    # and i'm not entirely sure this will work, but the pokemon randomization does so
    # let's hope.
    johto_static_encounter_data = {
        "REGION_UNION_CAVE_B2F": [
            {
                "name": "UnionCaveLapras",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_UnionCaveLapras_2"
                ]
            }
        ],
        "REGION_TEAM_ROCKET_HIDEOUT_B1F": [
            {
                "name": "RocketHQTrap1",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_RocketHQTrap_1_2"
                ]
            },
            {
                "name": "RocketHQTrap2",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_RocketHQTrap_2_2"
                ]
            },
            {
                "name": "RocketHQTrap3",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_RocketHQTrap_3_2"
                ]
            }
        ],
        "REGION_TEAM_ROCKET_HIDEOUT_B2F": [
            {
                "name": "RocketHQElectrode1",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_RocketHQElectrode_1_2"
                ]
            },
            {
                "name": "RocketHQElectrode2",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_RocketHQElectrode_2_2"
                ]
            },
            {
                "name": "RocketHQElectrode3",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_RocketHQElectrode_3_2"
                ]
            }
        ],
        "REGION_LAKE_OF_RAGE:WATER": [
            {
                "name": "RedGyarados",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_RedGyarados_2"
                ]
            }
        ],
        "REGION_TIN_TOWER_ROOF": [
            {
                "name": "Ho_Oh",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Ho_Oh_2"
                ]
            }
        ],
        "REGION_TIN_TOWER_1F": [
            {
                "name": "Suicune",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Suicune_2"
                ]
            }
        ],
        "REGION_WHIRL_ISLAND_LUGIA_CHAMBER": [
            {
                "name": "Lugia",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Lugia_2"
                ]
            }
        ],
        # Raikou and Entei share the same address for their level, so only one
        # of them needs to be listed here.
        "REGION_BURNED_TOWER_B1F": [
            {
                "name": "Raikou",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Roamer_Level"
                ]
            }
        ],
        "REGION_ROUTE_36": [
            {
                "name": "Sudowoodo",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Sudowoodo"
                ]
            }
        ],
        "REGION_ROUTE_35_GOLDENROD_GATE": [
            {
                "name": "Kenya",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Kenya"
                ]
            }
        ],
        "REGION_ILEX_FOREST:SOUTH": [
            {
                "name": "Celebi",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Celebi"
                ]
            }
        ],
        "REGION_BILLS_FAMILYS_HOUSE": [
            {
                "name": "Eevee",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Eevee"
                ]
            }
        ],
        "REGION_DRAGON_SHRINE": [
            {
                "name": "Dratini",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Dratini"
                ]
            }
        ],
        "REGION_MOUNT_MORTAR_B2F:BACK": [
            {
                "name": "Tyrogue",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Tyrogue"
                ]
            }
        ]
    }

    kanto_static_encounter_data = {
        "REGION_VERMILION_CITY": [
            {
                "name": "Snorlax",
                "type": "Static Scaling",
                "data_ids": [
                    "AP_Static_Snorlax_2"
                ]
            }
        ],
    }

    def create_scaling_data(region: str, data) -> ScalingData:
        scaling_data = ScalingData(
            data["name"],
            region,
            data["type"] if "type" in data else None,
            data["connections"] if "connections" in data else None,
            data["data_ids"]
        )
        return scaling_data

    def update_scaling_data(scaling_data: ScalingData, connections: List[str], data_ids: List[str]) -> None:
        scaling_data.connections.extend(connections)
        scaling_data.data_ids.extend(data_ids)

    for region, trainers in johto_trainer_data.items():
        for trainer in trainers:
            scaling_data = create_scaling_data(region, trainer)
            world.scaling_data.append(scaling_data)

#    for region, wild_encounters in johto_wild_encounter_data.items():
#        for wild_encounter in wild_encounters:
#            scaling_data = create_scaling_data(region, wild_encounter)
#            world.scaling_data.append(scaling_data)

    for region, static_encounters in johto_static_encounter_data.items():
        for static_encounter in static_encounters:
            scaling_data = create_scaling_data(region, static_encounter)
            world.scaling_data.append(scaling_data)

    # if johto only is not on, add mt. silver data
    if not world.options.johto_only == JohtoOnly.option_on:
        for region, trainers in mt_silver_trainer_data.items():
            for trainer in trainers:
                scaling_data = next((data for data in world.scaling_data if data.name == trainer["name"]), None)
                if scaling_data is not None:
                    update_scaling_data(scaling_data, trainer["connections"], trainer["data_ids"])
                else:
                    scaling_data = create_scaling_data(region, trainer)
                    world.scaling_data.append(scaling_data)

#        for region, wild_encounters in mt_silver_wild_encounter_data.items():
#            for wild_encounter in wild_encounters:
#                scaling_data = next((data for data in world.scaling_data if data.name == wild_encounter["name"]), None)
#                if scaling_data is not None:
#                    update_scaling_data(scaling_data, wild_encounter["connections"], wild_encounter["data_ids"])
#                else:
#                    scaling_data = create_scaling_data(region, wild_encounter)
#                    world.scaling_data.append(scaling_data)

    # if johto only is off, add kanto data
    if world.options.johto_only == JohtoOnly.option_off:
        for region, trainers in kanto_trainer_data.items():
            for trainer in trainers:
                scaling_data = next((data for data in world.scaling_data if data.name == trainer["name"]), None)
                if scaling_data is not None:
                    update_scaling_data(scaling_data, trainer["connections"], trainer["data_ids"])
                else:
                    scaling_data = create_scaling_data(region, trainer)
                    world.scaling_data.append(scaling_data)

#        for region, wild_encounters in kanto_wild_encounter_data.items():
#            for wild_encounter in wild_encounters:
#                scaling_data = next((data for data in world.scaling_data if data.name == wild_encounter["name"]), None)
#                if scaling_data is not None:
#                    update_scaling_data(scaling_data, wild_encounter["connections"], wild_encounter["data_ids"])
#                else:
#                    scaling_data = create_scaling_data(region, wild_encounter)
#                    world.scaling_data.append(scaling_data)

        for region, static_encounters in kanto_static_encounter_data.items():
            for static_encounter in static_encounters:
                scaling_data = next((data for data in world.scaling_data if data.name == static_encounter["name"]), None)
                if scaling_data is not None:
                    update_scaling_data(scaling_data, static_encounter["connections"], static_encounter["data_ids"])
                else:
                    scaling_data = create_scaling_data(region, static_encounter)
                    world.scaling_data.append(scaling_data)


def perform_level_scaling(multiworld: MultiWorld):
    # from regions.json; might need to add some events to that file, good thing we have all the data already.
    # actually, you know what? screw it, events are coming from data.json.
    # yeah, so i think i've figured out the path here.  these events need to be in regions.json so that the
    # apworld randomizer can account for them. this does not mean they need to be on the tracker fyi. but
    # we need to give this function some milestones so it can track the spheres and knows how to curve the
    # levels properly.
    # i'll also create a proper events.json to hold all the events inside.
    # so cherrygrove city rival isn't a real event it seems? unless i'm missing something. it gets set when
    # you pick your starter, but it never gets cleared. interesting. we could always add a clearevent tbh.
    # oh, since you're not required to win.  same happens in vroad, there's no BEAT event. and the fast ship too.
    # mostly this matters for ER/random start town future proofing. eusine matters for future legend hunt fyi.
    # basically, if you are asking why something is here, most likely it's future proofing.
    # for e4, each member has an event, plus a general "you beat them all" in hall of fame, so probably could
    # have which ones apply vary based on settings? or leave it as is, wouldn't hurt to scale them back to back lol.
    # so for every rival fight, there is a flag set just before fighting them.  there is never a flag that gets
    # cleared, with the exception of Mt. Moon, since that matters for future things.  All other rival fights,
    # aside from the first, when you lose you just whiteout, which might clear the event until you trigger it again.
    # so yeah this is kind of interesting to handle... hmm...
    # with the new approach, might be able to change all these to their trainer address, vice event.
    battle_events = [
#        "EVENT_RIVAL_CHERRYGROVE_CITY", # i only need to list one of the three rivals, since they are in the same region
#        "EVENT_BEAT_SAGE_LI", # Sprout Tower Boss
        "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
#        "EVENT_CLEARED_SLOWPOKE_WELL", # Slowpoke Well Boss
#        "EVENT_HIVE_BADGE_FROM_BUGSY",
        "EVENT_RIVAL_AZALEA_TOWN", # azalea
        "EVENT_PLAIN_BADGE_FROM_WHITNEY",
#        "EVENT_RIVAL_BURNED_TOWER", # burned tower
#        "EVENT_BEAT_KIMONO_GIRL_MIKI", # final girl
        "EVENT_FOG_BADGE_FROM_MORTY",
        "EVENT_BEAT_POKEFANM_DEREK", # Route 39
        "EVENT_STORM_BADGE_FROM_CHUCK",
#        "EVENT_FOUGHT_EUSINE", # in Cianwood, for legendary hunt maybe? could be fun.
        "EVENT_MINERAL_BADGE_FROM_JASMINE",
        "EVENT_CLEARED_ROCKET_HIDEOUT", # Rocket HQ Finale - ER won't randomize the HQ
        "EVENT_GLACIER_BADGE_FROM_PRYCE",
        "EVENT_BEAT_ROCKET_EXECUTIVEM_3",  # False Director
        "EVENT_RIVAL_GOLDENROD_UNDERGROUND", # basement
#        "EVENT_BEAT_ROCKET_GRUNTF_3", # Puzzle Room
#        "EVENT_BEAT_ROCKET_GRUNTM_24", # Warehouse
        "EVENT_CLEARED_RADIO_TOWER", # Radio Tower Finale
        "EVENT_RISING_BADGE_FROM_CLAIR",
        "EVENT_BEAT_COOLTRAINERM_DARIN", # Dragon's Den Entrance
        "EVENT_RIVAL_VICTORY_ROAD", # victory road
#        "EVENT_BEAT_ELITE_4_WILL",
#        "EVENT_BEAT_ELITE_4_KOGA",
#        "EVENT_BEAT_ELITE_4_BRUNO",
#        "EVENT_BEAT_ELITE_4_KAREN",
        "EVENT_BEAT_ELITE_FOUR", # we'll keep the e4 members for ER future proofing
        "EVENT_FAST_SHIP_LAZY_SAILOR", # boat quest
        "EVENT_THUNDER_BADGE_FROM_LTSURGE",
        "EVENT_MARSH_BADGE_FROM_SABRINA",
        "EVENT_RAINBOW_BADGE_FROM_ERIKA",
#        "EVENT_BEAT_BIRD_KEEPER_BOB", # Route 18
        "EVENT_SOUL_BADGE_FROM_JANINE",
#        "EVENT_BEAT_POKEFANM_JOSHUA", # Fred
#        "EVENT_BEAT_COOLTRAINERM_KEVIN", # Fabulous Prize
        "EVENT_CASCADE_BADGE_FROM_MISTY",
        "EVENT_BOULDER_BADGE_FROM_BROCK",
        "EVENT_VOLCANO_BADGE_FROM_BLAINE",
        "EVENT_EARTH_BADGE_FROM_BLUE",
        "EVENT_BEAT_RIVAL_IN_MT_MOON", # except for this one, because it's required to spawn the league rematch
#        "EVENT_RIVAL_INDIGO_PLATEAU_POKECENTER", # this is the league rematch, wednesdays and fridays only
#        "EVENT_KOJI_ALLOWS_YOU_PASSAGE_TO_TIN_TOWER", # 3rd of Wise Trio, if they ever get added back in.
        "EVENT_BEAT_RED" # Either Red is the final boss, or he's not lol.  Either way, might as well have a roof.
    ]

    level_scaling_required = False
    state = CollectionState(multiworld)
    progression_locations = {loc for loc in multiworld.get_filled_locations() if loc.item.advancement}
    crystal_locations: Set[PokemonCrystalLocation] = {loc for loc in multiworld.get_filled_locations() if loc.game == "Pokemon Crystal"}
    scaling_locations = {loc for loc in crystal_locations if loc.tags.contains("scaling")}
    locations = progression_locations | scaling_locations
    collected_locations = set()
    spheres = []

    for world in multiworld.get_game_worlds("Pokemon Crystal"):
        if world.options.level_scaling != LevelScaling.option_off:
            level_scaling_required = True
        else:
            world.finished_level_scaling.set()

    if not level_scaling_required:
        return

    # AP runs through the seed and starts collecting locations and counting spheres
    # to find battle milestones as listed above. this is important for creating our level curve.
    while len(locations) > 0:
        new_spheres: List[Set] = []
        new_battle_events = set()
        battle_events_found = True

        while battle_events_found:
            battle_events_found = False
            events_found = True
            sphere = set()
            old_sphere = set()
            distances = {}

            while events_found:
                events_found = False

                for world in multiworld.get_game_worlds("Pokemon Crystal"):
                    if world.options.level_scaling != LevelScaling.option_spheres_and_distance:
                        continue
                    # Menu is region 0, so we start counting from here.
                    regions = {multiworld.get_region("Menu", world.player)}
                    checked_regions = set()
                    distance = 0
                    while regions:
                        update_regions = True
                        while update_regions:
                            update_regions = False
                            same_distance_regions = set()
                            for region in regions:
                                encounter_regions = {e.connected_region for e in region.exits if e.access_rule(state)}
                                same_distance_regions.update(encounter_regions)
                            regions_len = len(regions)
                            regions.update(same_distance_regions)
                            if len(regions) > regions_len:
                                update_regions = True
                        next_regions = set()
                        for region in regions:
                            if not getattr(region, "distance") or distance < region.distance:
                                region.distance = distance
                            next_regions.update({e.connected_region for e in region.exits if e.connected_region not in checked_regions and e.access_rule(state)})
                        checked_regions.update(regions)
                        regions = next_regions
                        distance += 1

                for location in locations:
                    def can_reach():
                        if location.can_reach(state):
                            return True
                        return False

                    if can_reach():
                        sphere.add(location)

                        if location.game == "Pokemon Crystal":
                            parent_region: RegionData = location.parent_region
                            if getattr(parent_region, "distance", None) is None:
                                distance = 0
                            else:
                                distance = parent_region.distance
                        else:
                            distance = 0

                        if distance not in distances:
                            distances[distance] = {location}
                        else:
                            distances[distance].add(location)

                locations -= sphere
                old_sphere ^= sphere

                for location in old_sphere:
                    if location.is_event and location.item and location not in collected_locations:
                        if location.name not in battle_events:
                            collected_locations.add(location)
                            state.collect(location.item, True, location)
                            events_found = True
                        else:
                            new_battle_events.add(location)
                            battle_events_found = True

                old_sphere |= sphere

            if sphere:
                for distance in sorted(distances.keys()):
                    new_spheres.append(distances[distance])

            for event in new_battle_events:
                if event.item and event not in collected_locations:
                    collected_locations.add(event)
                    state.collect(event.item, True, event)

        if len(new_spheres) > 0:
            for sphere in new_spheres:
                spheres.append(sphere)

                for location in sphere:
                    if location.item and location not in collected_locations:
                        collected_locations.add(location)
                        state.collect(location.item, True, location)
        else:
            spheres.append(locations)
            break

    for world in multiworld.get_game_worlds("Pokemon Crystal"):
        if world.options.level_scaling == LevelScaling.option_off:
            continue

        red_goal_adjustment = 73 / 40 # adjusts for when red is goal, 1.8 times higher level
        e4_base_level = 40

        for sphere in spheres:
            scaling_locations = [loc for loc in sphere if loc.player == world.player and loc.tags.contains("scaling")]
            trainer_locations = [loc for loc in scaling_locations if loc.tags.contains("trainer scaling")]
            encounter_locations = [loc for loc in scaling_locations if loc.tags.contains("static scaling")]

            trainer_locations.sort(key=lambda loc: world.trainer_name_list.index(loc.name))
            encounter_locations.sort(key=lambda loc: world.encounter_name_list.index(loc.name))

            for trainer_location in trainer_locations:
                new_base_level = world.trainer_level_list.pop(0)
                old_base_level = world.trainer_name_level_dict[trainer_location.name]

                if trainer_location.name == "WILL_1" or "KOGA_1" or "BRUNO_1" or "KAREN_1" or "LANCE_1":
                    e4_base_level = new_base_level
                elif trainer_location.name == "RED_1":
                    new_base_level = max(new_base_level, round(e4_base_level * red_goal_adjustment))

                for trainer_location in trainer_location:
                    trainer_data = world.generated_trainers[trainer_location]
                    for pokemon in trainer_data.pokemon:
                        new_level = round(min((new_base_level * pokemon.level / old_base_level),
                                              (new_base_level + pokemon.level - old_base_level)))
                        new_level = bound(new_level, 1, 100)
                        trainer_data.pokemon[0] = new_level

            for encounter_location in encounter_locations:
                new_base_level = world.encounter_level_list.pop(0)
                old_base_level = world.encounter_name_level_dict[encounter_location.name]

                for encounter_location in encounter_location:
                    if encounter_location.tags.contains("static scaling"):
                            pokemon_data = world.generated_static[encounter_location]

                            pokemon_data.level = new_base_level

        world.finished_level_scaling.set()
