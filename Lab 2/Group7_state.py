from copy import deepcopy

class State:
    """
    The State class. Each State object represents a possible arrangement of the blocks on the table.

            |A|
            For a state with an arrangement like this:  |B|C|

            The layout attribute is {'A': ['B', 'c'], 'B': ['-', 'u'], 'C': ['-', 'c']}.
        
            example:
            |A|           |A| 
            |B|C| ----> |B|C|   The move attribute is ['A', 'B', 'C']
        
       
    """

    def __init__(self, layout, parent = None, move = [], distance = 0):
        self.layout = layout
        self.parent = parent
        self.move = move
        self.distance = distance

        values = list(self.layout.values())     #A list of the names of the blocks.

        self.id = ''.join([str(i) for s in values for i in s])     #Create the id attribute.
    
    def __eq__(self, other_state):
        if other_state != None:
            return self.id == other_state.id
        else:
            return False

    def calcChildren(self):
        
        #The method creates a list of all the states that can be produced from a given state.
        #It moves all the clear blocks to all available destinations and creates a new state 
        #for each alteration.
        
        layout = self.layout
        children = []

        free_blocks = [key for key in layout if layout[key][1] == 'c']     #The blocks that can be moved.

        for moving_block in free_blocks:     #For each free block that will be moved...
            for target_block in free_blocks:
                if moving_block != target_block:
                    temp = deepcopy(layout)     #Copy the current layout in order to alter it.
                    move = []
                    distance = 0

                    released_block = temp[moving_block][0]     #The 'released_block' is the first item of the list in layout with key == moving_block.

                    temp[moving_block][0] = target_block     #The 'moving block' now is on top of the 'target_block'.
                    temp[target_block][1] = 'u'     #And the 'target_block' is now unclear.

                    move.append(moving_block)     #Add the 'moving_block' to 'move' list.

                    if released_block != '-':     #If the 'released_block" is not '-' i.e. is not on the table...
                        temp[released_block][1] = 'c'     #Set the block clear.

                        move.append(released_block)     #Add the 'released_block' to 'move' list.
                    else:
                        move.append('table')
                    
                    move.append(target_block)     #Add the 'target_block' to 'move' list.
                    distance = self.distance + 1     #The distance of the child is the distance of the parent plus 1.

                    children.append(State(layout = temp, parent = self, move = move, distance = distance))     #Add to 'children' list a new State object.
            
            if layout[moving_block][0] != '-':     #If the 'moving_block' is not currently on the table, create a state that it is.
                temp = deepcopy(layout)
                move = []
                distance = 0

                released_block = temp[moving_block][0]     #The 'released_block' is the first item of the list in layout with key == moving_block.

                temp[moving_block][0] = '-'
                temp[released_block][1] = 'c'     #Set the block clear.

                move.append(moving_block)     #Add the 'moving_block' to 'move' list.
                move.append(released_block)      #Add the 'released_block' to 'move' list.
                move.append('table')

                distance = self.distance + 1     #The distance of the child is the distance of the parent plus 1.

                children.append(State(layout = temp, parent = self, move = move, distance = distance))     #Add to 'children' list a new State object.
        
        return children     #Return the children list.
    
    