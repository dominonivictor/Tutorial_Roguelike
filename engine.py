import tcod
from TheGame import TheGame
from interface.console import Console, Panel

'''
I can clean this up even further! :) maybe with one single func
'''

def main():

    the_game = TheGame()
    con = Console()
    panel = Panel()
   
    while not tcod.console_is_window_closed():

        the_game.check_event()

        con.render_console(panel, the_game.god, the_game.player, the_game.entities, 
                    the_game.game_map, the_game.fov_map, the_game.fov_recompute,
                    the_game.msg_log)

        #This is very ugly and temporary, until i find out how to properly close the window
        exit = the_game.update()

        if exit:
            return True

if __name__ == '__main__':
    main()