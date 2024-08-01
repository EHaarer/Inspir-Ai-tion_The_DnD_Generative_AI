import streamlit as st
import requests
import random
import openai
import streamlit.components.v1 as components
import re

# Set your OpenAI API key

# Base URL for the D&D 5e API
api_base_url = "https://www.dnd5eapi.co/api"

# Define ranges for settlement sizes
settlement_sizes = {
    "Thorp": (3, 6, (8, 20), (1, 3)),
    "Village": (5, 8, (80, 200), (1, 5)),
    "Town": (7, 12, (400, 2000), (1, 8)),
    "City": (10, 15, (5000, 25000), (1, 15)),
    "Metropolis": (12, 20, (30000, 150000), (1, 20))
}

# Function to fetch races from D&D API
def get_race():
    response = requests.get(f"{api_base_url}/races")
    if response.status_code == 200:
        races = response.json()
        return races['results']
    else:
        st.error("Failed to fetch races.")
        return []

# Function to fetch classes from D&D API
def get_class():
    response = requests.get(f"{api_base_url}/classes")
    if response.status_code == 200:
        classes = response.json()
        return classes['results']
    else:
        st.error("Failed to fetch classes.")
        return []

# Function to fetch all magic items from D&D API
@st.cache_resource  # Cache the response to avoid making multiple requests
def get_magic_items():
    response = requests.get(f"{api_base_url}/magic-items")
    if response.status_code == 200:
        items = response.json()
        return items['results']
    else:
        st.error("Failed to fetch magic items.")
        return []

# Function to generate random names from randomuser.me API
def generate_names(number_of_names):
    response = requests.get(f"https://randomuser.me/api/?results={number_of_names}&nat=us")
    if response.status_code == 200:
        users = response.json()['results']
        names = [f"{user['name']['first']} {user['name']['last']}" for user in users]
        return names
    else:
        st.error("Failed to generate names.")
        return []

# Function to generate a random name
def generate_random_name():
    first_names = ["Oak", "River", "Stone", "Wind", "Bright", "Shadow", "Golden", "Silver", "Wolf", "Dragon", "Ogre", "Stag", "Bear", "Eagle", "Raven", "Lion", "Tiger", "Fox", "Hawk", "Snake", "Badger", "Boar", "Deer", "Elk", "Falcon", "Horse", "Moose", "Owl", "Beholder", "Rat", "Shark", "Sparrow", "Swan", "Whale", "Wolf", "Bat", "Bee", "Hare", "Hawk", "Jaguar", "Koala", "Leopard", "Lizard", "Scorpion", "Spider"]
    return random.choice(first_names)

# Function to generate a random settlement name based on different conventions
def generate_settlement_name(custom_name):
    if custom_name:
        return custom_name

    convention = random.choice([1, 2])
    X = generate_random_name()

    if convention == 1:
        Y = random.choice(["Creek", "Divide", "Hill", "Burgh", "Hub", "Keep", "Fell", "Shire", "Haven", "Crossing", "Watch", "Gate", "Moor", "Field", "Glen", "Dale", "Wood", "Wick", "Wold"])
        return f"{X}'s {Y}"
    elif convention == 2:
        Y = random.choice(["polis", "ville", "vale", "ton", "stead", "ford", "burg", "borough", "ville", "field", "shire", "wood", "wick", "wold", "dale", "glen", "moor", "gate", "watch", "cross", "haven", "keep", "hub", "burgh", "divide", "creek"])
        return f"{X}-{Y}"
    else:
        words = ["Oak", "River", "Stone", "Wind", "Bright", "Shadow", "Golden", "Silver", "Wolf", "Dragon", "Ogre", "Stag", "Bear", "Eagle", "Raven", "Lion", "Tiger", "Fox", "Hawk", "Snake", "Badger", "Boar", "Deer", "Elk", "Falcon", "Horse", "Moose", "Owl", "Beholder", "Rat", "Shark", "Sparrow", "Swan", "Whale", "Wolf", "Bat", "Bee", "Hare", "Hawk", "Jaguar", "Koala", "Leopard", "Lizard", "Scorpion", "Spider"]
        return f"{random.choice(words)} {random.choice(words)}"

# Function to generate a random population based on settlement size
def generate_population(settlement_size):
    min_pop, max_pop = settlement_size[2]
    if max_pop <= 200:
        return random.randint(min_pop, max_pop)
    elif max_pop <= 2000:
        return random.randint(min_pop // 10, max_pop // 10) * 10
    else:
        return random.randint(min_pop // 100, max_pop // 100) * 100

# Function to assign race, class, level, and magic items to a character
def assign_race_class_level(character_name, level_range):
    race = random.choice(get_race())
    character_class = random.choice(get_class())
    level = random.randint(*level_range)
    magic_items = get_magic_items_based_on_level(level)

    # Fetch race details
    race_details = get_race_details(race['index'])
    size = race_details['size']
    speed = race_details['speed']
    traits = [trait['name'] for trait in race_details['traits']]

    alignment = generate_alignment()

    ability_scores = generate_ability_scores(character_class['name'])
    apply_racial_bonuses(race['name'], ability_scores)

    return {
        "name": character_name,
        "race": race['name'],
        "class": character_class['name'],
        "level": level,
        "magic_items": magic_items,
        "size": size,
        "speed": speed,
        "traits": traits,
        "alignment": alignment,
        "ability_scores": ability_scores,
        "passive_perception": calculate_passive_perception(ability_scores['Wisdom']),
        "armor_class": calculate_armor_class(character_class['name'], ability_scores['Dexterity']),
        "hit_points": calculate_hit_points(character_class['name'], level, ability_scores['Constitution'])
    }

# Function to fetch race details from D&D API
def get_race_details(race_index):
    response = requests.get(f"{api_base_url}/races/{race_index}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch race details.")
        return {}

# Function to get magic items based on character level
def get_magic_items_based_on_level(level):
    items = get_magic_items()
    if not items:
        return []

    if 3 <= level <= 5:
        count = random.randint(0, 1)
    elif 6 <= level <= 10:
        count = random.randint(1, 2)
    elif 11 <= level <= 15:
        count = random.randint(1, 3)
    elif 16 <= level <= 18:
        count = random.randint(3, 5)
    elif 19 <= level <= 20:
        count = random.randint(4, 8)
    else:
        count = 0

    return random.sample(items, min(count, len(items)))

# Function to generate characters based on settlement size
def generate_characters(settlement_size):
    min_names, max_names, _, level_range = settlement_sizes[settlement_size]
    number_of_names = random.randint(min_names, max_names)
    return generate_names(number_of_names), level_range

# Function to generate a random alignment
def generate_alignment():
    X = random.choice(["Lawful", "Neutral", "Chaotic"])
    Y = random.choice(["Good", "Neutral", "Evil"])
    if X == "Neutral" and Y == "Neutral":
        return "True Neutral"
    else:
        return f"{X} {Y}"

# Function to generate ability scores based on the character's class
def generate_ability_scores(character_class):
    def roll_dice():
        rolls = sorted([random.randint(1, 6) for _ in range(4)])
        return sum(rolls[1:])  # sum of the highest 3 rolls

    # Generate 6 roll values
    asi_array = [roll_dice() for _ in range(6)]
    asi_array.sort(reverse=True)  # Sort in descending order for easy assignment

    # Mapping for highest ability score by class
    class_mapping = {
        "Cleric": "Wisdom",
        "Druid": "Wisdom",
        "Ranger": "Wisdom",
        "Bard": "Charisma",
        "Paladin": "Charisma",
        "Sorcerer": "Charisma",
        "Warlock": "Charisma",
        "Barbarian": "Strength",
        "Fighter": "Strength",
        "Monk": "Dexterity",
        "Rogue": "Dexterity",
        "Wizard": "Intelligence",
        "Artificer": "Intelligence"
    }

    # Get the primary ability for the class
    primary_ability = class_mapping.get(character_class, "Strength")

    # Create a dictionary to hold ability scores
    ability_scores = {
        "Strength": 0,
        "Dexterity": 0,
        "Constitution": 0,
        "Intelligence": 0,
        "Wisdom": 0,
        "Charisma": 0
    }

    # Assign the highest roll to the primary ability
    ability_scores[primary_ability] = asi_array[0]

    # Assign the remaining 5 values to the other abilities randomly
    remaining_abilities = [key for key in ability_scores if key != primary_ability]
    random.shuffle(remaining_abilities)
    for i, ability in enumerate(remaining_abilities):
        ability_scores[ability] = asi_array[i + 1]

    return ability_scores

# Function to apply racial bonuses to ability scores
def apply_racial_bonuses(race, ability_scores):
    if race == "Human":
        for key in ability_scores:
            ability_scores[key] += 1
    elif race == "Half-Elf":
        ability_scores["Charisma"] += 1
        random_keys = random.sample([key for key in ability_scores if key != "Charisma"], 2)
        for key in random_keys:
            ability_scores[key] += 1
    elif race == "Elf":
        ability_scores["Dexterity"] += 2
    elif race == "Half-Orc":
        ability_scores["Strength"] += 2
        ability_scores["Constitution"] += 1
    elif race == "Dragonborn":
        ability_scores["Strength"] += 2
        ability_scores["Charisma"] += 1
    elif race == "Dwarf":
        ability_scores["Constitution"] += 2
    elif race == "Gnome":
        ability_scores["Intelligence"] += 2
    elif race == "Halfling":
        ability_scores["Dexterity"] += 2
    elif race == "Tiefling":
        ability_scores["Charisma"] += 2

# Function to calculate the ability modifier
def calculate_modifier(score):
    modifier = (score - 10) // 2
    sign = '+' if modifier > 0 else ''
    return f"{sign}{modifier}"

# Function to calculate passive perception
def calculate_passive_perception(wisdom_score):
    return 10 + (wisdom_score - 10) // 2

# Function to calculate armor class
def calculate_armor_class(character_class, dexterity_score):
    dex_mod = (dexterity_score - 10) // 2
    if character_class in ["Wizard", "Monk", "Sorcerer"]:
        return 10 + dex_mod
    elif character_class in ["Artificer", "Bard", "Druid", "Rogue", "Warlock"]:
        return min(14, 12 + dex_mod)
    elif character_class in ["Barbarian", "Cleric", "Ranger"]:
        return min(16, 14 + dex_mod)
    else:
        return 18

# Function to calculate hit points
def calculate_hit_points(character_class, level, constitution_score):
    con_mod = (constitution_score - 10) // 2
    if character_class in ["Sorcerer", "Wizard"]:
        return 6 + (level - 1) * 4 + (level * con_mod)
    elif character_class in ["Artificer", "Bard", "Cleric", "Druid", "Monk", "Rogue", "Warlock"]:
        return 8 + (level - 1) * 5 + (level * con_mod)
    elif character_class in ["Fighter", "Paladin", "Ranger"]:
        return 10 + (level - 1) * 6 + (level * con_mod)
    elif character_class == "Barbarian":
        return 12 + (level - 1) * 7 + (level * con_mod)
    else:
        return 10 + (level - 1) * 5 + (level * con_mod)  # Default case

# Function to generate a town description using OpenAI API
def generate_town_description(town_name, town_type, town_population, unique_characters):
    system_message = "You are to generate a description of 3-5 sentences of a fantasy town in Dnd 5e, and you should talk about the vibe of the town, the weather, the surrounding environment and any locations of note. In each request from here on, You will receive the town name, population size and number of unique characters. Generate the relevant information with each prompt, but do not list any characters by specific name."
    prompt = f"Town Name: {town_name}, Town Type: {town_type}, Town Population: {town_population}, Unique Characters: {unique_characters}"
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=1
    )
    return response.choices[0].message.content
    #return response['choices'][0]['message']['content']

def generate_quest(town_name, character_data):
    system_message = "You will receive a input prompt in the format of \"Town Name:T Characters:[N|A|C], [N|A|C], [N|A|C]...\" where T is the name of the settlement in which the quest MUST mainly be located, and then for all unique characters in the location N is the name of a character, A is that character's moral alignment, and C is the character's class. The output should be Blocked out in the following sections: Quest Title, Quest Giver, Quest Background, Stages of the Quest, Possible Resolutions, and Conclusion. There will be many 'characters' sent in this format, and you must generate a quest given all of these characters. Each quest should be detailed and in-depth. There will be a designated quest giver that will tell the Heroes of a problem, situation or event that is happening. You will list out the stages of the quest, listing what the quest giver wants the heroes to do, whether that be to collect something, clear out a location of monsters, convince someone of something, solve a mystery, catch a person or bad guy, track down a faction or secret society, steal an item or artifact, or unravel a political plot. These quests should be relevant to the Class and alignment of the character that is the quest-giver, and should be given out in or around the core location. For instance a wizard or sorcerer may have a quest that is more magic-aligned, a druid is nature-aligned, a rouge is sneaky-aligned, etc. The quest should have multiple stages of discovery, combat, skill checks or others that are needed to advance. In most quests, there should include some sort of revelation or twist that allows the heroes to resolve the quest in more than one way. The quest should only include named characters that are listed in the input, list out the stages of the quest in 1, 2, 3... format and then list all possible resolutions based on the player character's decisions, including rewards in either magic items and/or gold pieces, defining what the magic items do. The Possible Resolutions section should be similarly enumerated."
    prompt = f"Town Name:{town_name}: Characters: {character_data}"

    print(prompt)

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=1
    )
    return response.choices[0].message.content

def insert_newlines_before_numbers(text):
    # Define the regex pattern to match numbers followed by a dot (e.g., "1.", "2.", ...)
    pattern = r'(\d+\.)'
    
    def replace_match(match):
        if match.group(1) == '1.':
            return match.group(1)
        else:
            return f'<br>{match.group(1)}'
    
    # Replace the pattern using the replace_match function
    modified_text = re.sub(pattern, replace_match, text)
    
    return modified_text

def insert_newlines_before_hyphens(text):
    # Replace each hyphen with a new-line character followed by the hyphen
    modified_text = text.replace("-", "<br>-")
    
    return modified_text


def replace_bold_italic(text: str) -> str:
    # Define the regex pattern to match text between "**"
    pattern = r'\*\*(.*?)\*\*'
    
    def replace_match(match):
        inner_text = match.group(1)
        if len(inner_text) < 50:
            return f'<span style="font-weight:bold;font-style:italic;">{inner_text}</span>'
        else:
            return inner_text
    
    # Replace matching patterns using the replace_match function
    modified_text = re.sub(pattern, replace_match, text)
    
    # Remove any remaining "**"
    modified_text = modified_text.replace('**', '')
    
    return modified_text


def extract_quest_details(quest_text):
    # Define the substrings to search for
    substrings = [
        "Quest Title",
        "Quest Giver",
        "Quest Background",
        "Stages of the Quest",
        "Possible Resolutions",
        "Conclusion"
    ]
    
    # Initialize an empty list to store the results
    results = [""] * len(substrings)  # Initialize results with empty strings for each substring

    # Extract the text segments between the substrings
    for i in range(len(substrings) - 1):
        start = quest_text.find(substrings[i]) + len(substrings[i])
        end = quest_text.find(substrings[i + 1])
        if start < len(substrings[i]) or end == -1:  # Check if start is valid and end is found
            continue  # Skip to next iteration if not found
        results[i] = quest_text[start:end].strip()

    # Extract the text after the last substring
    start = quest_text.find(substrings[-1]) + len(substrings[-1])
    if start >= len(substrings[-1]):  # Check if start is valid
        results[-1] = quest_text[start:].strip()
    
    return results


    

def main():
    st.title("Inspiration AI - D&D Edition")

    custom_settlement_name = st.text_input("Custom Settlement Name")
    settlement_size = st.selectbox("Select Settlement Size", list(settlement_sizes.keys()))

    settlement_name_copy = custom_settlement_name

    loading_placeholder = st.empty()

    # Initialize session state if it doesn't exist
    if 'town_tile' not in st.session_state:
        st.session_state.town_tile = ""
    if 'character_tiles' not in st.session_state:
        st.session_state.character_tiles = ""
    if 'quests' not in st.session_state:
        st.session_state.quests = []

    if st.button(f"Generate {settlement_size}"):
        with loading_placeholder:
            st.spinner("Generating...")
            settlement_name = generate_settlement_name(custom_settlement_name)
            settlement_name_copy = settlement_name
            population = generate_population(settlement_sizes[settlement_size])
            character_names, level_range = generate_characters(settlement_size)
            unique_characters = len(character_names)

            town_description = generate_town_description(settlement_name, settlement_size, population, unique_characters)

        loading_placeholder.empty()
        
        st.session_state.town_tile = f"""
        <div class="town-tile" style="margin: 0 auto; text-align: left;">
            <div class="town-info">
                <h2 style="text-align: center;">{settlement_name} - {settlement_size}</h2>
                <p><strong>Population:</strong> {population}</p>
                <p><strong>Number of Unique Characters:</strong> {unique_characters}</p>
                <p><strong>Description:</strong> {town_description}</p>
            </div>
        </div>
        """

        character_tiles = ""
        character_data = ""
        for name in character_names:
            character_info = assign_race_class_level(name, level_range)
            ability_scores = character_info['ability_scores']
            character_data += f"[{character_info['name']}|{character_info['alignment']}|{character_info['class']}], "

            tile = f"""
            <div class="character-tile">
                <div contenteditable="true"  style="width:85%; font-family:Arial,Helvetica,sans-serif;font-size:11px;">
                <div class="name">{character_info['name']}</div>
                <div class="description">{character_info['race']} {character_info['class']}, {character_info['alignment']}</div>

                <div class="gradient"></div>

                <div class="red">
                    <div ><span class="bold red">Armor Class</span><span> {character_info['armor_class']} </span></div>
                    <div><span class="bold red">Hit Points</span><span> {character_info['hit_points']} </span></div>
                    <div><span class="bold red">Speed</span><span> {character_info['speed']} ft.</span></div>
                </div>

                <div class="gradient"></div>

                <table>
                    <tr><th>STR    </th><th>DEX   </th><th>CON    </th><th>INT   </th><th>WIS   </th><th>CHA   </th></tr>
                    <tr><td>{ability_scores['Strength']} ({calculate_modifier(ability_scores['Strength'])})</td><td>{ability_scores['Dexterity']} ({calculate_modifier(ability_scores['Dexterity'])})</td><td>{ability_scores['Constitution']} ({calculate_modifier(ability_scores['Constitution'])})</td><td>{ability_scores['Intelligence']} ({calculate_modifier(ability_scores['Intelligence'])})</td><td>{ability_scores['Wisdom']} ({calculate_modifier(ability_scores['Wisdom'])})</td><td>{ability_scores['Charisma']} ({calculate_modifier(ability_scores['Charisma'])})</td></tr>
                </table>
                    
                <div class="gradient"></div>
                    
                <div><span class="bold">Traits</span><span> {', '.join(character_info['traits'])}</span></div>
                <div><span class="bold">Passive Perception</span><span> {character_info['passive_perception']}</span></div>
                <div><span class="bold">Languages</span><span> Common, TODO</span></div>
                <div><span class="bold">Level </span><span> {character_info['level']}</span></div> 
                    
                <div class="gradient"></div>

                <div class="actions red">Actions</div>
                    
                <div class="hr"></div>
                
                <div><span class="bold">Magic Items: </span><span> {', '.join([item['name'] for item in character_info['magic_items']])}</span></div>
                <div class="attack"><span class="attackname">Greatclub.</span><span class="description"> Melee Weapon Attack:</span><span>+6 to hit, reach 5 ft., one target.</span><span class="description">Hit:</span><span>13 (2d8+4) bludgeoning damage.</span></div>    
                <div class="attack"><span class="attackname">Javelin.</span><span class="description"> Melee or Ranged Weapon Attack:</span><span>+6 to hit, reach 5 ft. or 30ft./120, one target.</span><span class="description">Hit:</span><span>11 (2d6+4) piercing damage.</span></div>    
                </div>
            </div>
            """

            character_tiles += tile

        st.session_state.character_tiles = character_tiles
        st.session_state.character_data = character_data

    # Display the town and character tiles
    if st.session_state.town_tile:
        custom_css = """
        <style>
        .gradient {
            background: linear-gradient(10deg, #A73335, white);
            height:5px;
            margin:7px 0px;
        }
        .name {
            font-size:225%;
            font-family:Georgia, serif;
            font-variant:small-caps;
            font-weight:bold;
            color:#A73335;
        }
        .description {
            font-style:italic;    
        }
        .bold {
            font-weight:bold;
        }
        .red {
            color:#A73335;
        }
        table {
            width:100%;
            border:0px;
            border-collapse:collapse;
            color:#A73335;
        }
        th, td {
            width:50px;
            text-align:center;
        }
        .actions {
            font-size:175%;
            font-variant:small-caps;
            margin:17px 0px 0px 0px;
        }
        .hr {
            background: #A73335;
            height:2px;
        }
        .attack {
            margin:5px 0px;
        }
        .attackname {
            font-weight:bold;
            font-style:italic;
        }
        .town-tile {
            width: 85%;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 7.5px;
            padding: 20px;
            margin-bottom: 20px;
            margin-left: auto;
            margin-right: auto;
        }
        .character-tiles-container-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .character-tiles-container {
            display: flex;
            overflow-x: auto;
            white-space: nowrap;
            scroll-snap-type: x mandatory;
            width: 80%;
            padding: 10px;
        }
        .character-tile {
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 7.5px;  /* Increased bevel on corners by 50% */
            margin-right: 10px;
            padding: 20px;
            min-width: 95%;
            max-width: 95%;
            flex: 0 0 auto;
            scroll-snap-align: start;
            white-space: normal;
        }
        .scroll-button {
            background-color: #007bff;
            border: none;
            color: white;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .scroll-button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .character-tiles-container::-webkit-scrollbar {
            display: none;
        }
        </style>
        <script>
        function scrollTilesContainer(direction) {
            const container = document.querySelector('.character-tiles-container');
            const tileWidth = container.querySelector('.character-tile').clientWidth + 10;  // Tile width + margin-right
            container.scrollBy({ left: direction * tileWidth, behavior: 'smooth' });
        }
        window.onload = function() {
            const container = document.querySelector('.character-tiles-container');
            const largestTile = Array.from(container.querySelectorAll('.character-tile')).reduce((maxHeight, tile) => {
                return Math.max(maxHeight, tile.clientHeight);
            }, 0);
            container.style.height = largestTile + 'px';
        };
        </script>
        """

        character_tiles_html = f"""
        {custom_css}
        {st.session_state.town_tile}
        <div class="character-tiles-container-wrapper">
            <button class="scroll-button" onclick="scrollTilesContainer(-1)">&lt;</button>
            <div class="character-tiles-container">
                {st.session_state.character_tiles}
            </div>
            <button class="scroll-button" onclick="scrollTilesContainer(1)">&gt;</button>
        </div>
        """

        components.html(character_tiles_html, height=900, scrolling=False)

    # Add the button to generate a new quest
    st.subheader("Quests")
    if st.button("Generate new quest"):
        quest = replace_bold_italic(generate_quest(settlement_name_copy, st.session_state.character_data))
        st.session_state.quests.append({
            "quest_text": quest,
            "quest_parts": extract_quest_details(quest)
        })

    # Display the quests
    for quest in st.session_state.quests:
        quest_parts = quest["quest_parts"]
        quest_tile = f"""
        <div class="quest-tile" style="margin: 0 auto; text-align: left; width: 85%; background-color: #f0f0f0; border: 1px solid #ddd; border-radius: 7.5px; padding: 20px; margin-bottom: 20px;">
            <div contenteditable="true"  style="width:100%; font-family:Arial,Helvetica,sans-serif;font-size:11px;">
            <h2 class="name" style = "font-size:225%; font-family:Georgia, serif; font-variant:small-caps; font-weight:bold; color:#A73335;">Quest: {quest_parts[0].strip(' :#')}</h2>
            <div style = "font-style:italic;">Quest Giver: {quest_parts[1].strip(' :#')}</div>
            <br>
            <div style="font-size:175%;font-variant:small-caps;margin:17px 0px 0px 0px; color:#A73335;">Quest Background</div>
            <div class="gradient" style="background: linear-gradient(10deg, #A73335, white); height:5px; margin:7px 0px;"></div>
            <p>{quest_parts[2].strip(' :#')}</p>
            <div style="font-size:175%;font-variant:small-caps;margin:17px 0px 0px 0px; color:#A73335;">Quest Stages</div>
            <div class="gradient" style="background: linear-gradient(10deg, #A73335, white); height:5px; margin:7px 0px;"></div>
            <p>{insert_newlines_before_numbers(quest_parts[3]).strip(' :#')}</p>
            <div style="font-size:175%;font-variant:small-caps;margin:17px 0px 0px 0px; color:#A73335;">Possible Resolutions</div>
            <div class="gradient" style="background: linear-gradient(10deg, #A73335, white); height:5px; margin:7px 0px;"></div>
            <p>{insert_newlines_before_numbers(quest_parts[4]).strip(' :#')}</p>
            <div style="font-size:175%;font-variant:small-caps;margin:17px 0px 0px 0px; color:#A73335;">Conclusion</div>
            <div class="gradient" style="background: linear-gradient(10deg, #A73335, white); height:5px; margin:7px 0px;"></div>
            <p>{quest_parts[5].strip(' :#')}</p>
            </div>
        </div>
        """

        # <span style = "font-weight:bold;font-style:italic;"></span>
        components.html(quest_tile, height=1200, scrolling=False)
        
        if st.session_state.quests:
            custom_css = """
            .gradient {
                background: linear-gradient(10deg, #A73335, white);
                height:5px;
                margin:7px 0px;
            }
            .name {
                font-size:225%;
                font-family:Georgia, serif;
                font-variant:small-caps;
                font-weight:bold;
                color:#A73335;
            }
            .description {
                font-style:italic;    
            }
            .bold {
                font-weight:bold;
            }
            .red {
                color:#A73335;
            }
            table {
                width:100%;
                border:0px;
                border-collapse:collapse;
                color:#A73335;
            }
            th, td {
                width:50px;
                text-align:center;
            }
            .actions {
                font-size:175%;
                font-variant:small-caps;
                margin:17px 0px 0px 0px;
            }
            .hr {
                background: #A73335;
                height:2px;
            }
            .attack {
                margin:5px 0px;
            }
            .attackname {
                font-weight:bold;
                font-style:italic;
            }       
            .quest-tile {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 7.5px;  /* Increased bevel on corners by 50% */
                margin-right: 10px;
                padding: 20px;
                min-width: 95%;
                max-width: 95%;
                flex: 0 0 auto;
                scroll-snap-align: start;
                white-space: normal;
            }
            """


if __name__ == "__main__":
    main()
