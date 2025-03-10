import numpy as np

def occupancy_grid_to_coordinates(grid):
    '''
    Convert an occupancy grid (NumPy array) into a list of (x, y) coordinates
    where the value is 1 (valid path).

    Arguments:
        grid: A 2D NumPy array where 1 represents a valid path coordinate and 0 represents nothing.

    Returns:
        A list of tuples, where each tuple contains the (x, y) indices of the valid path coordinates.
    '''
    # Use np.argwhere to find the indices of all elements that are 1
    coordinates = np.argwhere(grid == 1)
    
    # Convert the coordinates from (row, column) format to (x, y) format
    # In NumPy, the first index is the row (y), and the second is the column (x)
    coordinates = [(coord[1], coord[0]) for coord in coordinates]
    
    return coordinates


def toTextFile(outfile, shapes):
    '''
    Print the coordinates to a text file formatted in G code.
    
    Arguments:
        shapes is of type list. It contains sublists of tuples that correspond
                                to (x, y) coordinates.
    '''

    file = open(outfile, "w")
    
    # Boilerplate text:
    # G17: Select X, Y plane
    # G21: Units in millimetres
    # G90: Absolute distances
    # G54: Coordinate system 1
    file.write("G17 G21 G90 G54\n")
    
    # Start at origin (0, 0)
    file.write("G00 X0. Y0.\n")

    up = True
    
    # Assume Z0 is down and cutting and Z1 is retracted up
    for shape in shapes:
        for i in range(len(shape)):
            # If coordinate is an integer, append a decimal point
            if (shape[i][0] % 1.0 == 0): xstr = str(shape[i][0]) + "."
            else: xstr = str(shape[i][0])
            
            if (shape[i][1] % 1.0 == 0): ystr = str(shape[i][1]) + "."
            else: ystr = str(shape[i][1])

            # Write coordinate to file
            file.write("X" + xstr + " Y" + ystr + "\n")

            # When arrived at point of new shape, start cutting
            if up == True:
                file.write("Z0.\n")
                up = False
        # When finished shape, retract cutter
        file.write("Z1.\n")
        up = True
    # Return to origin (0, 0) when done, then end program with M2
    file.write("X0. Y0.\nM2")

    file.close()