


class Action:
    pass

    self.name = 'nothing'
    self.description = 'descriptive nothing'
    self.fail_msg = 'You failed'
    self.succeed_msg = 'You succeeded'

    def perform(self):
        print('Action class perform, smt went wrong')

    def fail():
        '''
        well there are 2 types of fails...
        1 cause u missed
        2 cause it is invalid
        '''


    def succeed():
        '''
        if succeeded, we can apply the time it took to perform the action
        '''

class BreakWall(Action):
    '''
    Ok so main goal is to return an action obj
    '''
    pass
    self.name = 'Wall Breaker'
    self.fail_msg = "You couldn't break the wall"
    self.succeed_msg = 'You broke the wall'

    def perform(self):
        pass
        '''
        ok what do i need? check if there are entities, update fov_map and game_map,
        a direction/position
        '''
        entities = 
        game_map = 
        fov_map =
        fov_recompute = 

        target_x = 
        target_y = 

        wall = the_game.game_map.tiles[target_x][target_y].blocked
        if not wall:#there is a wall here
            msg = Message('There is no wall to break here', tcod.yellow)
            results.append({'acted': False, 'message':msg})
        elif wall:
            msg = Message('CRUNCH! A wall is broken', tcod.light_green)
            results.append({'acted': True, 'message': msg})
            game_map.tiles[target_x][target_y].destroy_wall()
            fov_map = set_tile_fov(target_x, target_y, game_map, fov_map)
            fov_recompute = True #do i need to do this here??

        return results