# Author: Leslie Pedro
# Point class to be used with the fifteen problem.
# for TCSS 435 Programming Assignment 1
# Professor: Raghavi Sakpal

import sys
import point_2D as point
import queues
from copy import copy

''' Two possible goal states for detecting puzzle completion '''
GOAL_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' ']
GOAL_2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'F', 'E', ' ']
POINTS = [point.Point(0, 0), point.Point(0, 1), point.Point(0, 2), point.Point(0, 3),
point.Point(1, 0), point.Point(1, 1), point.Point(1, 2), point.Point(1, 3),
point.Point(2, 0), point.Point(2, 1), point.Point(2, 2), point.Point(2, 3),
point.Point(3, 0), point.Point(3, 1), point.Point(3, 2), point.Point(3, 3)]

''' Node class creates a node for the search tree '''
class Node:
    def __init__(self, board, node):
        # The cost by which to sort this node (varies by algorithm)
        self.total_cost = 0
        # The total cost to this state in the path
        self.pathlength = 0
        # The gameboard corresponding to this state
        self.state = board
        # The tracker (node connected to this one in a path)
        self.tracker = node
        # The depth at which this node resides, -1 indicates no place in graph/tree
        self.depth = -1
    
    ''' Checks if two nodes share the same state '''
    def are_same(self, state):
        same = True # Assume the states are the same
        count = 0 # for counting indices in the state
        while same == True and count < len(state): # while the two states match 
            if state[count] != self.state[count]: # continue checking for a mismatch
                same = False # if one is found, flag the loop to stop and...
                            # alter return val
            count += 1 #increment the count
        return same #return true or false
  
''' Tree class creates a search tree for solving the 15 puzzle '''
class Tree:
    ''' Initializes a new tree '''
    def __init__(self, root):
        self.root = root
        self.root.tracker = -1
        self.num_expanded = -1
        self.num_created = -1
        self.max_fringe = -1
    
    ''' Performs a breadth-first search on the 15-puzzle to find a solution '''
    ''' If a solution is found, the last node in the solution is returned '''
    ''' Otherwise, False is returned to indicate failure '''
    def bfs(self, root):
        fringe = queues.Queue() # a queue for holding the unexplored nodes
        explored = set([]) # a set for holding each unique state already processed
        if self.is_goal(root): # if the first state is the goal state we're done
            return root, 0  # return the root node
        fringe.put(root) # else place the root on the fringe
        self.num_created = 1
        self.num_expanded = 0
        root.depth = 0
        while fringe.empty() == False: # while there are nodes in the fringe:
            node = fringe.get() # get the next node
            explored.add(str(node.state)) # add the state to explored (if unique)
            self.num_expanded += 1
            next_states = self.get_moves(node.state) # get all next states from this one
            for state in next_states: # for each next state:
                self.num_created += 1
                child = Node(state, node) # create a child node
                child.depth = node.depth + 1
                if str(child.state) not in explored: # if the child state is unexplored, 
                    if not self.is_fringe(child, fringe): # not in the fringe,
                        if self.is_goal(child): # check if it is a goal state
                            return child, fringe.max_size # return the goal state's node
                        fringe.put(child) # else put the child on the fringe
        return False, fringe.max_size # if no goal state could be found, return false
    
    ''' Performs a depth-first search to solve the 15-puzzle'''
    ''' If a solution is found, the last node is returned'''
    ''' Else False is returned to indicate failure '''
    def dfs(self, root, limit):
        if self.is_goal(root): # if the first node is a goal state we're done
            return root, 0 # return the node
        fringe = queues.Stack() # a stack for states yet to be processed
        fringe.push(root) # push the node to the stack
        root.depth = 0
        self.num_created = 1
        self.num_expanded = 0
        discovered = set([]) # create an empty set for discovered states
        while fringe.empty() == False: # if the fringe is not empty:
            node = fringe.pop() # get the top node
            if str(node.state) not in discovered: # if the node is not discovered:
                if node.depth < limit:
                    discovered.add(str(node.state)) # add it to discovered set
                    self.num_expanded += 1
                    next_states = self.get_moves(node.state) # get all next states from this one
                    for state in next_states: # for each next state:
                        self.num_created += 1
                        child = Node(state, node) # create a child node
                        child.depth = node.depth + 1
                        if not self.has_cycle(child): # if the child state is undiscovered does not cause a cycle
                            if self.is_goal(child): # check if it is a goal state
                                return child, fringe.max_size # return the child if it is a goal state
                            #if not self.is_fringe(child, fringe): # and not in the fringe
                            fringe.push(child)
        return False, fringe.max_size # if no solution was found return False 
       
    ''' Performs a greedy best-first search to solve the 15- puzzle '''
    ''' If a solution is found, the last node is returned'''
    ''' Else False is returned to indicate failure '''
    def gbfs(self, root, heuristic):
        fringe = queues.PriorityQueue() #Priority queue sorts by total_cost, 
                                        # the heuristic result val
        explored = set([]) # set of explored states (initially empty)
        root.depth = 0
        self.num_created = 1
        self.num_expanded = 0
        fringe.put(root) # put the first (root) node in the queue
        while fringe.empty() == False: # while the queue is not empty
            node = fringe.get() # grab a node from the fringe
            if self.is_goal(node): # if it is a goal state, return the node
                return node, fringe.max_size
            explored.add(str(node.state)) # add the state to explored
            self.num_expanded += 1
            for state in self.get_moves(node.state): # for each next state do:
                if str(state) not in explored: # if the state is not explored,
                    child = Node(state, node) # set up a child node
                    child.depth = node.depth + 1 # set the correct depth for the child
                    self.num_created += 1
                    if not self.is_fringe(child, fringe): # and not in the fringe:
                        child.total_cost = self.get_heuristic(child.state, heuristic) # calculate heuristic
                        fringe.put(child) # place child on fringe
        return False, fringe.max_size # if no solution could be recovered, return false
    
    ''' Performs an A* search to solve the 15-puzzle '''
    ''' Returns the goal node when reached or False if no solution reached '''
    def aStar(self, root, heuristic):
        fringe = queues.PriorityQueue() # The fringe of nodes yet to be explored
        explored = set([]) # The set of already explored states
        g_scores = {} # A map of g_scores, mapped state -> g_score
        g_scores[str(root.state)] = 0
        f_scores = {} # A map of f_scores, mapped state -> f_score
        f_scores[str(root.state)] = sys.maxint # add the f_score for the root
        root.total_cost = 0
        self.num_created += 1
        self.num_expanded = 0
        root.depth = 0
        fringe.put(root) # add root to the fringe and begin loop:
        while fringe.empty() == False:
            node = fringe.get() # get the next node in the queue
            if self.is_goal(node):
                return node, fringe.max_size # if it is a goal state, return it
            explored.add(str(node.state)) # else, add it to explored
            self.num_expanded += 1
            for state in self.get_moves(node.state): # for each next state, create a child node
                if str(state) not in explored:
                    child = Node(state, node)
                    child.depth = node.depth + 1
                    self.num_created += 1
                    temp_g = g_scores[str(node.state)] + 1 # calculate g_Score for this trip
                    if self.is_fringe(child, fringe) == False: # if the state is not in the fringe:
                        child.total_cost = temp_g + self.get_heuristic(child.state, heuristic) # calculate f_score for this child
                        g_scores[str(child.state)] = temp_g # set a g_score value
                        f_scores[str(child.state)] = child.total_cost # and add the f_Score value
                        fringe.put(child) # place child on fringe
                    elif temp_g < g_scores[str(child.state)]: #else if this state is in fringe but temp_g is better g_score:
                        fringe.remove(child.state) #remove the old node with this state
                        child.tracker = node # update the parent, g_Score, f_score for this child node
                        g_scores[str(child.state)] = temp_g
                        f_scores[str(child.state)] = temp_g + self.get_heuristic(child.state, heuristic)
                        child.total_cost = f_scores[str(child.state)]
                        fringe.put(child) #place child back on fringe
        return False, fringe.max_size # if no solution was found return false and the max size of the fringe
    
    ''' Returns the heuristic value for the current state as specified by h, the heuristic id.'''
    def get_heuristic(self, state, h):
        if h == 1:
            return self.misplaced_blocks(state) #use misplaced blocks heuristic
        elif h == 2:
            return self.manhattan_distance(state) #use manhattan distance
    
    ''' Counts the number of blocks misplaced in the current state''' 
    ''' and returns that number '''
    def misplaced_blocks(self, state):
        miss = 0
        for loc in range(0, len(state)):
            if state[loc] != ' ':
                if GOAL_1[loc] != ' ' and state[loc] != GOAL_1[loc]:
                    if GOAL_2[loc] != ' ' and state[loc] != GOAL_2[loc]:
                        miss += 1
        return miss
  
    ''' Returns the max branching factor for the board position indicated by index '''
    def branching_factor(self, index):
        table = [2, 3, 3, 2, 3, 4, 4, 3, 3, 4, 4, 3, 2, 3, 3, 2]
        return table[index]
    
    ''' Checks a specific location on the board (index) to see if it contains '''
    ''' the same data as either goal state'''
    def check_loc(self, char, index):
        if char == GOAL_1[index]:
            return True
        elif char == GOAL_2[index]:
            return True
        return False
    
    ''' Returns the Manhattan Distance for all board moves in the current board state'''
    def manhattan_distance(self, board):
        distance_sum = 0
        n = 4
        last_row = n * n
        row = 0
        while row < last_row:
            col = row
            while col < row + n:
                char = board[col]
                if char  != ' ':
                    char_point = POINTS[col]
                    g1_point = POINTS[GOAL_1.index(char)]
                    g2_point = POINTS[GOAL_2.index(char)] 
                    dx_1 = abs(char_point.x - g1_point.x)
                    dy_1 = abs(char_point.y - g1_point.y)
                    dx_2 = abs(char_point.x - g2_point.x)
                    dy_2 = abs(char_point.y - g2_point.y)
                    distance_sum += min(dx_1 + dy_1, dx_2 + dy_2)
                col += 1
            row += n
        return distance_sum
    
    ''' Returns True if there is a cycle after placing this node in the graph, False otherwise'''
    def has_cycle(self, node):
        cycle_found = False
        path_set = set([])
        while node != -1 and cycle_found == False:
            if len(path_set) > 0 and str(node.state) in path_set:
                cycle_found = True
            path_set.add(str(node.state))
            node = node.tracker
        return cycle_found
    
    ''' Checks the current state against the goal states '''
    ''' returns True if it is a goal state, False otherwise '''
    def is_goal(self, node):
        state = node.state
        for count in range(0, len(state) - 1):
            if state[count] != GOAL_1[count] and state[count] != GOAL_2[count]:
                return False
        return True
    
    ''' Determines which moves are valid for the current state'''
    def get_moves(self, board):
        space = self.find_space(board)
        moves = []
        if (space + 1) % 4 != 0: # IF CAN MOVE RIGHT
            state = copy(board) # make a copy of the board and change it's state
            temp = state[space + 1]
            state[space] = temp
            state[space + 1] = ' '
            moves.insert(0, state)
        if space - 4 > 0: #IF CAN MOVE UP
            state = copy(board) # make a copy of the board and change it's state
            temp = state[space - 4]
            state[space] = temp
            state[space - 4] = ' '
            moves.insert(1, state)
        if space % 4 != 0: #IF CAN MOVE LEFT
            state = copy(board) # make a copy of the board and change it's state
            temp = state[space - 1]
            state[space] = temp
            state[space - 1] = ' '
            moves.insert(2, state)
        if space + 4 < 16: #IF CAN MOVE DOWN
            state = copy(board) # make a copy of the board and change it's state
            temp = state[space + 4]
            state[space] = temp
            state[space + 4] = ' '
            moves.insert(3, state)
        return moves
        
    ''' finds the position on the board where the space resides '''
    def find_space(self, board):
        count = 0 # for counting indices
        for char in board: # look at each character
            if(char == ' '): # if it is the space return the index
                return count
            count += 1 # increment the count
   
    ''' Checks to see if the state in the ode passed is already represented '''
    ''' in the fringe '''
    def is_fringe(self, node, fringe):
        found = False
        count = 0
        while found == False and count < fringe.size: # search for a node with 
            if (fringe.peek(count)).are_same(node.state): # the same state
                found = True
            count += 1
        return found
            
        