# wumpus
The top level script is wumpus.py. This can take a number of arguments:

- -h : generates a help message
- -g : runs the game version of the wumpus world
- -p : runs the puzzle version of the wumpus world
- -d : runs without using the graphics (i.e. run "hea(d)less")
- -n : \<number\> : runs either the -p or the -g version \<number\> of times. Note that \<number\> should be an integer.

So, to run the wumpus world as a puzzle you would run:
python wumpus.py -p

and to run the game 3 times you would run:
python wumpus.py -g -n 3

The -d option is useful if you want to run your code quickly, for
example if you are running it a large number of times to track down a
rare bug, or collecting statistics for an evaluation

As in the assignment brief, you have two coding jobs 1) to write code
for the game that controls Link to loot the gold while avoiding pits
and Wumpus, and 2) to write code for the puzzle that transforms the
initial configuration "puzzle" in puzzle.py into the final state
"endState".

## Task 1
For 1, your code needs to specify the value that the function
makeMove() in link.py returns. There are four legal values for
makeMove() to return:

- Directions.NORTH
- Directions.SOUTH
- Directions.EAST
- Directions.WEST

The simple code in link.py just moves Link towards the next gold in
the list.

The only file you absolutely need to modify to create a solution for 1 
is link.py, but a solution that does reuse code will need changes
to a wider range of files. Either way, you will also likely want to
modify config.py which allows you to change the configuration of the
game --- change the size of the grid, the number of pits, the number
of Wumpus and so on --- and you should edit this to add your student
ID to test your code with your unique test setup.

Clearly the static version of the game, in which the Wumpus do not
move, is easier to solve than the dynamic version, so you might want
to start out by looking at this version.

## Task 2
For 2, your code needs to needs specify the function makeAMove() in
puzzleWorld.py. As you will see from looking at the code, what
makeAMove() currently does is to move Link and the Wumpus (using
takeStep()) if self.plan has a value. So, at a minimum, what you need
to do is to write code in puzzleWorld.py to create a suitable value
for self.plan. The initial value in puzzleWorld.py gives you an
indication of what a plan is for the default version of config.py with
2 Wumpus: it is a sequence of "moves" where each move is one of the
same for legal moves given above for one of Link and the Wumpus.

As described in the brief and CRG, you will get more credit for not
duplicating code, and to do that you will have to do more than the
minimum indicated above.

Note that with two Wumpus, the puzzle has a branching factor of 12, so
breadth first search will not solve for a large dungeon in reasonable
time. That is why a "working solution" is for a 4 by 4 grid since on
my laptop that takes a few minutes to solve whereas a 10 x 10 takes
over 24 hours (that is when I stopped waiting). You should be able to
solve 10 x 10 (and larger) with sensible heuristic methods, and you
can tell us about them all in your report.

Of course, adding another Wumpus makes the puzzle much harder, and it
means that even a 4 x 4 grid is intractable for breadth first search.

## Contents
The rest of the files are as follows:

dungeon.py  -- draws the dungeon on the screen.

game.py     -- runs the wumpus world as a game until Link wins or loses.

graphics.py -- simple Python graphics.

puzzle.py   -- runs the wumpus world as a puzzle until it is solved.

utils.py    -- utilities used in a few places.

world.py    -- keeps track of everything (used by Dungeon to draw).



