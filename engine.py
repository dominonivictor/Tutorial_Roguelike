import tcod
from TheGame import TheGame
from interface.console import Console, Panel, render_console

'''
I can clean this up even further! :) maybe with one single func
'''

def main():

    the_game = TheGame()
    con = Console()
    pan = Panel()
   
    while not tcod.console_is_window_closed():

        the_game.check_event()

        render_console(con.console, pan.panel, the_game.god, the_game.player, the_game.entities, 
                    the_game.game_map, the_game.fov_map, the_game.fov_recompute,
                    the_game.msg_log, the_game.mouse, the_game.game_state)

        #This is very ugly and temporary, until i find out how to properly close the window
        exit = the_game.update()

        if exit:
            return True

if __name__ == '__main__':
    main()