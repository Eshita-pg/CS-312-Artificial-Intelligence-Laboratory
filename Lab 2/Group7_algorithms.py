import time
from collections import deque

"""
Two algorithms are implemented in order to sovle the problems:
    1) Best first search
    2) Hill Climbing 

Three heuristic functions are implemented 

"""

def heuristic_1(F, goal_layout, blocks_keys):
   
    scores = []     #A list object containing the score of each state.

    for state in F:
        out_of_place = 0     #Initialize each score to 0.

        for key in blocks_keys:     #For each block...
            if state.layout[key] != goal_layout[key]:     #If it is not in its final position...
                out_of_place += 1     #Add 1 to score.
        
        scores.append(out_of_place)
    
    return scores.index(min(scores))     #Return the index of the state with the minimun score.

def heuristic_2(F, goal_layout, blocks_keys):
   
    scores = []     #A list object containing the score of each state.

    for state in F:
        score = 0     #Initialize each score to 0.

        for key in blocks_keys:     #For each block...
            if state.layout[key] != goal_layout[key]:     #If it is not in its final position...
                score += 1     #Add 1 to score.
        
        score += state.distance     #Add the distance from the root to score.
        
        scores.append(score)
    
    return scores.index(min(scores))     #Return the index of the state with the minimun score.


def heuristic_3(F, goal_layout, blocks_keys):
    all_scores = []
    for state in F:
        score = 0
        for key in blocks_keys:
            if state.layout[key] != goal_layout[key]:
                score = 100
            elif state.layout[key] == goal_layout[key]:
                score = 1000
        
        all_scores.append(score)
        
    return all_scores.index(max(all_scores))
    
        

def heuristic_search(current_state, goal_state, function ,timeout =6):
   
    if function == '0':     
        heuristic_function = heuristic_1
    elif function == '1':     
        heuristic_function = heuristic_2
    elif function == '2':    
        heuristic_function = heuristic_3

    F = []     #A list fot storing the nodes/states.
    discovered = set()     #A set for keeping the ids of the discovered states.
    blocks_keys = list(current_state.layout.keys())     #A list with the names/keys of the blocks.

    F.append(current_state)     #Add the current/initial state to the list.
    discovered.add(current_state.id)     #Add the id of the state to the set.

    st = time.perf_counter()     #Start a time counter.
    counter = 0

    while F:     #While F is not empty...    #Break.
        if time.perf_counter() - st > timeout:     #If the execution time exceeds the timeout...
            print('Timeout!')
            counted = str(st)
            print('Execution time :' + counted)
            return None     

        i = heuristic_function(F, goal_state.layout, blocks_keys)     #Return the index of the state with the minimum score in F.
        state = F.pop(i)     #Pop the state with the minimum score.

        if state == goal_state:     #If the state is the goal state, return it and break.
            count = str(counter)
            print('No of states explored:' + count  )
            return state
        
        children = state.calcChildren()     #Else, calculate the children of this state.

        for child in children:  
            counter += 1 #For each child...
            if child.id not in discovered:     #If this child has not been discovered...
                discovered.add(child.id)     #Mark it as discovered.
                child.parent = state     #Set the parent attribute of the child to be the state that has been poped.

                F.append(child)     #Append the child to F.
                

def hill_climbing(current_state , goal_state , function , timeout =0.00005):
    F = []
    blocks_keys = list(current_state.layout.keys())     #A list with the names/keys of the blocks.
    if function == '0':     
        heuristic_function = heuristic_1
    elif function == '1':     
        heuristic_function = heuristic_2
    elif function == '2':    
        heuristic_function = heuristic_3
        
    F.append(goal_state)
    j = heuristic_function(F, goal_state.layout, blocks_keys) 
    st = time.perf_counter()
    counter = 0
    count1 = 0
    
        
    while (True) :
        if time.perf_counter() - st > timeout:     #If the execution time exceeds the timeout...
            print('Timeout!')
            counted = str(st)
            cou = str(count1)
            print('Execution time :' + counted)
            print('No of states explored:' + cou  )
            return None
        
        curr =[]
        curr.append(current_state)
        i = heuristic_function(curr, goal_state.layout, blocks_keys)     #Return the index of the state with the minimum score in F.
        state = current_state
        
        if state == goal_state:     #If the state is the goal state, return it and break.
            return state
        
        children = state.calcChildren()  # for calculating corresponding states
        
        for child in children:
            count1 += 1
            if function == '0' or function == '1':  
                if i <= j :
                    current_state = child
                    state = child   
               
            elif function == '2':     
                if i >= j :
                    current_state = child
                    state = child 
           
        

        
        
        
    