from game_states import GameStates
from functions.pc_actions import process_player_turn_results

def show_inventory_action(the_game):
    the_game.prev_game_state = the_game.game_state
    the_game.game_state = GameStates.SHOW_INVENTORY

def inventory_index_action(the_game, inventory_index):
    player_turn_results = []
    item = the_game.player.inventory.items[inventory_index]
    if the_game.game_state == GameStates.SHOW_INVENTORY:
        player_turn_results.extend(the_game.player.inventory.use(item, entities=the_game.entities, fov_map=the_game.fov_map))
    elif the_game.game_state == GameStates.DROP_INVENTORY:
        player_turn_results.extend(the_game.player.inventory.drop_item(item))

    process_player_turn_results(the_game, player_turn_results)

def drop_inventory_action(the_game):
    the_game.prev_game_state = the_game.game_state
    the_game.game_state = GameStates.DROP_INVENTORY