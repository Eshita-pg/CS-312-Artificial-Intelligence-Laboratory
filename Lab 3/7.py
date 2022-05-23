import numpy as np
import random
from string import ascii_lowercase, ascii_uppercase
from itertools import combinations
from numpy.core.fromnumeric import var

# ******************************************************************************************************************
def Create_Problems(No_of_Clause, No_of_literals, No_of_Variables):

    variables = (list(ascii_lowercase))[:No_of_Variables] + (list(ascii_uppercase))[:No_of_Variables]
    variables.sort()
    
    All_Combos = list(combinations(variables, No_of_literals))
    All_Combos.sort()
    
    for i in range(5):
        for comb in All_Combos:
            for lits in comb:
                if (lits.upper() in comb) and (lits.lower() in comb):
                    All_Combos.remove(comb)
                    break

    True_Combos = []

    c = random.sample(All_Combos, No_of_Clause)
    c.sort()

    if c not in True_Combos:
        True_Combos.append(list(c))
    True_Combos.sort()
    return True_Combos

problems = Create_Problems(5, 4, 4)
f = open("Clauses.txt", "w")

for expression in problems:
    for clause in expression:
        f.write(str(clause) + "\n")

f.close()

# ************************************************************************************************************************

# reading clauses from clauses.txt

fp = open("Clauses.txt", "r")

Expression = list()

# clearing each of the clause input
for j in range(5):
    clause = (
        fp.readline().strip("\n)").strip("(").replace(",", "").replace("'", "").split()
    )
    Expression.append(clause)
    
# ************************************************************************************************************************
   
# randomly creating intial state 
  
No_of_Variables = 4

variables = (list(ascii_lowercase))[:No_of_Variables] + (list(ascii_uppercase))[:No_of_Variables]

def Val_assign(variables, n):
    # for Tabu search to amke the initial state as all lowercase 0 and uppercase 1
    # for_Lowercase = [0,0,0,0]
    # for_Uppercase = [1,1,1,1]
    # for other searches , random initial states can be made using following code/syntax
    for_Lowercase = list(np.random.choice(2, n))
    for_Uppercase = [abs(1 - i) for i in for_Lowercase]
    
    assign = for_Lowercase + for_Uppercase
    var_assign = dict(zip(variables, assign))
    return var_assign

initial_state = Val_assign(variables, No_of_Variables)

# ************************************************************************************************************************

# calculate Hueristic value via Function 
def Heuristic_Val(Expression, assign):
    count = 0
    for exp in Expression:
        l = [assign[val] for val in exp]
        count += any(l)
    return count

initial_val = Heuristic_Val(Expression, initial_state)

# ************************************************************************************************************************
output_file = open('output.txt' , 'w')
print("\n****************** Initial Declarations ******************" , file = output_file)
print("Intial Expression:" , file = output_file)
print(Expression , file = output_file)
print("Initial state:" , file = output_file)
print(initial_state , file = output_file)
print("Heuristic Value:", initial_val , file = output_file)
print("***********************************************************" , file = output_file)

# ************************************************************************************************************************

Explored_states = []

def Beam_Search(Expression, intermediate_State, beam, step_Size):

    Explored_states.append(intermediate_State)
    
    # print(intermediate_State)

    if initial_val == len(Expression):
        p = str(step_Size)
        return intermediate_State, p

    intermediate_State_Val = list(intermediate_State.values())
    intermediate_State_keys = list(intermediate_State.keys())
  
    steps = []
    possible_intermediate_States = []
    possible_states_scores = []

    #  considering all possible intermediate states form any particular state
    for i in range(int(len(intermediate_State_Val) / 2)):
        editing_intermediate_State = intermediate_State.copy()
        if intermediate_State_Val[i] == 1:
            editing_intermediate_State[intermediate_State_keys[i]] = 0
        if intermediate_State_Val[i] == 0:
            editing_intermediate_State[intermediate_State_keys[i]] = 1
        if intermediate_State_Val[i+4] == 1:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 0
        if intermediate_State_Val[i+4] == 0:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 1

        possible_intermediate_States.append(editing_intermediate_State)

        c = Heuristic_Val(Expression, editing_intermediate_State)
        possible_states_scores.append(c)

        step_Size += 1
        steps.append(step_Size)

    # sorting the intermediate states
    selected = list(np.argsort(possible_states_scores))[-beam:]

    # if we get goal state ==> exit
    if len(Expression) in possible_states_scores:
        index = [
            i
            for i in range(len(possible_states_scores))
            if possible_states_scores[i] == len(Expression)
        ]
        p = str(steps[-1])
        return possible_intermediate_States[index[0]], p
    # else consider next best-state among best beam-length elements
    else:
        selected_intermediate_States = [possible_intermediate_States[i] for i in selected]
        for a in selected_intermediate_States:
            if not a in Explored_states:
                return Beam_Search(Expression, a, beam, step_Size)

# ************************************************************************************************************************

tabu_tenure_array = [0, 0, 0, 0]
time = 0

# tabu search algo
def Tabu_Search(Expression, intermediate_State, tabu_tanure, step_Size):

    global time
    time += 1
    
    if not intermediate_State in Explored_states:
        Explored_states.append(intermediate_State)

    if initial_val == len(Expression):
        p = str(step_Size)
        return intermediate_State, p

    intermediate_State_Val = list(intermediate_State.values())
    intermediate_State_keys = list(intermediate_State.keys())

    steps = []
    possible_intermediate_States = []
    possible_states_scores = []

    # adding intermediate states depending on tabu tenure values
    for i in range(int(len(intermediate_State_Val) / 2)):

        if tabu_tenure_array[i] > 0:
            tabu_tenure_array[i] -= 1
            continue
        
        else:
            tabu_tenure_array[i] = -1

        editing_intermediate_State = intermediate_State.copy()
        if intermediate_State_Val[i] == 1:
            editing_intermediate_State[intermediate_State_keys[i]] = 0
        if intermediate_State_Val[i] == 0:
            editing_intermediate_State[intermediate_State_keys[i]] = 1
        if intermediate_State_Val[i+4] == 1:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 0
        if intermediate_State_Val[i+4] == 0:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 1
        possible_intermediate_States.append(editing_intermediate_State)

        c = Heuristic_Val(Expression, editing_intermediate_State)
        possible_states_scores.append(c)

        step_Size += 1
        steps.append(step_Size)

    if len(possible_intermediate_States) == 0:
        return Tabu_Search(Expression, intermediate_State, tabu_tanure, step_Size)

    selected = list(np.argsort(possible_states_scores))[-1:]

    if len(Expression) in possible_states_scores:
        index = [
            i
            for i in range(len(possible_states_scores))
            if possible_states_scores[i] == len(Expression)
        ]
        p = str(steps[-1])
        tempry = selected[0]
        for j in range(len(tabu_tenure_array)):
            if tabu_tenure_array[j] == -1:
                if tempry == 0:
                    tabu_tenure_array[j] = tabu_tanure
                else:
                    tabu_tenure_array[j] = 0
                tempry -= 1
        return possible_intermediate_States[index[0]], p
    else:
        selected_intermediate_States = [possible_intermediate_States[i] for i in selected]
        for x in selected_intermediate_States:
            tempry = selected[0]
            for j in range(len(tabu_tenure_array)):
                if tabu_tenure_array[j] == -1:
                    if tempry == 0:
                        tabu_tenure_array[j] = tabu_tanure
                    else:
                        tabu_tenure_array[j] = 0
                    tempry -= 1
            if not x in Explored_states:
                return Tabu_Search(Expression, x, tabu_tanure, step_Size)

# ************************************************************************************************************************

# HILL climbing for variable_neighborhood_descent 
def HILL_climbing(Expression, intermediate_State, parent_num, received, step):

    intermediate_State_Val = list(intermediate_State.values())
    intermediate_State_keys = list(intermediate_State.keys())

    max_num = parent_num
    max_Assign = intermediate_State.copy()

    for i in range(int(len(intermediate_State_Val) / 2)):

        editing_intermediate_State = intermediate_State.copy()
        best_assigned_val = intermediate_State.copy()
        if intermediate_State_Val[i] == 1:
            editing_intermediate_State[intermediate_State_keys[i]] = 0
        if intermediate_State_Val[i] == 0:
            editing_intermediate_State[intermediate_State_keys[i]] = 1
        if intermediate_State_Val[i+4] == 1:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 0
        if intermediate_State_Val[i+4] == 0:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 1
        step += 1
        c = Heuristic_Val(Expression, editing_intermediate_State)
        if max_num < c:
            received = step
            max_num = c
            max_Assign = editing_intermediate_State.copy()

    if max_num == parent_num:
        s = str(received)
        return best_assigned_val, max_num, s
    else:
        parent_num = max_num
        best_assigned_val = max_Assign.copy()
        return HILL_climbing(Expression, best_assigned_val, parent_num, received, step)

# ************************************************************************************************************************

def variable_neighborhood_descent(Expression, intermediate_State, b, step):

    Explored_states.append(intermediate_State)

    intermediate_State_Val = list(intermediate_State.values())
    intermediate_State_keys = list(intermediate_State.keys())

    steps = []
    possible_intermediate_States = []
    possible_states_scores = []

    initial_val = Heuristic_Val(Expression, intermediate_State)

    if initial_val == len(Expression):
        p = str(step)
        return intermediate_State, p, b

    for i in range(int(len(intermediate_State_Val) / 2)):

        editing_intermediate_State = intermediate_State.copy()
    
        if intermediate_State_Val[i] == 1:
            editing_intermediate_State[intermediate_State_keys[i]] = 0
        if intermediate_State_Val[i] == 0:
            editing_intermediate_State[intermediate_State_keys[i]] = 1
        if intermediate_State_Val[i+4] == 1:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 0
        if intermediate_State_Val[i+4] == 0:
            editing_intermediate_State[intermediate_State_keys[i+4]] = 1

        c = Heuristic_Val(Expression, editing_intermediate_State)
        step += 1
        possible_intermediate_States.append(editing_intermediate_State.copy())
        possible_states_scores.append(c)
        steps.append(step)

    selected = list(np.argsort(possible_states_scores))[-b:]

    if len(Expression) in possible_states_scores:
        index = [
            i
            for i in range(len(possible_states_scores))
            if possible_states_scores[i] == len(Expression)
        ]
        p = str(steps[-1])
        return possible_intermediate_States[index[0]], p, b

    else:
        selectedAssigns = [possible_intermediate_States[i] for i in selected]
        for a in selectedAssigns:
            best_assigned_val, max_num, s = HILL_climbing(Expression, a, initial_val, 1, 1)
            step += int(s)
            if max_num == len(Expression):
                Explored_states.append(a)
                return variable_neighborhood_descent (Expression, best_assigned_val, b, step)

        variable_neighborhood_descent(Expression, intermediate_State, b + 1, step)

# ************************************************************************************************************************

print("\n---------------Beam Search (Beam_Length-2)----------------\n" , file = output_file)
Explored_states.clear()
beam_length = 2
finalState, state_count = Beam_Search(Expression, initial_state, beam_length, 1)
if not finalState in Explored_states:
    Explored_states.append(finalState)
print("States Explored : " + state_count , file = output_file)
for exp in Explored_states:
    print(exp , file = output_file)

# ************************************************************************************************************************

print("\n---------------Tabu search (Tabu_Tenure-2)-----------------\n" , file = output_file)
Explored_states.clear()
tabu_tanure = 2
finalState, tabu = Tabu_Search(Expression, initial_state, tabu_tanure, 1)
if not finalState in Explored_states:
    Explored_states.append(finalState)
print("States Explored : " + tabu , file = output_file)
for exp in Explored_states:
    print(exp , file = output_file)

# ************************************************************************************************************************

print("\n--------------Variable neighborhood descent-----------------\n" , file = output_file)
Explored_states.clear()
finalState, p, bb = variable_neighborhood_descent(Expression, initial_state, 1, 1)
if not finalState in Explored_states:
    Explored_states.append(finalState)
print("States explored : ", p, sep="" , file = output_file)
for exp in Explored_states:
    print(exp , file = output_file)
print("\n------------------------------------------------------------" , file = output_file)    

# ************************************************************************************************************************
