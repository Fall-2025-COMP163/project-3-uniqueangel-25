"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    quests = {}
    with open(filename, "r", encoding="utf-8") as f:
        current_quest = {}
        for line in f:
            line = line.strip()
            if not line:
                if "QUEST_ID" in current_quest:
                    quests[current_quest["QUEST_ID"]] = current_quest
                current_quest = {}
            else:
                key, value = line.split(":", 1)
                current_quest[key.strip()] = value.strip()
        if "QUEST_ID" in current_quest:
            quests[current_quest["QUEST_ID"]] = current_quest
    return quests
    
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    items = {}
    with open(filename, "r", encoding="utf-8") as f:
        current_item = {}
        for line in f:
            line = line.strip()
            if not line:
                if "ITEM_ID" in current_item:
                    items[current_item["ITEM_ID"]] = current_item
                current_item = {}
            else:
                key, value = line.split(":", 1)
                current_item[key.strip()] = value.strip()
        # Add last item if file does not end with blank line
        if "ITEM_ID" in current_item:
            items[current_item["ITEM_ID"]] = current_item
    return items
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required_fields = [
        "quest_id", "title", "description", 
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]
    for key in required_fields:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing quest field: {key}")

    # Check numeric fields
    try:
        quest_dict["reward_xp"] = int(quest_dict["reward_xp"])
        quest_dict["reward_gold"] = int(quest_dict["reward_gold"])
        quest_dict["required_level"] = int(quest_dict["required_level"])
    except Exception:
        raise InvalidDataFormatError("Numeric quest fields must be integers.")

    return True
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for key in required_fields:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    try:
        item_dict["cost"] = int(item_dict["cost"])
    except Exception:
        raise InvalidDataFormatError("Item cost must be an integer.")

    return True
    # TODO: Implement validation
    

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    import os

    os.makedirs("data", exist_ok=True)

    # ------------------------------
    # Default items
    # ------------------------------
    default_items = [
        {
            "ITEM_ID": "health_potion",
            "NAME": "Health Potion",
            "TYPE": "consumable",
            "EFFECT": "health:20",
            "COST": "25",
            "DESCRIPTION": "Restores 20 health points"
        },
        {
            "ITEM_ID": "iron_sword",
            "NAME": "Iron Sword",
            "TYPE": "weapon",
            "EFFECT": "strength:5",
            "COST": "50",
            "DESCRIPTION": "A basic iron sword"
        },
        {
            "ITEM_ID": "expensive_item",
            "NAME": "Expensive Sword",
            "TYPE": "weapon",
            "EFFECT": "strength:50",
            "COST": "100",
            "DESCRIPTION": "A very expensive weapon"
        },
    ]

    items_file = "data/items.txt"
    existing_item_ids = set()

    # Read existing items if file exists
    if os.path.exists(items_file):
        with open(items_file, "r", encoding="utf-8") as f:
            content = f.read()
            for item in default_items:
                if f"ITEM_ID: {item['ITEM_ID']}" in content:
                    existing_item_ids.add(item['ITEM_ID'])

    # Append missing items
    with open(items_file, "a", encoding="utf-8") as f:
        for item in default_items:
            if item["ITEM_ID"] not in existing_item_ids:
                f.write(
                    f"ITEM_ID: {item['ITEM_ID']}\n"
                    f"NAME: {item['NAME']}\n"
                    f"TYPE: {item['TYPE']}\n"
                    f"EFFECT: {item['EFFECT']}\n"
                    f"COST: {item['COST']}\n"
                    f"DESCRIPTION: {item['DESCRIPTION']}\n\n"
                )

    # ------------------------------
    # Default quests
    # ------------------------------
    default_quests = [
        {
            "QUEST_ID": "first_steps",
            "TITLE": "First Steps",
            "DESCRIPTION": "Complete your first adventure",
            "REWARD_XP": "25",
            "REWARD_GOLD": "15",
            "REQUIRED_LEVEL": "1",
            "PREREQUISITE": "NONE"
        },
        {
            "QUEST_ID": "test_quest",
            "TITLE": "Test Quest",
            "DESCRIPTION": "A test quest",
            "REWARD_XP": "50",
            "REWARD_GOLD": "25",
            "REQUIRED_LEVEL": "1",
            "PREREQUISITE": "NONE"
        },
    ]

    quests_file = "data/quests.txt"
    existing_quest_ids = set()

    if os.path.exists(quests_file):
        with open(quests_file, "r", encoding="utf-8") as f:
            content = f.read()
            for quest in default_quests:
                if f"QUEST_ID: {quest['QUEST_ID']}" in content:
                    existing_quest_ids.add(quest['QUEST_ID'])

    with open(quests_file, "a", encoding="utf-8") as f:
        for quest in default_quests:
            if quest["QUEST_ID"] not in existing_quest_ids:
                f.write(
                    f"QUEST_ID: {quest['QUEST_ID']}\n"
                    f"TITLE: {quest['TITLE']}\n"
                    f"DESCRIPTION: {quest['DESCRIPTION']}\n"
                    f"REWARD_XP: {quest['REWARD_XP']}\n"
                    f"REWARD_GOLD: {quest['REWARD_GOLD']}\n"
                    f"REQUIRED_LEVEL: {quest['REQUIRED_LEVEL']}\n"
                    f"PREREQUISITE: {quest['PREREQUISITE']}\n\n"
                )
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest = {}
    try:
        for line in lines:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            mapping = {
                "quest_id": "quest_id",
                "title": "title",
                "description": "description",
                "reward_xp": "reward_xp",
                "reward_gold": "reward_gold",
                "required_level": "required_level",
                "prerequisite": "prerequisite"
            }
            if key not in mapping:
                raise InvalidDataFormatError(f"Unknown quest field: {key}")
            quest[mapping[key]] = value
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")

    return quest
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}
    try:
        for line in lines:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            mapping = {
                "item_id": "item_id",
                "name": "name",
                "type": "type",
                "effect": "effect",
                "cost": "cost",
                "description": "description"
            }
            if key not in mapping:
                raise InvalidDataFormatError(f"Unknown item field: {key}")
            item[mapping[key]] = value
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")

    return item
    # TODO: Implement parsing logic

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

