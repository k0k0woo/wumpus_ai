# puzzleWorld.py
#
# A file that represents a puzzle version of the Wumpus World, keeping
# track of the position of the Wumpus and Link.
#
# Written by: Simon Parsons
# Last Modified: 17/12/24

import random
import config
import utils
import copy
from world import World
from utils import Pose, Directions, State
from collections import deque

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
        if utils.sameAs(self, goal):
            self.status = State.WON 
            print("Puzzle Over!")
            return True
        return False
    
    def makeAMove(self, goal):
        """
        Executes the next move in the plan if available. If no plan exists,
        it generates one first.
        
        :param goal: The target state to reach
        """
        if not self.plan:
            self.plan = self.generatePlan(goal)
        
        if self.plan:
            move = self.plan.pop(0)
            print("Executing Move:", move)
            self.takeStep(move)
        else:
            print("No moves left to execute!")
    
    def generatePlan(self, goal):
        """
        Generates a sequence of moves to transition from the current state to the goal state.
        Uses BFS to determine the optimal path for Link and each Wumpus.
        
        :param goal: The target state
        :return: A list of moves in the format [Link_move, Wumpus1_move, Wumpus2_move, ...]
        """
        link_path = self.bfs_search(self.lLoc, goal.lLoc)
        wumpus_paths = [self.bfs_search(self.wLoc[i], goal.wLoc[i]) for i in range(len(self.wLoc))]
        
        max_length = max(len(link_path), max(len(path) for path in wumpus_paths))
        plan = []
        
        for i in range(max_length):
            move = []
            move.append(link_path[i] if i < len(link_path) else 0)
            for j in range(len(self.wLoc)):
                move.append(wumpus_paths[j][i] if i < len(wumpus_paths[j]) else 0)
            plan.append(move)
        
        return plan
    
    def bfs_search(self, start, goal):
        """
        Uses Breadth-First Search (BFS) to find the shortest path from start to goal.
        
        :param start: The starting position
        :param goal: The target position
        :return: A list of directional moves to reach the goal
        """
        queue = deque([(start, [])])
        visited = set()
        
        while queue:
            current, path = queue.popleft()
            if (current.x, current.y) in visited:
                continue
            
            visited.add((current.x, current.y))
            
            if current.x == goal.x and current.y == goal.y:
                return path  # Ensure one final move is included
            
            for move in self.moves:
                new_pos = self.getNewPosition(current, move)
                if (0 <= new_pos.x <= self.maxX and 0 <= new_pos.y <= self.maxY and (new_pos.x, new_pos.y) not in visited):
                    queue.append((new_pos, path + [move]))
        
        return []
    
    def getNewPosition(self, position, move):
        """
        Computes a new position given a move direction.
        
        :param position: The current position
        :param move: The move direction (NORTH, SOUTH, EAST, WEST)
        :return: A new Pose object representing the new position
        """
        new_pos = Pose()
        new_pos.x = position.x + (1 if move == Directions.EAST else -1 if move == Directions.WEST else 0)
        new_pos.y = position.y + (1 if move == Directions.NORTH else -1 if move == Directions.SOUTH else 0)
        return new_pos
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
        if move[0] != 0:
            direction = move[0]
            if direction and isinstance(direction, Directions):
                self.lLoc = self.getNewPosition(self.lLoc, direction)
        
        for i in range(1, len(self.wLoc) + 1):
            if move[i] != 0:
                direction = move[i]
                if direction and isinstance(direction, Directions):
                    self.wLoc[i - 1] = self.getNewPosition(self.wLoc[i - 1], direction)
