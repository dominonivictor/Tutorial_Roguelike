import tcod
from TheGame import TheGame
from functions.console import Console

'''
I can clean this up even further! :) maybe with one single func
'''

def main():

    the_game = TheGame()
    con = Console()
   
    while not tcod.console_is_window_closed():

        the_game.check_event()

        con.render_console(the_game.god, the_game.player, the_game.entities, 
                    the_game.game_map, the_game.fov_map, the_game.fov_recompute)

        #This is very ugly and temporary, until i find out how to properly close the window
        exit = the_game.update()

        if exit:
            return True

if __name__ == '__main__':
    main()