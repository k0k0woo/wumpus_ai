import random
from utils import Directions, Pose
from collections import deque

class Link():

    def __init__(self, dungeon):
        self.gameWorld = dungeon
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        self.visited = set()

    def checkvalid(self, pos, allow_windy=False):
        """Check if the move is safe (not smelly, windy, out of bounds, containing Wumpus or Pit)."""
        if self.gameWorld.isSmelly(pos):
            print(f"Avoiding Smelly tile at ({pos.x}, {pos.y})")
            return False
        if not allow_windy and self.gameWorld.isWindy(pos):
            print(f"Avoiding Windy tile at ({pos.x}, {pos.y})")
            return False
        if any(pos.x == wumpus.x and pos.y == wumpus.y for wumpus in self.gameWorld.getWumpusLocation()):
            print(f"Avoiding Wumpus at ({pos.x}, {pos.y})")
            return False
        if any(pos.x == pit.x and pos.y == pit.y for pit in self.gameWorld.getPitsLocation()):
            print(f"Avoiding Pit at ({pos.x}, {pos.y})")
            return False
        return True

    def bfs_search(self, start, goal, allow_windy=False):
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
                    self.checkvalid(new_pos, allow_windy) and
                    (new_pos.x, new_pos.y) not in visited):
                    queue.append((new_pos, path + [move]))
        
        return []  # No valid path found

    def makeMove(self):
        """Determines the best move using BFS while ensuring safety dynamically."""
        myPosition = self.gameWorld.getLinkLocation()
        allGold = self.gameWorld.getGoldLocation()

        if not allGold:
            print("No more gold left!")
            return random.choice(self.moves)

        nextGold = allGold[0]  # Target the closest gold
        print(f"Finding safe path from {myPosition.x},{myPosition.y} to gold at {nextGold.x},{nextGold.y}")
        
        path = self.bfs_search(myPosition, nextGold, allow_windy=False)
        
        if not path:
            print("No fully safe path found, allowing windy tiles...")
            path = self.bfs_search(myPosition, nextGold, allow_windy=True)
        
        if path:
            print(f"Path found: {path}")
            next_move = path[0]
            new_position = self.getNewPosition(myPosition, next_move)
            return next_move
        
        # If no clear path is found, make a safe random move
        safe_moves = [move for move in self.moves if self.checkvalid(self.getNewPosition(myPosition, move), allow_windy=True)]
        if not safe_moves:
            print("No safe moves found, making a random move.")
            return random.choice(self.moves)
        
        chosen_move = random.choice(safe_moves)
        print(f"No path found, moving {chosen_move}")
        return chosen_move

    def getNewPosition(self, position, move):
        """Get new position based on movement direction."""
        newPosition = Pose()
        newPosition.x = position.x + (1 if move == Directions.EAST else -1 if move == Directions.WEST else 0)
        newPosition.y = position.y + (1 if move == Directions.NORTH else -1 if move == Directions.SOUTH else 0)
        return newPosition