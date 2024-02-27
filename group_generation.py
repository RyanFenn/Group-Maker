
import random

PLAYER_FIRST_NAME_INDEX = 0
PLAYER_LAST_NAME_INDEX = 1
PLAYER_VETERAN_INDEX = 2
PLAYER_SKILL_INDEX = 3
PLAYER_AVAILABILITY_INDEX = 4   # This item is appended during group generation.

MAX_SKILL_LEVEL = 3

# This dictionary is used to convert keys within player_select_priority to index values.
convert_key_to_index_dict = { 'veteran': PLAYER_VETERAN_INDEX, 'skill': PLAYER_SKILL_INDEX, 'availability': PLAYER_AVAILABILITY_INDEX }

# - The player select priority list is the order in which players will be selected for groups. Players that match the
#   values from the first index get selected first. The second index is the next highest priority, and so on. Selected
#   players will be distributed to groups evenly.
# - Only veterans that have a skill level of 3 are balanced evenly if enabled.
def get_player_select_priority_list(en_veteran_balancing: bool, en_skill_balancing: bool) -> list:

    player_select_priority = []

    # - Prioritizing players who are potentially available. Because of the way players are added to groups, the last group
    #   will have the least amount of players, unless the groups are split perfectly even. Knowing that the last group
    #   is most likely to have less players, less potential players should be in this group to give the best chance of
    #   having even groups.
    # - Also note that the prioritization of skill levels goes from highest to lowest for potential players, and lowest
    #   to highest for available players so that the lowest level players are distributed evenly.

    if en_veteran_balancing and en_skill_balancing:
        player_select_priority = [
            { 'skill': 3, 'availability': 'potential' },
            { 'skill': 2, 'availability': 'potential' },
            { 'skill': 1, 'availability': 'potential' },
            { 'skill': 1, 'availability': 'available'}, 
            { 'skill': 2, 'availability': 'available' },
            { 'skill': 3, 'availability': 'available', 'veteran': True },
            { 'skill': 3, 'availability': 'available', 'veteran': False }]

    elif en_veteran_balancing and not en_skill_balancing:
        player_select_priority = [
            { 'availability': 'potential' },
            { 'availability': 'available', 'veteran': True },
            { 'availability': 'available', 'veteran': False }]

    elif not en_veteran_balancing and en_skill_balancing:
        player_select_priority = [
            { 'skill': 3, 'availability': 'potential' },
            { 'skill': 2, 'availability': 'potential' },
            { 'skill': 1, 'availability': 'potential' },
            { 'skill': 1, 'availability': 'available' },
            { 'skill': 2, 'availability': 'available' },
            { 'skill': 3, 'availability': 'available' }]

    elif not en_veteran_balancing and not en_skill_balancing:
        player_select_priority = [
            { 'availability': 'potential' },
            { 'availability': 'available' }]        

    return player_select_priority

# enable_name_formatting -> When true, potential players will have parenthesis around the first and last name
#                           and veteran players will have an asterisk (*) in front of their first name.
def print_groups(groups, enable_name_formatting):

    for group in groups:
        for player in group:
            temp_string = f'{player[PLAYER_FIRST_NAME_INDEX]} {player[PLAYER_LAST_NAME_INDEX]}'

            if enable_name_formatting:

                try:
                    # If potential player, add parenthesis around the first ane last name.
                    # The availability element should have been appended when merging the available and potential players into one list.
                    if player[PLAYER_AVAILABILITY_INDEX] == 'potential':
                        temp_string = '(' + temp_string + ')'
                
                except IndexError:
                    print('ERROR: Availability status data was not added to the player list.')
                    raise SystemExit

                # If veteran player, add asterisk (*) to the start of the string.
                if player[PLAYER_VETERAN_INDEX] == True:
                    temp_string = '*' + temp_string

            print(temp_string)
        print()

# - This function/method is used to cycle between all of the groups so that players can be added to groups evenly.
# - Returns the next group index.
def get_next_group_index(current_index, number_of_groups):
    next_index = current_index + 1
    
    if next_index >= number_of_groups:
        next_index = 0
        
    return next_index

# Generates a list of lists to group players. Each group will have a list of players.
def generate_list(number_of_groups: int, available_players: list, potential_players: list, en_veteran_balancing: bool,
    en_skill_balancing: bool) -> list:

    groups = [[] for _ in range(number_of_groups)]   # Initializing lists within list.
    players = []

    # Add all available players to the players list, while also setting the availility status to "available".
    # The availability status item should have an index number of 4 (PLAYER_AVAILABILITY_INDEX).
    for available_player in available_players:
        try:
            available_player[PLAYER_AVAILABILITY_INDEX] = 'available'
        except IndexError:
            available_player.append('available')

        players.append(available_player)

    # Add all potential players to the players list, while also setting the availility status to "potential".
    # The availability status item should have an index number of 4 (PLAYER_AVAILABILITY_INDEX).
    for potential_player in potential_players:
        try:
            potential_player[PLAYER_AVAILABILITY_INDEX] = 'potential'
        except IndexError:
            potential_player.append('potential')

        players.append(potential_player)

    random.shuffle(players)

    player_select_priority = get_player_select_priority_list(en_veteran_balancing, en_skill_balancing)

    # Initialized value should be -1. This value will be incremented by 1 when get_next_group_index is called.
    current_group_index = -1

    while len(players) > 0:
        
        for player_index in range(len(players)):
     
            is_player_qualified = True   # Does the player match the player select priority qualifications.
            for key in player_select_priority[0]:   # The keys are 'skill', 'availability', and 'veteran'.

                if players[player_index][convert_key_to_index_dict[key]] != player_select_priority[0][key]:
                    is_player_qualified = False
                    break
        
            if is_player_qualified:
                current_group_index = get_next_group_index(current_group_index, number_of_groups)
                print(f'Added player to group : {players[player_index]}')
                groups[current_group_index].append(players[player_index])
                del players[player_index]
                break   # Breaks out of the player for loop.

            # Reached the last player in the list and none of the players match the current qualifications.
            elif player_index == len(players)-1:
                del player_select_priority[0]   # Deletes the first item in the list because no players meet the qualifications.
                
        if len(player_select_priority) == 0 and len(players) > 0:
        
            # To fix this error, make sure every player meets the qualifications of one of the player_select_priority options.
            print('\nERROR: One or more players could not be added to a group.')
            raise SystemExit            

    return groups




