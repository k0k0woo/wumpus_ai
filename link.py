import random
from utils import Directions, Pose
from collections import deque
import heapq
import math
class Link():

    def __init__(self, dungeon):
        self.gameWorld = dungeon
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        self.visited = set()

    def checkvalid(self, pos, allow_windy=False):
        """
        Determines if a position is safe for Link to move into.
        
        :param pos: Position object representing the next move.
        :param allow_windy: If True, allows movement into windy squares.
        :return: True if the position is safe, False otherwise.
        """

        if self.gameWorld.isSmelly(pos):  # Smelly tiles indicate proximity to Wumpus
            print(f"Avoiding Smelly tile at ({pos.x}, {pos.y})")
            return False
        if not allow_windy and self.gameWorld.isWindy(pos):  # Windy tiles indicate proximity to a pit
            print(f"Avoiding Windy tile at ({pos.x}, {pos.y})")
            return False
        if any(pos.x == wumpus.x and pos.y == wumpus.y for wumpus in self.gameWorld.getWumpusLocation()): # Tile checked if it contains wumpus
            print(f"Avoiding Wumpus at ({pos.x}, {pos.y})")
            return False
        if any(pos.x == pit.x and pos.y == pit.y for pit in self.gameWorld.getPitsLocation()): # Tile checked if it contains pit
            print(f"Avoiding Pit at ({pos.x}, {pos.y})")
            return False
        return True

    def bfs_search(self, start, goal, allow_windy=False):
        """
        Finds the shortest path from start to goal while avoiding dangers using Breadth-First Search.
        
        :param start: Starting position of Link.
        :param goal: Target position (gold location).
        :param allow_windy: If True, allows Link to move through windy tiles.
        :return: A list of moves representing the shortest safe path, or an empty list if no path is found.
        """
        queue = deque([(start, [])]) # create queue (position,path-to-reach)
        visited = set()
        
        while queue:
            (current, path) = queue.popleft()
            if (current.x, current.y) in visited:
                continue
            
            visited.add((current.x, current.y))
            
            if current.x == goal.x and current.y == goal.y:
                return path # valid path to gold found
            
            for move in self.moves:
                new_pos = self.getNewPosition(current, move)
                
                if (0 <= new_pos.x <= self.gameWorld.maxX and
                    0 <= new_pos.y <= self.gameWorld.maxY and
                    self.checkvalid(new_pos, allow_windy) and
                    (new_pos.x, new_pos.y) not in visited):

                    # if move results in valid and safe position not already added
                    queue.append((new_pos, path + [move])) # add position and path to queue
        
        return []  # No valid path found
    
    def dfs_search(self, start, goal, allow_windy=False):
        """
        Finds the shortest path from start to goal while avoiding dangers using Breadth-First Search.
        
        :param start: Starting position of Link.
        :param goal: Target position (gold location).
        :param allow_windy: If True, allows Link to move through windy tiles.
        :return: A list of moves representing the shortest safe path, or an empty list if no path is found.
        """
        stack = deque([(start, [])]) # create queue (position,path-to-reach)
        visited = set()
        
        while stack:
            (current, path) = stack.pop(-1)
            if (current.x, current.y) in visited:
                continue
            
            visited.add((current.x, current.y))
            
            if current.x == goal.x and current.y == goal.y:
                return path # valid path to gold found
            
            for move in self.moves:
                new_pos = self.getNewPosition(current, move)
                
                if (0 <= new_pos.x <= self.gameWorld.maxX and
                    0 <= new_pos.y <= self.gameWorld.maxY and
                    self.checkvalid(new_pos, allow_windy) and
                    (new_pos.x, new_pos.y) not in visited):

                    # if move results in valid and safe position not already added
                    stack.append((new_pos, path + [move])) # add position and path to queue
        
        return []  # No valid path found

    def makeMove(self):
        """
        Determines Link's next move based on a dynamic decision-making process.
        Prioritizes escaping danger, then finding the safest path to gold.
        
        :return: The next move direction.
        """
        myPosition = self.gameWorld.getLinkLocation()
        allGold = self.gameWorld.getGoldLocation()

        # determine closest gold via euclidian distance difference
        nextGold = allGold[0]  
        for gold in allGold:
            if (abs(myPosition.x-nextGold.x) + abs(myPosition.y-nextGold.y)) > (abs(gold.x-nextGold.x) + abs(gold.y-nextGold.y)):
                nextGold = gold

        print(f"Finding safe path from {myPosition.x},{myPosition.y} to gold at {nextGold.x},{nextGold.y}")
        
        path = self.A_star_search(myPosition, nextGold, allow_windy=False) # initial path to avoid windy squares
        
        if not path:
            print("No fully safe path found, allowing windy tiles...")
            path = self.A_star_search(myPosition, nextGold, allow_windy=True) # if no safe path try again allowing windy tiles
        
        if path:
            print(f"Path found: {path}") # follow move of path
            next_move = path[0]
            return next_move
        
        # If no clear path is found, make a safe random move
        safe_moves = [move for move in self.moves if self.checkvalid(self.getNewPosition(myPosition, move), allow_windy=True)]
        if not safe_moves:
            print("No safe moves found, making a random move.")
            return random.choice(self.moves) # completely random move
        
        chosen_move = random.choice(safe_moves) # random move from safe squares
        print(f"No path found, moving {chosen_move}")
        return chosen_move
    
    def uniform_cost(self, start, goal,allow_windy=False):
        """
        Uses uniform cost to find a path from start to goal.
        
        :param start: The starting position
        :param goal: The target position
        :return: A list of directional moves to reach the goal
        """
        queue = [] # init stack
        heapq.heappush(queue,(start, []))
        visited = set() # init visited
        while queue: # while moves in stack
            (current,path) = heapq.heappop(queue) # get item
            if (current.x, current.y) in visited: # if already visited
                continue # skip
            
            visited.add((current.x, current.y)) # add to visited
            
            if current.x == goal.x and current.y == goal.y: # if current is goal
                return path# append to complete paths array
            
            for move in self.moves: # for each move
                new_pos = self.getNewPosition(current, move) # get possible new position
                if (0 <= new_pos.x <= self.gameWorld.maxX and 0 <= new_pos.y <= self.gameWorld.maxY and (new_pos.x, new_pos.y) not in visited and self.checkvalid(new_pos, allow_windy)): # if valid and not visited
                    heapq.heappush(queue, (new_pos, path + [move]))# append to the queue

        else:
            return []
        
    def greedy_search(self, start, goal,allow_windy=False):
        """
        Uses gready search to find a path from start to goal.
        
        :param start: The starting position
        :param goal: The target position
        :return: A list of directional moves to reach the goal
        """
        queue = [] # init stack
        heapq.heappush(queue,(start, []))
        visited = set() # init visited
        while queue: # while moves in stack
            (current,path) = heapq.heappop(queue) # get item
            if (current.x, current.y) in visited: # if already visited
                continue # skip
            
            visited.add((current.x, current.y)) # add to visited
            
            if current.x == goal.x and current.y == goal.y: # if current is goal
                return path# append to complete paths array
            
            for move in self.moves: # for each move
                new_pos = self.getNewPosition(current, move) # get possible new position
                new_pos.cost = math.sqrt(abs(new_pos.x-goal.x)**2 + abs(new_pos.y-goal.y)**2) # euclidian to goal
                if (0 <= new_pos.x <= self.gameWorld.maxX and 0 <= new_pos.y <= self.gameWorld.maxY and (new_pos.x, new_pos.y) not in visited and self.checkvalid(new_pos, allow_windy)): # if valid and not visited
                    heapq.heappush(queue, (new_pos, path + [move]))# append to the queue

        else:
            return []

    def A_star_search(self, start, goal,allow_windy=False):
        """
        Uses A star search to find a path from the start to the goal
        
        creating with help from:
        https://www.geeksforgeeks.org/a-search-algorithm-in-python/

        :param start: The starting position
        :param goal: The target position
        :return: A list of directional moves to reach the goal
        """
        queue = [] # init stack
        heapq.heappush(queue,(start, []))
        visited = set() # init visited
        while queue: # while moves in stack
            (current,path) = heapq.heappop(queue) # get item
            if (current.x, current.y) in visited: # if already visited
                continue # skip
            
            visited.add((current.x, current.y)) # add to visited
            
            if current.x == goal.x and current.y == goal.y: # if current is goal
                return path# append to complete paths array
            
            for move in self.moves: # for each move
                new_pos = self.getNewPosition(current, move) # get possible new position
                # add euclidian cost
                new_pos_euclidian = math.sqrt(abs(new_pos.x-goal.x)**2 + abs(new_pos.y-goal.y)**2) # euclidian to goal
                new_pos.cost += new_pos_euclidian
                if (0 <= new_pos.x <= self.gameWorld.maxX and 0 <= new_pos.y <= self.gameWorld.maxY and (new_pos.x, new_pos.y) not in visited and self.checkvalid(new_pos, allow_windy)): # if valid and not visited
                    heapq.heappush(queue, (new_pos, path + [move]))# append to the queue

        else:
            return []
    def getNewPosition(self, position, move):
        """
        Calculates the new position based on the current position and move direction.
        
        :param position: The current position of Link.
        :param move: The direction of movement.
        :return: The new position after moving.
        """
        newPosition = Pose()
        newPosition.x = position.x + (1 if move == Directions.EAST else -1 if move == Directions.WEST else 0)
        newPosition.y = position.y + (1 if move == Directions.NORTH else -1 if move == Directions.SOUTH else 0)

        newPosition.cost = abs(newPosition.x-position.x) + abs(newPosition.y-position.y) + position.cost
        return newPosition