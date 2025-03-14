# puzzleWorld.py
#
# A file that represents a puzzle version of the Wumpus World, keeping
# track of the position of the Wumpus and Link.
#
# Written by: Simon Parsons
# Last Modified: 17/12/24

import utils
from world import World
from utils import Pose, Directions, State
from collections import deque
import heapq
class PuzzleWorld(World):

    def __init__(self):
        super().__init__()
        self.pLoc = []
        self.gLoc = []
        self.status = State.PLAY
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        self.plan = []
    
    def isSolved(self, goal):
        """
        Checks if the current world state matches the goal state.
        
        :param goal: The desired end state of the game
        :return: True if solved, False otherwise
        """
        if utils.sameAs(self, goal): # using sameAs check if puzzle state == goaalstate
            self.status = State.WON # chaange state to won
            print("Puzzle Over!")
            return True # return true
        return False # return false
    
    def makeAMove(self, goal):
        """
        Executes the next move in the plan if available. If no plan exists,
        it generates one first.
        
        :param goal: The target state to reach
        """
        if not self.plan: # if no plan found
            self.plan = self.generatePlan(goal) # create a plan
        
        if self.plan: # if plan found
            move = self.plan.pop(0) # get and remove next moves from plan
            print("Executing Move:", move)
            self.takeStep(move) # move characters
        else:
            print("No moves left to execute!")
    
    def generatePlan(self, goal):
        """
        Generates a sequence of moves to transition from the current state to the goal state.
        Uses BFS to determine the optimal path for Link and each Wumpus.
        
        :param goal: The target state
        :return: A list of moves in the format [Link_move, Wumpus1_move, Wumpus2_move, ...]
        """
        link_path = self.bfs_search(self.lLoc, goal.lLoc) # get links path
        wumpus_paths = [self.bfs_search(self.wLoc[i], goal.wLoc[i]) for i in range(len(self.wLoc))] # get wumpus paths
        
        max_length = max(len(link_path), max(len(path) for path in wumpus_paths)) # get length of longest path
        plan = []
        
        for i in range(max_length): # for each move
            move = []
            move.append(link_path[i] if i < len(link_path) else 0) # if move in link path append otherwise adde 0 (no move)
            for j in range(len(self.wLoc)): # for each wumpus
                move.append(wumpus_paths[j][i] if i < len(wumpus_paths[j]) else 0) # if wumpus has a move add it if not add 0 (no move) 
            plan.append(move) # add combined move to plan
        
        return plan # return complete plan
    
    def bfs_search(self, start, goal):
        """
        Uses Breadth-First Search (BFS) to find the shortest path from start to goal.
        
        :param start: The starting position
        :param goal: The target position
        :return: A list of directional moves to reach the goal
        """
        queue = deque([(start, [])]) # init queue
        visited = set() # init visited
        
        while queue: # while moves in queue
            current, path = queue.popleft() # pop first item in queue
            if (current.x, current.y) in visited: # skip if already in visited
                continue
            
            visited.add((current.x, current.y)) # add to visited
            
            if current.x == goal.x and current.y == goal.y: # if current path is goal state
                return path  # return path to square
            
            for move in self.moves: # for each direction
                new_pos = self.getNewPosition(current, move) # get new square (if you were to do the move)
                if (0 <= new_pos.x <= self.maxX and 0 <= new_pos.y <= self.maxY and (new_pos.x, new_pos.y) not in visited): # if vaalid squaare that has not been visited
                    queue.append((new_pos, path + [move])) # add to the end of the queue (cords , path from to to cords)
        
        return [] # return empty if no valid path
    
    def dfs_search(self, start, goal):
        """
        Uses Depth-First Search (DFS) to find a path from start to goal.
        
        :param start: The starting position
        :param goal: The target position
        :return: A list of directional moves to reach the goal
        """
        stack = [(start, [])] # init stack
        visited = set() # init visited
        
        while stack: # while moves in stack
            current, path = stack.pop() # get last item in stack
            if (current.x, current.y) in visited: # if already visited
                continue # skip
            
            visited.add((current.x, current.y)) # add to visited
            
            if current.x == goal.x and current.y == goal.y: # if current is goal
                return path # return path
            
            for move in self.moves: # for each move
                new_pos = self.getNewPosition(current, move) # get possible new position
                if (0 <= new_pos.x <= self.maxX and 0 <= new_pos.y <= self.maxY and (new_pos.x, new_pos.y) not in visited): # if valid and not visited
                    stack.append((new_pos, path + [move])) # append to the stack
        
        return [] # if no path return empty array
    
    def getNewPosition(self, position, move):
        """
        Computes a new position given a move direction.
        
        :param position: The current position
        :param move: The move direction (NORTH, SOUTH, EAST, WEST)
        :return: A new Pose object representing the new position
        """
        new_pos = Pose() # init pose
        new_pos.x = position.x + (1 if move == Directions.EAST else -1 if move == Directions.WEST else 0) # increment x
        new_pos.y = position.y + (1 if move == Directions.NORTH else -1 if move == Directions.SOUTH else 0) # increment y
        return new_pos # return new pose

    # A move is a list of the directions that [Link, Wumpus1, Wumpus2,
    # ...] move in.  takeStep decodes these and makes the relevant
    # change to the state. Basically it looks for the first list
    # element that is non-zero and interprets this as a
    # direction. Movements that exceed the limits of the world have no
    # effect.

    def takeStep(self, move):
        """
        Moves Link and the Wumpus characters according to the given move array.
        
        :param move: A list of moves where move[0] is Link's move and move[i] is Wumpus i's move.
        """
        if move[0] != 0: # if move for link
            direction = move[0] # get move direction
            if direction and isinstance(direction, Directions): # if direction is actually a direction
                self.lLoc = self.getNewPosition(self.lLoc, direction) # move folloeing the direction
        
        for i in range(1, len(self.wLoc) + 1): # for each wumpus
            if move[i] != 0: # if moved
                direction = move[i] # get direction of move
                if direction and isinstance(direction, Directions): # ensure actually a direction
                    self.wLoc[i - 1] = self.getNewPosition(self.wLoc[i - 1], direction) #move to new position
