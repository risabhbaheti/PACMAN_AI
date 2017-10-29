# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from curses import start_color
from inspect import stack


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()

    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()     #present state
    stack = util.Stack()                #stack to hold present state and directions from Start state
    visited_set = []                    # list containing all visited nodes 
    start_dir = []                      # Entire path from start to the goal path
    while( problem.isGoalState(start) != True ):
        successors = problem.getSuccessors(start)
        start_dir_len = len(start_dir)
        for l,m,n in successors:
            temp = start_dir[0:start_dir_len]
            temp.append(m)
            stack.push((l,temp))
        while True:
            start,start_dir = stack.pop()               #Getting the successor to be explored and the directions from start node
            if start not in visited_set:                #If the successor is in the visited set get the next successor
                visited_set.append(start)
                break
    return start_dir
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()         #present state
    queue = util.Queue()                    #stack to hold present state and directions from Start state
    visited_set = [start]                   # list containing all visited nodes 
    start_dir = []                          # Entire path from start to the goal path
    while( problem.isGoalState(start) != True ):
        successors = problem.getSuccessors(start)
        start_dir_len = len(start_dir)
        for l,m,n in successors:
            temp = start_dir[0:start_dir_len]
            temp.append(m)
            queue.push((l,temp))
        while True:
            start,start_dir = queue.pop()               #Getting the successor to be explored and the directions from start node
            if start not in visited_set:                #If the successor is in the visited set get the next successor
                visited_set.append(start)
                break
    return start_dir

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()         #present state
    queue = util.PriorityQueue()            #stack to hold present state
    visited_set = [start]                   # list containing all visited nodes 
    start_dir = []                          # Entire path from start to the goal path
    cost = 0                  
    while( problem.isGoalState(start) != True ):
        successors = problem.getSuccessors(start)
        start_dir_len = len(start_dir)
        for l,m,n in successors:
            temp = start_dir[0:start_dir_len]
            temp.append(m)
            temp_cost = cost + n                        #Calculating the path cost till the next successor
            queue.push((l,temp,temp_cost),temp_cost)
        while True:
            start,start_dir,cost = queue.pop()          #Getting the successor to be explored ,direction from start state and cost to the path
            if start not in visited_set:                #If the successor is in the visited set get the next successor
                visited_set.append(start)
                break
    return start_dir
        
def nullHeuristic(state, problem=None):
    """
from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    start = problem.getStartState()         #present state
    queue = util.PriorityQueue()            #stack to hold present state
    visited_set = [start]                   # list containing all visited nodes 
    start_dir = []                          # Entire path from start to the goal path
    cost = 0                  
    while( problem.isGoalState(start) != True ):
        successors = problem.getSuccessors(start)
        start_dir_len = len(start_dir)
        for l,m,n in successors:
            temp = start_dir[0:start_dir_len]
            temp.append(m)
            temp_cost = cost + n                    #Calculating the path cost till the next successor
            heuristic_cost = heuristic(l,problem)   #Calculating the heuristic cost and adding it to the path cost
            path_cost = cost + n
            temp_cost = path_cost + heuristic_cost
            queue.push((l,temp,path_cost),temp_cost)
        while True:
            start,start_dir,cost = queue.pop()      #Getting the successor to be explored ,direction from start state and cost to the path
            if start not in visited_set:            #If the successor is in the visited set get the next successor
                visited_set.append(start)
                break
    return start_dir
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
