"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    while True:
        choice = input("Choose an option (1-3): ").strip()

        if choice in ("1", "2", "3"):
            return int(choice)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    
    global current_character
    
    print("\n=== CREATE NEW CHARACTER ===")
    name = input("Enter your character name: ").strip()
    char_class = input("Enter your class (warrior/mage/rogue): ").strip()

    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"Character '{name}' created successfully!")

        

    except InvalidCharacterClassError:
        print(f"ERROR: '{char_class}' is not a valid character class.")
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    # Give starting items
    inventory_system.add_item_to_inventory(current_character, "health_potion", all_items)
    inventory_system.add_item_to_inventory(current_character, "iron_sword", all_items)

    if "first_steps" in all_quests:
        quest_handler.accept_quest(current_character, "first_steps", all_quests)

    game_loop()

    

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    print("\n=== LOAD GAME ===")

    saved = character_manager.list_saved_characters()

    if not saved:
        print("No saved characters found.")
        return

    print("Saved Characters:")
    for i, char_name in enumerate(saved, start=1):
        print(f"{i}. {char_name}")

    while True:
        choice = input("Select a character number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(saved):
            chosen_name = saved[int(choice) - 1]
            break
        else:
            print("Invalid choice. Try again.")

    try:
        current_character = character_manager.load_character(chosen_name)
        print(f"Loaded character '{chosen_name}' successfully!")

        game_loop()

    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"ERROR: {e}")
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        print("\n=== GAME MENU ===")
        choice = game_menu()
        
        try:
            if choice == 1:
                view_character_stats()
            elif choice == 2:
                view_inventory()
            elif choice == 3:
                quest_menu()
            elif choice == 4:
                explore()
            elif choice == 5:
                shop()
            elif choice == 6:
                save_game()
                print("Game saved! Exiting to main menu.")
                game_running = False
            else:
                print("Invalid choice. Please select 1-6.")
        except Exception as e:
            print(f"An error occurred: {e}")
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    while True:
        choice = input("Choose an action (1-6): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return int(choice)
        print("Invalid choice. Enter a number 1-6.")


    # TODO: Implement game menu
    

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    while True:
        choice = input("Choose an action (1-6): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return int(choice)
        print("Invalid choice. Enter a number 1-6.")

    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    
    # Show quest progress using quest_handler
    display_character_quest_progress(current_character, all_quests)
    

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    while True:
        print(f"\n=== {current_character['name']}'s Inventory ===")
        inventory_system.display_inventory(current_character, all_items)
        print("\nOptions:")
        print("1. Use Item")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Drop Item")
        print("5. Back to Game Menu")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            item_id = input("Enter the item ID to use: ").strip()
            try:
                result = inventory_system.use_item(current_character, item_id, all_items)
                print(result)
            except (inventory_system.ItemNotFoundError, inventory_system.InvalidItemTypeError) as e:
                print(f"ERROR: {e}")
        elif choice == "2":
            item_id = input("Enter weapon ID to equip: ").strip()
            try:
                result = inventory_system.equip_weapon(current_character, item_id, all_items)
                print(result)
            except (inventory_system.ItemNotFoundError, inventory_system.InvalidItemTypeError) as e:
                print(f"ERROR: {e}")
        elif choice == "3":
            item_id = input("Enter armor ID to equip: ").strip()
            try:
                result = inventory_system.equip_armor(current_character, item_id, all_items)
                print(result)
            except (inventory_system.ItemNotFoundError, inventory_system.InvalidItemTypeError) as e:
                print(f"ERROR: {e}")
        elif choice == "4":
            item_id = input("Enter item ID to drop: ").strip()
            try:
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"{item_id} removed from inventory.")
            except inventory_system.ItemNotFoundError as e:
                print(f"ERROR: {e}")
        elif choice == "5":
            break
        else:
            print("Invalid choice, try again.")
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    while True:
        print("\n=== Quest Menu ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back to Game Menu")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            active = quest_handler.get_active_quests(current_character, all_quests)
            quest_handler.display_quest_list(active)
        elif choice == "2":
            available = quest_handler.get_available_quests(current_character, all_quests)
            quest_handler.display_quest_list(available)
        elif choice == "3":
            completed = quest_handler.get_completed_quests(current_character, all_quests)
            quest_handler.display_quest_list(completed)
        elif choice == "4":
            quest_id = input("Enter quest ID to accept: ").strip()
            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' accepted!")
            except Exception as e:
                print(f"ERROR: {e}")
        elif choice == "5":
            quest_id = input("Enter quest ID to abandon: ").strip()
            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' abandoned.")
            except Exception as e:
                print(f"ERROR: {e}")
        elif choice == "6":
            quest_id = input("Enter quest ID to complete: ").strip()
            try:
                rewards = quest_handler.complete_quest(current_character, quest_id, all_quests)
                print(f"Quest completed! Rewards: {rewards}")
            except Exception as e:
                print(f"ERROR: {e}")
        elif choice == "7":
            break
        else:
            print("Invalid choice, enter 1-7.")
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    

import random
import combat_system
import inventory_system

def explore():
    """Find and fight random enemies"""
    global current_character, all_items
    
    print("\nYou venture into the wilds...")

    # Generate a random enemy based on character level
    player_level = current_character.get("level", 1)
    
    # Simple enemy template: scale stats with player level
    enemy = {
        "name": f"Goblin Lv{player_level}",
        "health": 20 + player_level * 5,
        "max_health": 20 + player_level * 5,
        "strength": 5 + player_level * 2,
        "magic": 0,
        "gold": random.randint(5, 15) + player_level * 2,
        "level": player_level,
        "inventory": [],  # Enemy could drop items later
    }

    print(f"A wild {enemy['name']} appears!")
    
    # Start combat using combat_system
    try:
        result = combat_system.SimpleBattle(current_character, enemy)
        # Assume result is a dict with a "winner" key
        if result["winner"] == "player":
            print(f"You defeated {enemy['name']}!")
            xp_reward = result.get("xp", 10 + player_level * 5)
            gold_reward = result.get("gold", enemy["gold"])
            current_character["gold"] = current_character.get("gold", 0) + gold_reward
            print(f"You earned {xp_reward} XP and {gold_reward} gold.")
            
            # Add item drops (let exceptions propagate for testing)
            if "loot" in result and result["loot"]:
                for item_id in result["loot"]:
                    inventory_system.add_item_to_inventory(current_character, item_id, all_items)
                    print(f"You found an item: {item_id}")

        else:
            print("You were defeated...")
            handle_character_death()

    except inventory_system.InventoryFullError:
        print("Inventory full! Could not pick up some items.")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    while True:
        print("\n=== Shop Menu ===")
        print(f"Gold: {current_character.get('gold', 0)}")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back to Game Menu")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            item_id = input("Enter item ID to buy: ").strip()
            try:
                inventory_system.purchase_item(current_character, item_id, all_items)
                print(f"Purchased {item_id}!")
            except Exception as e:
                print(f"ERROR: {e}")
        elif choice == "2":
            item_id = input("Enter item ID to sell: ").strip()
            try:
                gold = inventory_system.sell_item(current_character, item_id, all_items)
                print(f"Sold {item_id} for {gold} gold.")
            except Exception as e:
                print(f"ERROR: {e}")
        elif choice == "3":
            break
        else:
            print("Invalid choice, enter 1-3.")
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    if not current_character:
        print("No character to save.")
        return

    try:
        character_manager.save_character(current_character)
        print(f"Character '{current_character['name']}' saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
    except (MissingDataFileError, InvalidDataFormatError):
        print("Quests missing or invalid. Creating default quests...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()

    try:
        all_items = game_data.load_items()
    except (MissingDataFileError, InvalidDataFormatError):
        print("Items missing or invalid. Creating default items...")
        game_data.create_default_data_files()
        all_items = game_data.load_items()
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print("\nYou have been defeated!")
    if current_character.get("gold", 0) >= 50:  # Example revive cost
        choice = input("Spend 50 gold to revive? (y/n): ").strip().lower()
        if choice == "y":
            current_character["gold"] -= 50
            character_manager.revive_character(current_character)
            print("You have been revived!")
            return
    print("Game Over. Returning to main menu.")
    game_running = False
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # -----------------------------
    # Ensure default data exists
    # -----------------------------
    game_data.create_default_data_files()  # Creates data/ folder + default items/quests
    
    # -----------------------------
    # Load quests and items into memory
    # -----------------------------
    load_game_data()  # Populates all_quests and all_items

    try:
        print("Game data loaded successfully!")
    except (MissingDataFileError, InvalidDataFormatError) as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # -----------------------------
    # Main menu loop
    # -----------------------------
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

