# Author: Leslie Pedro
# This program uses various search techniques (uninformed and informed) to 
# solve the fifteen puzzle. 
# for TCSS 435 Programming Assignment 1
# Professor: Raghavi Sakpal
import sys
import queues
import search_tree
import fifteen_gui
from copy import copy

node = search_tree.Node
tree = search_tree.Tree
        
''' Prints the board to the console for testing and debugging '''
def printBoard(board):
    col = 0
    print '-----------------'
    for row in range(0,4):
        print'|', board[col], '|', board[col + 1], '|', board[col + 2], '|', board[col + 3], '|'
        print '-----------------'
        col += 4
  
''' finds the position on the board where the space resides '''
def find_space(self, board):
    count = 0
    for char in board:
        if(char == ' '):
            return count
        count += 1

''' performs a breadth-first search technique to solve the 15 puzzle '''
def bfs(board):
    srchTree = tree(node(copy(board), -1))
    return srchTree.bfs(srchTree.root)

''' performs a depth-first search technique to solve the 15 puzzle '''
def dfs(board):
    srchTree = tree(node(copy(board), -1))
    return srchTree.dfs(srchTree.root)
    
''' Recovers the steps to solution for the 15-puzzle'''
def recover(end_node):
    path = get_path(end_node)
    print 'Solution: \n' # print the solution and the board at each state
    while not path.empty():
        node = path.pop()
        printBoard(node.state) 
        print '\n'

def get_path(end_node): 
    path = queues.Stack() # stack for tracing up to the root ...
    node = end_node # ... from the end node
    while node != -1 and node is not None: #loop to fill stack with nodes in path
        path.push(node)
        node = node.tracker
    return path
    
''' Starts the search to solve the puzzle based on command line arguments'''
def start_search(args, board):
    srch_type = args[2]     # get the search type
    if srch_type == 'DLS' or srch_type == 'GBFS' or srch_type == 'AStar':
        opts = args[3]          # get the options
        print 'options: ', opts
    srchTree = tree(node(copy(board), -1))
    end = False
    print 'Search Type: ', srch_type, '\n'
    print 'Start State: \n'
    printBoard(board)       # print board (for testing)
    if srch_type == 'BFS': # if the search type is bfs, perform search
        end, max_fringe = srchTree.bfs(srchTree.root)
    elif srch_type == 'DFS': # if the search type is dfs, perform search
        end, max_fringe = srchTree.dfs(srchTree.root, sys.maxint)
        print end
    elif srch_type == 'DLS': # if the search type is dls, perform search
        end, max_fringe = srchTree.dfs(srchTree.root, int (opts))
    elif srch_type == 'GBFS': # if the search type is dfs, perform search
        if opts == 'h1':
            end, max_fringe = srchTree.gbfs(srchTree.root, 1)
        elif opts == 'h2':
            end, max_fringe = srchTree.gbfs(srchTree.root, 2)
    elif srch_type == 'AStar' : # if the search type is A*, perform search
        if opts == 'h1':
            end, max_fringe = srchTree.aStar(srchTree.root, 1)
        elif opts == 'h2':
            end, max_fringe = srchTree.aStar(srchTree.root, 2)

    if end != False: # recover solution
        recover(end)
        print end.depth,',', srchTree.num_created, ',', srchTree.num_expanded, ',', max_fringe
    else:
        print -1, ',', srchTree.num_created, ',', -1, ',', max_fringe
    return end

        
        
        
''' main for the fifteen puzzle program '''
''' accepts arguments containing the start state for the puzzle and the '''
''' type of search to use in problem solving '''
def main():
    print 'Hello from main'
    # Get the command line arguments
    args = sys.argv
    board_1 = list(args[1])    # Create the game board
    gui = fifteen_gui.fifteen_gui()
    end = start_search(args, board_1)
    gui.main_loop(get_path(end))
        
        
main()