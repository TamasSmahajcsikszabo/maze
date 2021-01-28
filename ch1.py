# perfect maze vs braid maze
# unicursal vs multicursal mazes: unicursal is a non-branching passage, a.k.a.
# labyrinth


# binary tree algorithm
# at each cell: do you carve a passage to N or E
# by *visiting* each cell
# visiting in some order means *walking* the grid
# the generated maze in itself is a binary tree with the northeast cell is athe
# root and the all others are either leaf nodes or parents
# BT gives unbrokenc corridors: norhern row and eastern column

# a perfect maze is a maze where exist exactly one passage between any two
# cells

# texture of a maze: a general term to descirbe patterns and characteristics in
# the maze such as passage length and direction
# some alogrithms produce mazes with similar texture
# BT always poduces unbroken corridors along N and E borders, and direction is
# diagonal to NE
# this means a given algorithm is biased toward mazes with particular texture

import numpy.random as rand
# Binary Tree
def get_matrix(x=10, y=10):
    cells = list(range(x * y))
    matrix = list()
    for i in range(x):
        row = list()
        index = cells[i * y : y * i + y]
        for c in index:
            row.append(cells[c])
        matrix.append(row)

    return matrix

def get_corners(m):
    NW = min(m[0])
    NE = max(m[0])
    SW = min(m[len(m)-1])
    SE = max(m[len(m)-1])
    return (NW, NE, SW, SE)

def find_unbroken_corridors(matrix, algorithm="BT"):
    if algorithm == "BT":
        northern_corridor = m[0]
        eastern_corridor = [max(r) for r in m]
        return (northern_corridor, eastern_corridor)

def find_boundaries(matrix, algorithm="BT"):
    if algorithm == "BT":
        northern_corridor = [i for i in m[0] if i not in get_corners(m)]
        southern_corridor = [i for i in m[len(matrix)-1] if i not in get_corners(m)]
        eastern_corridor = [max(r) for r in m if max(r) not in get_corners(m)]
        western_corridor = [min(r) for r in m if min(r) not in get_corners(m)]
        horizontal=[]
        [horizontal.extend(l) for l in (northern_corridor, southern_corridor)]
        vertical =[]
        [vertical.extend(l) for l in (eastern_corridor, western_corridor)]
        return (horizontal, vertical)


def draw_maze(m):
    corner = "*"
    up = "| "
    side_down = "=="
    side_up = "|"
    corners = get_corners(m)
    boundaries = find_boundaries(m)
    unbroken = find_unbroken_corridors(m)
    frame = ""
    cell = "  "

    for row in m:
        for element in row:
            if element in corners:
                frame = frame + corner
            elif element in boundaries[0]:
                frame = frame + side_down
            elif element in unbroken:
                frame  = frame + cell
            elif element in boundaries[1]:
                frame = frame + side_up
            else:
                v = rand.randint(0,2)
                if v == 0:
                    frame = frame + side_down
                else:
                    frame = frame + up
        frame = frame + "\n"
    return frame

m = get_matrix(x = 40, y = 30)
[print(draw_maze(m)) for i in range(10)]
