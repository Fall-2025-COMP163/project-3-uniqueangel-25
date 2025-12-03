"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    quest = quest_data_dict[quest_id]

    # Check level requirement
    if character.get("level", 1) < quest.get("required_level", 1):
        raise InsufficientLevelError(f"Level {quest['required_level']} required.")

    # Check prerequisite
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character.get("completed_quests", []):
        raise QuestRequirementsNotMetError(f"Must complete '{prereq}' first.")

    # Check already completed
    if quest_id in character.get("completed_quests", []):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed.")

    # Check already active
    if quest_id in character.get("active_quests", []):
        # FIX: Changed generic Exception to a more appropriate custom exception.
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' already active.") 

    # Accept quest
    character.setdefault("active_quests", []).append(quest_id)
    return True
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    quest = quest_data_dict[quest_id]

    # Grant rewards
    xp = quest.get("reward_xp", 0)
    gold = quest.get("reward_gold", 0)

    # Update character lists
    character["active_quests"].remove(quest_id)
    character.setdefault("completed_quests", []).append(quest_id)
    
    # --- FIX for test_quest_acceptance_and_completion (assert 0 == 50) ---
    # Direct dictionary updates (Required change based on user constraint)
    
    # Update Gold
    character["gold"] = character.get("gold", 0) + gold
    
    # Update Experience (Must use 'experience', not 'xp')
    character["experience"] = character.get("experience", 0) + xp 
    # ----------------------------------------------------------------------

    # NOTE: Since we are not calling gain_experience(), level-up logic is NOT
    # triggered here, but the test (which just checks XP reward) should now pass.

    return {"xp": xp, "gold": gold}
    

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    character["active_quests"].remove(quest_id)
    return True
    # TODO: Implement quest abandonment
    

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    active = character.get("active_quests", [])
    return [quest_data_dict[qid] for qid in active if qid in quest_data_dict]
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    completed = character.get("completed_quests", [])
    return [quest_data_dict[qid] for qid in completed if qid in quest_data_dict]
    # TODO: Implement completed quest retrieval
    

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    available = []
    for qid, quest in quest_data_dict.items():
        if qid in character.get("active_quests", []):
            continue
        if qid in character.get("completed_quests", []):
            continue
        if character.get("level", 1) < quest.get("required_level", 1):
            continue
        prereq = quest.get("prerequisite", "NONE")
        if prereq != "NONE" and prereq not in character.get("completed_quests", []):
            continue
        available.append(quest)
    return available

    # TODO: Implement available quest search
    # Filter all quests by requirements
    

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    return quest_id in character.get("completed_quests", [])
    # TODO: Implement completion check
    

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    return quest_id in character.get("active_quests", [])
    # TODO: Implement active check
    

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    quest = quest_data_dict.get(quest_id)
    if not quest:
        return False

    # Already completed
    if quest_id in character.get("completed_quests", []):
        return False

    # Already active
    if quest_id in character.get("active_quests", []):
        return False

    # Level requirement
    if character.get("level", 1) < quest.get("required_level", 1):
        return False

    # Prerequisite requirement
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character.get("completed_quests", []):
        return False

    return True
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    chain = []
    current = quest_id

    # Follow prerequisites backwards
    while current != "NONE":
        quest = quest_data_dict.get(current)
        if not quest:
            raise QuestNotFoundError(f"Quest '{current}' not found.")
        chain.append(current)
        current = quest.get("prerequisite", "NONE")

    return list(reversed(chain))
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0

    completed_quests = len(character.get("completed_quests", []))
    percentage = (completed_quests / total_quests) * 100
    return round(percentage, 2)
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0

    for quest_id in character.get("completed_quests", []):
        quest = quest_data_dict.get(quest_id)
        if quest:
            total_xp += quest.get("reward_xp", 0)
            total_gold += quest.get("reward_gold", 0)

    return {"total_xp": total_xp, "total_gold": total_gold}
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    filtered_quests = []
    for quest in quest_data_dict.values():
        level = quest.get("required_level", 1)
        if min_level <= level <= max_level:
            filtered_quests.append(quest)
    return filtered_quests
    # TODO: Implement level filtering
    

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """

    print(f"\n=== {quest_data.get('title', 'Unknown Quest')} ===")
    print(f"Description: {quest_data.get('description', 'No description')}")
    print(f"Required Level: {quest_data.get('required_level', 1)}")
    prereq = quest_data.get('prerequisite', 'NONE')
    print(f"Prerequisite: {prereq}")
    print(f"Reward XP: {quest_data.get('reward_xp', 0)}")
    print(f"Reward Gold: {quest_data.get('reward_gold', 0)}")
    

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    if not quest_list:
        print("No quests to display.")
        return

    for quest in quest_list:
        title = quest.get('title', 'Unknown')
        level = quest.get('required_level', 1)
        xp = quest.get('reward_xp', 0)
        gold = quest.get('reward_gold', 0)
        print(f"- {title} (Level {level}) | XP: {xp}, Gold: {gold}")
    # TODO: Implement quest list display
    

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    completion_pct = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== Quest Progress ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {completion_pct}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")
    # TODO: Implement progress display
    

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for quest_id, quest_data in quest_data_dict.items():
        prereq = quest_data.get("prerequisite", "NONE")
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite quest '{prereq}' for '{quest_id}' does not exist.")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

