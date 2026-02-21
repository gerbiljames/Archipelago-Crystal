from ..Locations import all_locations_table, speedrun_logic_table, sub_locations_in_maps
from ..ItemNames import *

# Custom font for items
items_shortened = {
    portal_gun_1 : "ÿ",
    portal_gun_2 : "ú",
    potatos : "ù",
    weighted_cube : "ç",
    reflection_cube : "ì",
    spherical_cube : "ë",
    antique_cube : "é",
    button : "ñ",
    old_button : "ò",
    floor_button : "æ",
    old_floor_button : "è",
    frankenturret : "ð",
    paint : "¢",
    laser : "í",
    faith_plate : "õ",
    funnel : "å",
    bridge : "¿",
    laser_relays : "ï",
    laser_catcher : "î",
    turrets : "ó",
    adventure_core : "A.ô",
    space_core : "S.ô",
    fact_core : "F.ô",

    moon_dust : "¡",
    lemon : "¡",
    slice_of_cake : "¡",

    motion_blur_trap : "¥",
    fizzle_portal_trap : "¥",
    butter_fingers_trap : "¥",
    cube_confetti_trap : "¥",
    slippery_floor_trap : "¥"
}

indicator_characters: dict[str, str] = {
    "completed" : "✓",
    "map": "M",
    "wheatley" : "ô",
    "ratman": "R",
    portal_gun_1 : "ÿ",
    portal_gun_2 : "ú",
    potatos : "ù"
}

def items_to_shortened(items_list: list[str]) -> list[str]:
    return map(lambda x: items_shortened[x], items_list)

class MenuElement:
    def __init__(self, parent, name: str, title: str, subtitle: str = "", command: str = "", pic: str = ""):
        self.parent = parent
        self.name = name
        self.title = title
        self.subtitle = subtitle
        self.command = command
        self.pic = pic

    def __str__(self):
        return (
            f'  "{self.name}"\n'
             '   {\n'
            f'      "title"    "{self.title}"\n'
            f'      "subtitle" "{self.subtitle}"\n'
            f'      "command"  "{self.command}"\n'
            f'      "pic"      "{self.pic}"\n'
             '   }\n'
        )


class MapMenuElement(MenuElement):
    next_map: MenuElement = None
    completed: bool = False
    def __init__(self, parent, chapter_number, map_number, title, map_code, location_id, required_items, pic):
        self.location_id = location_id
        self.required_items = required_items
        subtitle = " ".join(items_to_shortened(self.required_items))
        new_title = indicator_characters["map"] + check_sub_locations(title, parent.parent.has_wheatley_monitors, parent.parent.has_ratman_dens)
        # Pad title to 4 characters for alignment
        new_title = new_title.ljust(4, "-") + title.removesuffix(" Completion")
        super().__init__(parent, f"chapter {chapter_number}.{map_number}", new_title, subtitle, f"map {map_code}", pic)

    def get_string(self, previous_completed: bool):
        # Update required items
        new_required_items = [item for item in self.required_items if item in self.parent.parent.client.item_list]
        
        # Remake subtitle
        self.subtitle = " ".join(items_to_shortened(new_required_items))
        
        text = super().__str__()
        if not (self.parent.parent.is_open_world or previous_completed):
            text = text.replace("command", "command_deactivated")
        if self.next_map:
            return text + self.next_map.get_string(self.completed)
        else:
            return text

    def complete_map(self, map_id: int) -> bool:
        if self.location_id == map_id:
            if self.completed:
                return True
            self.completed = True
            self.title = self.title.replace(indicator_characters["map"], indicator_characters["completed"], 1)
            if self.next_map:
                self.next_map.command = self.next_map.command.replace("command_deactivated", "command")
            return True
        else:
            if self.next_map:
                return self.next_map.complete_map(map_id)
            else:
                return False
                
    def complete_sub_location_check(self, sub_location: str):
        if sub_location in sub_locations_in_maps.get(self.title[4:] + " Completion", []):
            if "Wheatley Monitor" in sub_location:
                self.title = self.title.replace(indicator_characters["wheatley"], indicator_characters["completed"], 1)
            elif "Ratman Den" in sub_location:
                self.title = self.title.replace(indicator_characters["ratman"], indicator_characters["completed"], 1)
            elif sub_location in indicator_characters:
                self.title = self.title.replace(indicator_characters[sub_location], indicator_characters["completed"], 1)
        elif self.next_map:
            self.next_map.complete_sub_location_check(sub_location)
            
    def complete_check(self, location_id: int):
        if not self.complete_map(location_id):
            location_name = self.parent.parent.client.location_names.lookup_in_game(location_id)
            if "Complete" not in location_name:
                self.complete_sub_location_check(location_name)
                
def check_sub_locations(title: str, has_wheatley_monitors: bool, has_ratman_dens: bool) -> str:
    location_name = title
    
    additional_indicators = ""
    if location_name in sub_locations_in_maps:
        sub_locations = sub_locations_in_maps[location_name]
        for sub_location in sub_locations:
            if "Wheatley Monitor" in sub_location and has_wheatley_monitors:
                additional_indicators += indicator_characters["wheatley"]
            elif "Ratman Den" in sub_location and has_ratman_dens:
                additional_indicators += indicator_characters["ratman"]
            elif sub_location in indicator_characters:
                additional_indicators += indicator_characters[sub_location]
    
    return additional_indicators

class ChapterMenuElement(MenuElement):
    first_map: MapMenuElement = None
    def __init__(self, parent, chapter_number: int, map_names: list[str]):
        super().__init__(parent, f"chapter{chapter_number}", f"Chapter {chapter_number}", pic=f"vgui/chapters/chapter{chapter_number}")
        current_map: MapMenuElement = None
        for i, name in enumerate(map_names):
            location = all_locations_table[name]
            next_map = MapMenuElement(self, chapter_number, i, name, location.map_name, location.id, location.required_items, self.pic)
            if not self.first_map:
                self.first_map = next_map
                current_map = self.first_map
            else:
                current_map.next_map = next_map
                current_map = next_map

    def __str__(self):
        return super().__str__() + self.first_map.get_string(True)
    
    def complete_map(self, map_id: int):
        self.first_map.complete_map(map_id)
        
    def complete_sub_location_check(self, sub_location: str):
        self.first_map.complete_sub_location_check(sub_location)
        
    def complete_check(self, location_id: int):
        self.first_map.complete_check(location_id)


class Menu:
    chapters: list[ChapterMenuElement] = []

    def __init__(self, chapter_dict: dict[int, list[str]], client, is_open_world: bool = False, logic_difficulty: int = 0, wheatley_monitors: bool = False, ratman_dens: bool = False):
        # Update all_locations table to speedrun logic
        if logic_difficulty == 1:
            for map_location in speedrun_logic_table:
                all_locations_table[map_location].required_items = speedrun_logic_table[map_location]
        self.client = client
        self.is_open_world = is_open_world
        self.has_wheatley_monitors = wheatley_monitors
        self.has_ratman_dens = ratman_dens
        for chapter_number, map_names in chapter_dict.items():
            self.chapters.append(ChapterMenuElement(self, chapter_number, map_names))

    def __str__(self):
        return (
            '"Extras"\n'
            '{\n'
            f'{"".join([str(map) for map in self.chapters])}'
            '}\n'
        )

    def complete_map(self, map_id: int):
        for chapter in self.chapters:
            chapter.complete_map(map_id)
            
    def complete_sub_location_check(self, sub_location: str):
        for chapter in self.chapters:
            chapter.complete_sub_location_check(sub_location)
            
    def complete_check(self, location_id: int):
        for chapter in self.chapters:
            chapter.complete_check(location_id)
