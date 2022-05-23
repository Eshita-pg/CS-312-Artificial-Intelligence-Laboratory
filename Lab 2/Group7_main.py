import time
import sys
import os

from Group7_state import State
from Group7_algorithms import heuristic_search,hill_climbing
from Group7_input_output import read_input_file, write_output_file

def main():
    st = time.perf_counter()     #Start a time counter.

    if len(sys.argv) == 5:     #If the length of the keyword arguments is four...
        method = sys.argv[1]     #The second argument is the method/algorithm used to find a solution.
        heuristic = sys.argv[2]   #The third argument is number of heuristic function
        input_file = sys.argv[3]     #The fourth argument is a .txt file containing the initial and final state of the problem.
        output_file = sys.argv[4]     #The fifth argument is a .txt file containing the solution of the problem.

        initial_state, goal_state = read_input_file(filename = input_file)     #Read the input file and return two state objects.

        
        if method == 'best':
            solution = heuristic_search(current_state = initial_state, goal_state = goal_state,function = heuristic )
        elif method == 'hill':
            solution = hill_climbing(current_state = initial_state, goal_state = goal_state, function = heuristic)
        else:     #If the method argument is none of the above, print a usage message.
            solution = None
            print('Usage: python main.py <method> <input filename> <output filename>')

        if solution == goal_state:     #If the solution is equal to the goal state...
            number_of_moves = write_output_file(solution = solution, filename = output_file)     #Write the solution file and return the number of moves.

            print('Solution found!')
            print('Number of blocks:', len(initial_state.layout.keys()))
            print('Method:', method)
            print('Number of moves:', number_of_moves)
            print('Execution time:', str(round(time.perf_counter() - st, 4)))
    else:     #Else, if the length of the keyword arguments is not equal to four, print a usage message.
        print('Usage: python main.py <method> <heuristic> <input filename> <output filename>')

if __name__ == '__main__':
	main()