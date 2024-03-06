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
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #states to be explored (LIFO). holds nodes in form (state, action)
    frontier = util.Stack()
    #previously explored states (for path checking), holds states
    exploredNodes = []
    #define start node
    startState = problem.getStartState()
    startNode = (startState, [])
    
    frontier.push(startNode)
    
    while not frontier.isEmpty():
        #begin exploring last (most-recently-pushed) node on frontier
        currentState, actions = frontier.pop()
        
        if currentState not in exploredNodes:
            #mark current node as explored
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                return actions
            else:
                #get list of possible successor nodes in 
                #form (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                #push each successor to frontier
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newNode = (succState, newAction)
                    frontier.push(newNode)

    return actions  
   

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    Args:
    - problem: A SearchProblem instance representing the problem to be solved.

    Returns:
    - actions: A list of actions that reach the goal state.
    """
    # Initialize the frontier as a queue (FIFO) for BFS
    frontier = util.Queue()
    # Initialize a set to keep track of explored nodes
    exploredNodes = set()
    
    # Define the start state
    startState = problem.getStartState()
    startNode = (startState, [])
    
    frontier.push(startNode)
    
    while not frontier.isEmpty():
        # Explore the first (oldest) node in the frontier
        currentState, actions = frontier.pop()
        
        if currentState not in exploredNodes:
            # Mark the current state as explored
            exploredNodes.add(currentState)

            if problem.isGoalState(currentState):
                return actions
            else:
                # Get a list of possible successor nodes in the form (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                # Push each successor to the end of the queue (BFS)
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newNode = (succState, newAction)
                    frontier.push(newNode)

    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic):
    
    open_list = util.PriorityQueue()
    start = problem.getStartState()
    open_list.push((start, [], 0), 0)
    visited = set()

    while not open_list.isEmpty():
        state, actions, cost = open_list.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for successor, action, step_cost in successors:
                new_cost = cost + step_cost
                f_value = new_cost + heuristic(successor, problem)
                open_list.push((successor, actions + [action], new_cost), f_value)

    return None

def aStarWeighted(problem, heuristic, weight=100):
   
    open_list = util.PriorityQueue()
    start = problem.getStartState()
    open_list.push((start, [], 0), 0)
    visited = set()

    while not open_list.isEmpty():
        state, actions, cost = open_list.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for successor, action, step_cost in successors:
                new_cost = cost + step_cost
                f_value = new_cost + weight*heuristic(successor, problem)
                open_list.push((successor, actions + [action], new_cost), f_value)

    return None

def iterativeDeepeningAStar(problem, heuristic):
    depth_limit = 1
    while True:
        result = aStarSearchLimited(problem, heuristic, depth_limit)
        if result is not None:
            return result
        depth_limit += 1

def aStarSearchLimited(problem, heuristic, depth_limit):
    open_list = util.PriorityQueue()
    start = problem.getStartState()
    open_list.push((start, [], 0), 0)
    visited = set()

    while not open_list.isEmpty():
        state, actions, cost = open_list.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited and len(actions) <= depth_limit:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for successor, action, step_cost in successors:
                new_cost = cost + step_cost
                f_value = new_cost + heuristic(successor, problem)
                if len(actions) + 1 <= depth_limit:
                    open_list.push((successor, actions + [action], new_cost), f_value)

    return None





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
astarwgt=aStarWeighted
deepastar=iterativeDeepeningAStar

