# link.py
#
# The code that defines the behaviour of Link.
#
# You should be able to write the code for a simple solution to the
# game version of the Wumpus World here, getting information about the
# game state from self.gameWorld, and using makeMove() to generate the
# next move.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

import world
import random
import utils
from utils import Directions
from collections import deque

class Link():

    def __init__(self, dungeon):

        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.gameWorld = dungeon

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
    
        self.visited = set()
    # check if next posi
    def checkvalid(self,pos):
        if self.gameWorld.linkSmelly():
            print("location: [",pos.x,pos.y,"] is smelly!")
            return False
        if self.gameWorld.linkWindy():
            print("location: [",pos.x,pos.y,"] is windy!")
            return False
        if any(pos.x == wumpus.x and pos.y == wumpus.y for wumpus in self.gameWorld.getWumpusLocation()):
            print("location: [",pos.x,pos.y,"] is has wumpus!")
            return False
        if any(pos.x == wumpus.x and pos.y == wumpus.y for wumpus in self.gameWorld.getWumpusLocation()):
            print("location: [",pos.x,pos.y,"] is has pit!")
            return False
        return True
    

    def bfs_search(self, start, goal):
        """Breadth-First Search to find the shortest path to the gold while avoiding danger."""
        queue = deque([(start, [])])
        visited = set()
        
        while queue:
            (current, path) = queue.popleft()
            if (current.x, current.y) in visited:
                continue
            
            visited.add((current.x, current.y))
            
            if current.x == goal.x and current.y == goal.y:
                return path
            
            for move in self.moves:
                new_pos = self.getNewPosition(current, move)
                
                if (0 <= new_pos.x <= self.gameWorld.maxX and
                    0 <= new_pos.y <= self.gameWorld.maxY and
                    self.checkvalid(new_pos) and
                    (new_pos.x, new_pos.y) not in visited):
                    queue.append((new_pos, path + [move]))
    
    def makeMove(self):
        # This is the function you need to define
        #
        # For now we have a placeholder, which always moves Link
        # directly towards the gold.
        
        """Decides the best move for Link based on BFS pathfinding."""
        myPosition = self.gameWorld.getLinkLocation()
        allGold = self.gameWorld.getGoldLocation()

        if not allGold:
            print("No more gold left!")
            return random.choice(self.moves)

        nextGold = allGold[0]  # Target the closest gold
        path = self.bfs_search(myPosition, nextGold)

        if path:
            # Recalculate path every step to avoid outdated paths
            print(f"Path found: {path}")
            next_move = path[0]
            new_position = self.getNewPosition(myPosition, next_move)
            
            if self.checkvalid(new_position):
                return next_move
            else:
                print("Next move leads to danger, recalculating...")
                return self.makeMove()  # Recalculate if move is unsafe
        
        # If no clear path is found, make a safe random move
        safe_moves = [move for move in self.moves if self.checkvalid(self.getNewPosition(myPosition, move))]
        if not safe_moves:
            print("No safe moves found, making a random move.")
            return random.choice(self.moves)
        chosen_move = random.choice(safe_moves)
        print(f"No path found, moving {chosen_move}")
        return chosen_move

    def getNewPosition(self, position, move):
        """Get new position based on movement direction."""
        newPosition = utils.Pose()
        newPosition.x = position.x + (1 if move == Directions.EAST else -1 if move == Directions.WEST else 0)
        newPosition.y = position.y + (1 if move == Directions.NORTH else -1 if move == Directions.SOUTH else 0)
        return newPosition
