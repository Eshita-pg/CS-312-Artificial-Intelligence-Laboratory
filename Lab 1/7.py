from numpy.core.fromnumeric import shape
import sys
Open_Lists = set()

sys.setrecursionlimit(10**6)

# DFS Stop Indication
DFS_stop_chcek = False  
# target co-ordinate in DFS 
Goal_DFS = (0, 0)
# target co-ordinate in DFID      
Goal_DFID = (0, 0)    
# no. of states in DFS 
States_in_DFS = 0  
# no. of states in DFID    
states_in_DFID = 0       
# DFID Stop Indication and braek point for recursion
DFID_Stop_check = False    


def GoalTest(i, j, MAZE_input):
    
    if(MAZE_input[i][j] == '*'):
        return True
    else:
        return False


def MoveGen(i, j, MAZE_input):

    global Open_Lists

    Temp_lists = []
    
    # This part is for the priority order of  Up > Down > Right > Left
    if(i<column-1):
        if((MAZE_input[i+1][j]==' ' or MAZE_input[i+1][j]=='*') and ((i+1,j) not in Open_Lists)):
            Temp_lists.append((i+1,j))
    if(i>0):
        if(MAZE_input[i-1][j]==' 'or MAZE_input[i-1][j]=='*') and ((i-1,j) not in Open_Lists):
            Temp_lists.append((i-1,j))
    if(j<column-1):
        if(MAZE_input[i][j+1]==' 'or MAZE_input[i][j+1]=='*')and ((i,j+1) not in Open_Lists):
            Temp_lists.append((i,j+1))
    if(j>0):
        if(MAZE_input[i][j-1]==' 'or MAZE_input[i][j-1]=='*') and ((i+1,j) not in Open_Lists):
            Temp_lists.append((i,j-1))
            
    return Temp_lists

# commented part is for the priority order of Right > Left > Down > Up
    # if(j < column-1):
    #     if(MAZE_input[i][j+1] == ' ' or MAZE_input[i][j+1] == '*') and ((i, j+1) not in Open_Lists):
    #         Temp_lists.append((i, j+1))
    # if(j > 0):
    #     if(MAZE_input[i][j-1] == ' ' or MAZE_input[i][j-1] == '*') and ((i+1, j) not in Open_Lists):
    #         Temp_lists.append((i, j-1))
    # if(i < column-1):
    #     if((MAZE_input[i+1][j] == ' ' or MAZE_input[i+1][j] == '*') and ((i+1, j) not in Open_Lists)):
    #         Temp_lists.append((i+1, j))
    # if(i > 0):
    #     if(MAZE_input[i-1][j] == ' ' or MAZE_input[i-1][j] == '*') and ((i-1, j) not in Open_Lists):
    #         Temp_lists.append((i-1, j))
    # return Temp_lists 
    
    
def DFS_Recursive(v, visited, prnts, MAZE_input, open_list):

    global DFS_stop_chcek, Goal_DFS, States_in_DFS
    if DFS_stop_chcek:
        return

    visited.add(v)

    Temp_lists = MoveGen(v[0], v[1], MAZE_input)

    for neghbor in Temp_lists:
        if neghbor not in open_list:
            open_list.add(neghbor)
    States_in_DFS += 1
    for neghbor in Temp_lists:
        if neghbor not in prnts:
            prnts[neghbor] = v
            open_list.add(neghbor)

            if GoalTest(neghbor[0], neghbor[1], MAZE_input):
                Goal_DFS = neghbor
                DFS_stop_chcek = True
            if DFS_stop_chcek:
                return
            DFS_Recursive(neghbor, visited, prnts, MAZE_input, open_list)
            if DFS_stop_chcek:
                return


def DFS(MAZE_input, v=(0, 0)):
    global Goal_DFS, States_in_DFS
 
    visited = set()
    prnts = {}

    DFS_Recursive(v, visited, prnts, MAZE_input, Open_Lists)

    path = [v, Goal_DFS]
    x = Goal_DFS

    while x != (0, 0):
        path.append(prnts[x])
        x = prnts[x]

    return path, States_in_DFS

def DFID(MAZE_input, depth, v=(0, 0)):
    global Goal_DFID, states_in_DFID
  
    visited = set()

    prnts = {}

    DFID_recursive(v, visited, prnts, MAZE_input, depth)

    PATH = [v, Goal_DFS]

    x = Goal_DFS 

    while x != (0, 0):

        PATH.append(prnts[x])
        x = prnts[x]
    return PATH, states_in_DFID

def DFID_recursive(v, visited, prnts, MAZE_input, depth):
    if depth == 0:
        return
    global DFID_Stop_check, Goal_DFS, states_in_DFID, Open_Lists
    if DFID_Stop_check:
        return

    visited.add(v)

    templist = MoveGen(v[0], v[1], MAZE_input)
    for neighbour in templist:
        if neighbour not in Open_Lists:
            Open_Lists.add(neighbour)

    for neighbour in templist:
        if depth == 0:
            return
        if neighbour not in visited:
            prnts[neighbour] = v
            states_in_DFID += 1
            if GoalTest(neighbour[0], neighbour[1], MAZE_input):
                Goal_DFS = neighbour
                DFID_Stop_check = True
            if DFID_Stop_check:
                return

            DFID_recursive(neighbour, visited, prnts, MAZE_input, depth-1)
            if DFID_Stop_check or depth == 0:
                return


def dfid(MAZE_input, v=(0, 0)):
    depth = 1
    global Open_Lists
    while not DFID_Stop_check:
        PATH, statesdfid = DFID(MAZE_input, depth)
        Open_Lists = set()
        depth += 1

    return PATH, statesdfid

def BFS(MAZE_input, s=(0, 0)):
    visited = {}
    end = 0

    queue = []
    states = 0

    Parents = {}
    queue.append(s)
    visited[s] = True

    while queue:

        s = queue.pop(0)

        templist = MoveGen(s[0], s[1], MAZE_input)

        for i in templist:

            if i not in visited:
                states += 1
                queue.append(i)
                Parents[i] = s

                visited[i] = True
                if(GoalTest(i[0], i[1], MAZE_input)):
                    end = 1
                    break
        if end == 1:
            break

    PATH = [s, i]
    x = i

    while x != (0, 0):
        PATH.append(Parents[x])
        x = Parents[x]
    return PATH, states

def Traversdal(bdd, MAZE_input):
    if bdd == 0:
        print("BFS")
        PATH, states = BFS(MAZE_input)
    elif bdd == 1:
        PATH, states = DFS(MAZE_input)
        print("DFS")
    else:
        PATH, states = dfid(MAZE_input)
        print("DFID")
        
    for i in PATH:
        MAZE_input[i[0]][i[1]] = '0'
    return MAZE_input, states, len(PATH)

MAZE_input = []
FP = open("7_input.txt", "r")
Rows = FP.readlines()
maze = len(Rows)-1 
BFS_DFS_DFID = int(Rows[0])
for i in range(1, maze+1):
    X = Rows[i]
    MAZE_input.append(list(X[:len(X)-1]))

column = len(MAZE_input[0])

MAZE_input, states, PATH_Len = Traversdal(BFS_DFS_DFID, MAZE_input)

OP = open("output.txt", "w")
OP.write(f"NO. of States = {states+1}\nPath Length = {PATH_Len-1}")
for i in MAZE_input:
    strin = ''.join(map(str, i))
    OP.write("\n")
    OP.write(strin)
OP.write("+")
OP.close()


