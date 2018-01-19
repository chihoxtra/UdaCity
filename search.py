# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import copy
import searchAgents
from game import Directions

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    return  [s,s,w,s,w,w,s,w]

def nullHeuristic(pos, p=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def deepTree(p, state, gInfo): #search only first found path
    #p: problem object
    #state: tuple: pos, move, cost
    #info: dict of various states and variables

    currPos = state[0]
    currMove = state[1] #(e,s,w,n or None for start State)
    currCost = state[2]

    #step 1: remove current pos from Frontier list
    if currPos in gInfo['frontierList']:
        gInfo['frontierList'].pop(gInfo['frontierList'].index(currPos))

        #step 2: commit the current move to exploredList, cost, and moveList
        gInfo['exploredList'].append(currPos)

    # step 3: check if reached goal state
    if not p.isGoalState(currPos):

        # step 3: extract successors/actions
        listSuccessors = p.getSuccessors(currPos)

        if bool(listSuccessors): #if there is successor
            for s in reversed(listSuccessors):
                #if currPos == (29,10):
                #    print(s[0] not in gInfo['exploredList'])
                #    print(s[0] not in gInfo['frontierList'])
                if s[0] not in gInfo['exploredList'] and s[0] not in gInfo['frontierList']:
                    # step 4: add existing state to frontier list
                    gInfo['frontierList'].append(s[0])

                    #gInfo, rInfo = deepTree(p, s, gInfo, dict(cInfo))
                    gInfo = deepTree(p, s, gInfo)

                    if gInfo['goalFound'] == True: #only commit to cache list if goal is found
                        gInfo['bestPosList'].insert(0,s[0])
                        gInfo['bestMovesList'].insert(0,s[1])
                        gInfo['bestCost'] += s[2]
                        #print gInfo['bestPosList']
                        #print ""
                        break
                else:
                    pass

        else: #running out of moves
            return gInfo
    else:
        gInfo['goalFound'] = True
        return gInfo

    return gInfo

def deepTree1(p, state, gInfo, path): #Search optimal path by clearing explored list
    #p: problem object
    #state: tuple: pos, move, cost
    #ginfo: dict of various states and variables
    #path: the disposable path cache when agent ix exploring different paths

    currPos = state[0]
    currMove = state[1] #(e,s,w,n or None for start State)
    currCost = state[2]

    #step 1: remove current pos from Frontier list
    if currPos in path['frontierList']:
        path['frontierList'].pop(path['frontierList'].index(currPos))

        #step 2.1: commit the current move to exploredList
        path['exploredList'].append(currPos)

        #step 2.2: temporally commit the corrent path
        if currMove != None: #not adding the initial state
            path['cost'] += currCost
            path['posList'].append(currPos)
            path['movesList'].append(currMove)

    # step 3: check if reached goal state
    if not p.isGoalState(currPos):

        # step 3: extract successors/actions of current pos
        # make sure it is not found in exploredlist or frontierlist
        sList = [x for x in p.getSuccessors(currPos) if
                (x[0] not in path['exploredList']
                and x[0] not in path['frontierList'])]

        if bool(sList): #if there is successor

            backupPath = {}
            if len(sList) > 1: # keep a copy of the current path when there is branch
                backupPath = copy.deepcopy(path)

            for s in sList:
                # step 4: add existing state to frontier list
                path['frontierList'].append(s[0])

                gInfo, path = deepTree1(p, s, gInfo, path)

                if gInfo['goalFound'] == True: #only commit to cache list if goal is found
                    #print(path['posList'])
                    #print(path['cost'])
                    if path['cost'] < gInfo['bestCost']:

                        gInfo['bestCost'] = copy.deepcopy(path['cost'])
                        gInfo['bestPosList'] = copy.deepcopy(path['posList'])
                        gInfo['bestMovesList'] = copy.deepcopy(path['movesList'])
                        #print gInfo['exploredList']
                    gInfo['goalFound'] = False #so that it can continute to search
                    #path = copy.deepcopy(backupPath)
                #else:
                    #pass
                if len(sList) > 1: #and (sList.index(s) < (len(sList)-1)):
                    path = copy.deepcopy(backupPath) #retore the backup copy

        else: #dead end?
            return gInfo, path
    else:
        gInfo['goalFound'] = True #goal found
        return gInfo, path

    return gInfo, path



def depthFirstSearch(p):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    startPos = p.getStartState()
    startState = (startPos, None, 0)

    gInfo = {}
    gInfo['exploredList'] = []
    gInfo['frontierList'] = [startPos]
    gInfo['bestCost'] = 100000
    gInfo['bestMovesList'] = []
    gInfo['bestPosList'] = []
    gInfo['goalFound'] = False

    path = {}
    path['cost'] = 0
    path['posList'] = []
    path['movesList'] = []
    path['exploredList'] = []
    path['frontierList'] = [startPos]

    #gSearchInfo, path = deepTree1(p, startState, gInfo, path)
    gSearchInfo = deepTree(p, startState, gInfo)

    #print gSearchInfo['goalFound']

    #print gInfo['bestPosList']

    #print "Start Pos:", startPos

    #print "Is this a goal?", p.isGoalState((29,10))
    #print "Start's successors:", p.getSuccessors((2,2))

    return gSearchInfo['bestMovesList']

def bfsInit_backup(p):

    startPos = p.getStartState()
    #print(startPos)
    exploredList = []
    frontierList1 = {}

    FQueue = util.Queue()
    fListItem = (startPos, 0.0, [], [])
    FQueue.push(fListItem)

    frontierList = [startPos]
    #frontierList1 = {startPos: 0.0}

    return exploredList, FQueue, frontierList

def breadthFirstSearch_backup(p):
    """Search the shallowest nodes in the search tree first."""
    completeMovesList = []
    completePosList = []
    exploredList, FQueue, frontierList = bfsInit(p)

    while not FQueue.isEmpty():

      # step 1: choose the next candidate:
      (currPos, currCummStepCost, currCummMoves, currCummPos)  = FQueue.pop()

      # step 2: commit to explored list, Move and Cost
      # currPos is chosen
      frontierList.pop(frontierList.index(currPos))
      #frontierList1.pop(currPos, None)

      # step 3: check if this state is the goal
      if p.isGoalState(currPos):
          if bool(completeMovesList):
              completeMovesList.extend(currCummMoves)
              completePosList.extend(currCummPos)
              #print(len())
              #print(completePosList)
              return completeMovesList
          else:
              return currCummMoves
      else:
          sList = [x for x in p.getSuccessors(currPos) if
                  (x[0] not in exploredList
                   and x[0] not in frontierList)]
          for pos, mov, _ in sList:
              # step 4: add new nodes to frontierlist and add cost
              # 4.1 make copies of the current path info
              fcummStepCost = copy.deepcopy(currCummStepCost)
              fcummMoves = copy.deepcopy(currCummMoves)
              fcummPos = copy.deepcopy(currCummPos)
              if pos != (-1,-1): # a hack to reset search

                  fcummMoves.append(mov)
                  fcummPos.append(pos)
                  fcummStepCost = p.getCostOfActions(fcummMoves)

                  fListItem = (pos, fcummStepCost, fcummMoves, fcummPos)
                  FQueue.push(fListItem)
                  #frontierListQ.push(fListItem, fcummStepCost)

                  frontierList.append(pos)
                  #frontierList1[currPos] = fcummStepCost
              else: #need reset?

                  completeMovesList.extend(fcummMoves)
                  completePosList.extend(fcummPos)
                  exploredList, FQueue, frontierList = bfsInit(p)

      exploredList.append(currPos)
      #frontierList.pop(currPos, None)

def bfsInit(p):

    pQueue = util.PriorityQueue()
    startPos = p.getStartState()
    pQueue.push((startPos, [], []) ,0.0)
    frontierList = {startPos: 0.0}
    exploredList = []
    #print("from fx: "+ str(startPos))
    #print(frontierList)
    return pQueue, frontierList, exploredList

def breadthFirstSearch(p):
    """Search the shallowest nodes in the search tree first."""
    pQueue, frontierList, exploredList = bfsInit(p)

    while not pQueue.isEmpty():
      # step 1: choose the next candidate:
      (currPos, currCummMoves, currCummPos) = pQueue.pop()
      frontierList.pop(currPos, None)

      if currPos not in exploredList:
          # step 3: commit to explored list, Move and Cost
          exploredList.append(currPos)

      """ the hack to get decided info from Agent """
      if 'updateParams' in dir(p):
          _ = p.updateParams(currCummMoves,currCummPos)

      # step 2: check if this state is the goal
      if p.isGoalState(currPos):
          # need to get best moves list'

          if 'g' in dir(p):
              p.g['_1CMovesList'] = currCummMoves
              p.g['_1CPosList'] = currCummPos
          if 'allSeqTried' in dir(p):
              if p.allSeqTried:
                  return p.bestMovesSeq
              #bestMovesSeq = p.updateParams(currCummMoves,currCummPos)
              #if bool(bestMovesSeq): return bestMovesSeq
          return currCummMoves

      # step 4: get successor nodes
      sList = p.getSuccessors(currPos)
      """ Make sure there is no special signal at the end """

      if bool(sList) and sList[-1][0][0] >= 0:
          for (spos, smoves, scost) in sList:
              # step 4: add new nodes to frontierlist and add cost
              # 4.1 make copies of the current path info
              fcummMoves = copy.deepcopy(currCummMoves)
              fcummPos = copy.deepcopy(currCummPos)

              fcummPos.append(spos)
              #print(fcummPos)
              fcummMoves.append(smoves)
              # 4.2 get current path cost

              #fcummUnitCost = p.getCostOfActions(fcummMoves, currPos, currCummPos)
              fcummUnitCost = p.getCostOfActions(fcummMoves)

              # 4.3 update Queue and frontier list
              if spos not in exploredList and spos not in frontierList:
                  #legal value
                  pQueue.push((spos, fcummMoves, fcummPos), fcummUnitCost)
                  frontierList[spos] = fcummUnitCost
              # 4.4 update if same nodes with lower cost found on frontierlist
              elif spos in frontierList:
                  if frontierList[spos] > fcummUnitCost:
                      pQueue.update((spos, fcummMoves, fcummPos), fcummUnitCost)
                      frontierList[spos] = fcummUnitCost

      elif bool(sList) and sList[-1][0][0] < 0: #handle special signal and reset
          fcummMoves = []
          fcummPos = []
          pQueue, frontierList, exploredList = bfsInit(p)




def uniformCostSearch(p):
    """Search the shallowest nodes in the search tree first."""

    pQueue = util.PriorityQueue()
    startPos = p.getStartState()

    pQueue.push((startPos, [], []) ,0.0)
    frontierList = {startPos: 0.0}
    exploredList = []

    while not pQueue.isEmpty():
      # step 1: choose the next candidate:
      (currPos, currCummMoves, currCummPos) = pQueue.pop()
      frontierList.pop(currPos, None)

      if currPos not in exploredList:
          # step 3: commit to explored list, Move and Cost
          exploredList.append(currPos)

      # step 2: check if this state is the goal
      if p.isGoalState(currPos):
          return currCummMoves

      # step 4: get successor nodes
      for (spos, smoves, scost) in p.getSuccessors(currPos):
          # step 4: add new nodes to frontierlist and add cost
          # 4.1 make copies of the current path info
          fcummMoves = copy.deepcopy(currCummMoves)
          fcummPos = copy.deepcopy(currCummPos)

          fcummPos.append(spos)
          fcummMoves.append(smoves)
          # 4.2 get current path cost
          fcummUnitCost = p.getCostOfActions(fcummMoves)

          # 4.3 update Queue and frontier list
          if spos not in exploredList and spos not in frontierList:
              pQueue.push((spos, fcummMoves, fcummPos), fcummUnitCost)
              frontierList[spos] = fcummUnitCost
          # 4.4 update if same nodes with lower cost found on frontierlist
          elif spos in frontierList:
              if frontierList[spos] > fcummUnitCost:
                  pQueue.update((spos, fcummMoves, fcummPos), fcummUnitCost)
                  frontierList[spos] = fcummUnitCost


def aStarSearch_backup(p, h=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    pQueue = util.PriorityQueue()
    startPos = p.getStartState()

    pQueue.push((startPos, [], []) ,0.0 + h(startPos, p))
    frontierList = {startPos: 0.0 + h(startPos, p)}
    exploredList = []

    while not pQueue.isEmpty():
      # step 1: choose the next candidate:
      (currPos, currCummMoves, currCummPos) = pQueue.pop()
      frontierList.pop(currPos, None)

      if currPos not in exploredList:
          # step 3: commit to explored list, Move and Cost
          exploredList.append(currPos)

      # step 2: check if this state is the goal
      if p.isGoalState(currPos):
          return currCummMoves

      # step 4: get successor nodes
      for (spos, smoves, scost) in p.getSuccessors(currPos):
          # step 4: add new nodes to frontierlist and add cost
          # 4.1 make copies of the current path info
          fcummMoves = copy.deepcopy(currCummMoves)
          fcummPos = copy.deepcopy(currCummPos)

          fcummPos.append(spos)
          fcummMoves.append(smoves)
          # 4.2 get current path cost
          fcummUnitCost = p.getCostOfActions(fcummMoves)
          fTotalCost = fcummUnitCost + h(spos, p)

          # 4.3 update Queue and frontier list
          if spos not in exploredList and spos not in frontierList:
              pQueue.push((spos, fcummMoves, fcummPos), fTotalCost)
              frontierList[spos] = fTotalCost
          # 4.4 update if same nodes with lower cost found on frontierlist
          elif spos in frontierList:
              if frontierList[spos] > fTotalCost:
                  pQueue.update((spos, fcummMoves, fcummPos), fTotalCost)
                  frontierList[spos] = fTotalCost


def astarInit(p, h):

    pQueue = util.PriorityQueue()
    startPos = p.getStartState()
    pQueue.push((startPos, [], []) ,0.0 + h(startPos, p))
    frontierList = {startPos: 0.0 + h(startPos, p)}
    exploredList = []
    #print("from fx: "+ str(startPos))
    #print(frontierList)
    return pQueue, frontierList, exploredList

def manhattanHeuristic(pos, p=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    print(p.goal)
    return util.manhattanDistance(pos, p.goal)

def cornersHeuristic(currPos, p):
    """  reference to searchAgents.cornersHeuristic """
    return searchAgents.cornersHeuristic(currPos, p) # Default to trivial solution

def foodHeuristic(state, problem):
    """  reference to searchAgents.cornersHeuristic """
    return searchAgents.foodHeuristic(state, problem) # Default to trivial solution

def aStarSearch(p, heuristic=nullHeuristic): #nullHeuristic cornersHeuristic foodHeuristic

    """Search the shallowest nodes in the search tree first."""
    pQueue, frontierList, exploredList = astarInit(p,heuristic)

    while not pQueue.isEmpty():
      # step 1: choose the next candidate:
      (currPos, currCummMoves, currCummPos) = pQueue.pop()
      frontierList.pop(currPos, None)

      if currPos not in exploredList:
          # step 3: commit to explored list, Move and Cost
          exploredList.append(currPos)

      """ the hack to get decided info from Agent """
      if 'updateParams' in dir(p):
          _ = p.updateParams(currCummMoves,currCummPos)

      # step 2: check if this state is the goal
      if p.isGoalState(currPos):
          # need to get best moves list'

          if 'updateParams' in dir(p):
              bestMovesSeq = p.updateParams(currCummMoves,currCummPos)
              if bool(bestMovesSeq): return bestMovesSeq
          return currCummMoves

      # step 4: get successor nodes
      sList = p.getSuccessors(currPos)
      """ Make sure there is no special signal at the end """
      if bool(sList) and sList[-1][0][0] >= 0:
          for (spos, smoves, scost) in sList:
              # step 4: add new nodes to frontierlist and add cost
              # 4.1 make copies of the current path info
              fcummMoves = copy.deepcopy(currCummMoves)
              fcummPos = copy.deepcopy(currCummPos)

              fcummPos.append(spos)
              fcummMoves.append(smoves)
              # 4.2 get current path cost

              #fcummUnitCost = p.getCostOfActions(fcummMoves, currPos, currCummPos)
              fcummUnitCost = p.getCostOfActions(fcummMoves)
              fTotalCost = fcummUnitCost + heuristic(spos, p)

              # 4.3 update Queue and frontier list
              if spos not in exploredList and spos not in frontierList:
                  #legal value
                  pQueue.push((spos, fcummMoves, fcummPos), fTotalCost)
                  frontierList[spos] = fTotalCost
              # 4.4 update if same nodes with lower cost found on frontierlist
              elif spos in frontierList:
                  if frontierList[spos] > fTotalCost:
                      pQueue.update((spos, fcummMoves, fcummPos), fTotalCost)
                      frontierList[spos] = fTotalCost

      elif bool(sList) and sList[-1][0][0] < 0: #handle special signal and reset
          fcummMoves = []
          fcummPos = []
          pQueue, frontierList, exploredList = astarInit(p, heuristic)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
