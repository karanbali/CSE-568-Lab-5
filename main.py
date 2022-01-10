# Importing Dependencies
import numpy as np
import sys
import matplotlib.pyplot as plt


# Plotting the positional beliefs
def plot(map,ts=1):
    plt.imshow(map, cmap='viridis', origin='lower')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.colorbar()
    if ts==1:
        plt.title("Move Map")
        plt.show(block=False)
        plt.pause(1)
        plt.close()
    else:
        plt.title("Final Map")
        plt.show()
    

# Defining the possible ending positions for the R(Right),L(Left),U(Up) & D(Down) actions relative to the map menioned in the assignment (i.e. origin at the bottom-left corner)
R = [[0,0],[0,1],[0,2]]
L = [[0,0],[0,-1],[0,-2]]
D = [[0,0],[-1,0],[-2,0]]
U = [[0,0],[1,0],[2,0]]

# Extracting the action command passed as argument in CLI
dr = sys.argv[1]

# Getting the number of actions mentioned in the command
command_length = len(dr)

# Initial position
init_x = 8
init_y = 5

# Position belief map
map = np.zeros((10,20))

# Initializing the starting position with full probability (i.e. 1)
map[init_y,init_x] = 1

# Plotting initial map
plot(map)


# Defining the transition probability for the possible actions (i.e. doesn't move, moves by 1 unit, moves by 2 units)
prob = [0.2,0.6,0.2]
 
# Loop through all given actions in the command
for iter in range(command_length):

    # Assign 'turn' variable depending upon the particular action mentioned in the command
    if dr[iter] == 'R':
        turn = R
    elif dr[iter] == 'L':
        turn = L
    elif dr[iter] == 'U':
        turn = U
    elif dr[iter] == 'D':
        turn = D

    # Initialize a temporary variable 'cmap' (with similar dimensions as 'map')
    # We'll use 'cmap' to calculate the change in position belief due to just current action relative to the previous position belief (i.e. 'map')
    cmap = np.zeros((10,20))

    # Loop through all map positions
    for i in range(10):
        for j in range(20):
            
            # Extract the previous position belief for the [i,j] element from the 'map'
            pij = map[i,j]

            # Change the position belief for the [i,j] element from the 'map' to 0
            map[i,j] = 0

            # Temporary variable to hold new calculated positional beliefs due just current action
            temp = []

            # Temporary variable to hold position coordinates for the respective beliefs in the 'temp'
            t = []
            
            # Loop through all posible end (position) points for a given action (i.e. 3)
            for k in range(3):
                
                # Get possible end position
                ik = i + turn[k][0]
                jk = j + turn[k][1]

                # save possible end position
                t.append([ik,jk])
                
                # save new calculated positional beliefs due just current action using previous positional belief
                # Idea is to take previous belief and distribute it among other positions (in proportion to transition probability)
                temp.append(pij*prob[k])

            
            # Loop through all posible end (position) points for a given action (i.e. 3)
            # This timwe we loop to update the temporary 'cmap'
            for k in range(3):

                # Get possible end position
                ti = t[k][0]
                tj = t[k][1]

                # Check if possible end positions can be out of bounds
                if ti >9 or ti <0 or tj >19 or tj <0:

                    # If end position is the second possibilty
                    if k == 1:
                        # Accumulate probability of positions out of bound
                        pro = temp[1] + temp[2]

                        # If probability is not 0.0
                        if pro != 0.0:

                            # Add the accumulated probability to the last in bound position
                            cmap[t[k-1][0],t[k-1][1]] += pro

                    # If end position is the third possibilty
                    elif k == 2:

                        # Accumulate probability of positions out of bound
                        pro = temp[2]

                        # If probability is not 0.0
                        if pro != 0.0:

                            # Add the accumulated probability to the last in bound position
                            cmap[t[k-2][0],t[k-2][1]] += pro

                # Else (if position is in-bound)
                else:

                    # Get the new calculated probability
                    pro = temp[k]

                    # If probability is not 0.0
                    if pro != 0.0:

                        # Add the probability to the particular position on temporary 'cmap'
                        cmap[t[k][0],t[k][1]] += pro 
                    
                        
    # Update 'map' by adding 'cmap' (i.e. change in position belief due to just current action relative to the previous position belief)  
    map = np.add(map,cmap)

    # Plotting 'map' on a pyplot heatmap (It'll close after '1 sec')
    plot(map)


# Plotting Final 'map' (This won't get close after '1 sec' as it's the last one)
plot(map,0)
