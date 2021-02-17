import numpy.random as rand


def get_matrix(x=10, y=10):
    cells = list(range(x * y))
    matrix = list()
    for i in range(x):
        row = list()
        index = cells[i * y: y * i + y]
        for c in index:
            row.append(cells[c])
        matrix.append(row)

    return matrix


class Component:
    def __init__(self, indicator, name, body=""):
        self.indicator = indicator
        self.name = name
        self.body = body

    def __repr__(self):
        return self.body


class Corner(Component):
    def __init__(self, orientation, **kargs):
        Component.__init__(self, **kargs)
        self.orientation = orientation

        if orientation == "NE":
            self.body = "╗"
        elif orientation == "NW":
            self.body = "╔"
        elif orientation == "SE":
            self.body = "╝"
        elif orientation == "SW":
            self.body = "╚"


class Wall(Component):
    def __init__(self, orientation, **kargs):
        Component.__init__(self, **kargs)
        self.orientation = orientation

        if orientation == "N":
            self.body = "═══"
        elif orientation == "S":
            self.body = "═══"
        elif orientation == "E":
            self.body = "║"
        elif orientation == "W":
            self.body = "║"


class Room(Component):

    def __init__(self, **kargs):
        Component.__init__(self, **kargs)
        self.body = "   "


def get_base_components():
    NE_corner = Corner("NE", indicator=2, name="NE_corner")
    NW_corner = Corner("NW", indicator=0, name="NW_corner")
    N_wall = Wall(orientation="N", indicator=1, name="N_wall")
    SE_corner = Corner("SE", indicator=8, name="SE_corner")
    SW_corner = Corner("SW", indicator=6, name="SW_corner")
    S_wall = Wall(orientation="S", indicator=7, name="S_wall")
    room = Room(indicator=4, name="room")
    W_wall = Wall(orientation="W", indicator=3, name="W_wall")
    E_wall = Wall(orientation="E", indicator=5, name="E_wall")

    components = [
        NW_corner,
        N_wall,
        NE_corner,
        E_wall,
        room,
        W_wall,
        SE_corner,
        S_wall,
        SW_corner]

    return components


def get_matrix(x=10, y=10):
    cells = list(range(x * y))
    matrix = list()
    for i in range(y):
        row = list()
        index = cells[i * x: x * i + x]
        for c in index:
            row.append(cells[c])
        matrix.append(row)

    return matrix


def open_wall(orientation, cells):
    # first cell is either northern or western
    if len(cells) == 2:

        if orientation == "N":
            cells[0].S_wall.body = "╕ ╒"
            cells[1].N_wall.body = "╛ ╘"

        if orientation == "E":
            cells[0].E_wall.body = " "
            cells[1].W_wall.body = " "

    else:
        pass


class Cell(Component):
    def __init__(self, **kargs):
        Component.__init__(self, **kargs)
        components = get_base_components()
        self.components = components
        for component in components:
            setattr(self, component.name, component)

        for i in [3, 6, 9]:
            section = []
            if i == 3:
                r = range(i)
            else:
                r = range(i-3, i)
            for y in r:
                for component in self.components:
                    if y == component.indicator:
                        section.append(component)
            setattr(self, 'section_' + str(i), section)

    def __repr__(self):
        cellstring = ""
        for i in range(9):
            for component in self.components:
                if i == component.indicator:
                    if i in [2, 5, 8]:
                        cellstring = cellstring + component.body + "\n"
                    else:
                        cellstring = cellstring + component.body

        return cellstring

    def __getitem__(self, section):
        return getattr(self, section)


def merge_objects(section):
    string = ""
    for component in section:
        string = string + component.body

    return string


def get_corners(m):
    NW = min(m[0])
    NE = max(m[0])
    SW = min(m[len(m)-1])
    SE = max(m[len(m)-1])
    return (NW, NE, SW, SE)


def find_unbroken_corridors(matrix, algorithm="BT"):
    if algorithm == "BT":
        northern_corridor = [e for e in matrix[0]]
        eastern_corridor = [max(r) for r in matrix]
        return (northern_corridor, eastern_corridor)

    if algorithm == "SW":
        norhern_corridor = matrix[0]
        return norhern_corridor


def find_boundaries(matrix, algorithm="BT"):
    if algorithm == "BT":
        corners = get_corners(matrix)
        northern_corridor = [i for i in matrix[0] if i not in corners]
        southern_corridor = [
            i for i in matrix[len(matrix)-1] if i not in corners]
        eastern_corridor = [max(r) for r in matrix if max(r) not in corners]
        western_corridor = [min(r) for r in matrix if min(r) not in corners]
        horizontal = []
        [horizontal.extend(l) for l in (northern_corridor, southern_corridor)]
        vertical = []
        [vertical.extend(l) for l in (eastern_corridor, western_corridor)]
        return (horizontal, vertical)


def collapse_to_list(tupl):
    result = []
    [result.extend(i) for i in tupl]
    return result

def generate_maze(selfObject):
    # Binary Tree algorithm
        if selfObject.algorithm == "BT":
            for row in range(len(selfObject.matrix)-1, -1, -1):
                for c in range(selfObject.x):
                    selected_indicator = selfObject.matrix[row][c]
                    for cell in selfObject.cells:
                        if cell.indicator == selected_indicator:
                            if cell.indicator not in collapse_to_list(selfObject.unbroken_corridors):
                                v = rand.randint(0, 2)
                                if v == 0:
                                    other_cell = [
                                        cell for cell in selfObject.cells
                                        if cell.indicator == selfObject.matrix
                                        [row - 1][c]][0]
                                    open_wall("N", [other_cell, cell])
                                elif v == 1:
                                    other_cell = [
                                        cell for cell in selfObject.cells
                                        if cell.indicator == selfObject.matrix[row]
                                        [c + 1]][0]
                                    open_wall("E", [cell, other_cell])
                            elif cell.indicator in selfObject.unbroken_corridors[0] and cell.indicator not in selfObject.corners:
                                other_cell = [
                                    cell for cell in selfObject.cells
                                    if cell.indicator == selfObject.matrix[row]
                                    [c + 1]][0]
                                open_wall("E", [cell, other_cell])
                            elif cell.indicator in selfObject.unbroken_corridors[1] and cell.indicator not in selfObject.corners:
                                other_cell = [
                                    cell for cell in selfObject.cells
                                    if cell.indicator == selfObject.matrix
                                    [row - 1][c]][0]
                                open_wall("N", [other_cell, cell])
                            elif cell.indicator == [i for i in selfObject.corners][0]:
                                other_cell = [
                                    cell for cell in selfObject.cells
                                    if cell.indicator == selfObject.matrix[row]
                                    [c + 1]][0]
                                open_wall("E", [cell, other_cell])
                            elif cell.indicator == [i for i in selfObject.corners][3]:
                                other_cell = [
                                    cell for cell in selfObject.cells
                                    if cell.indicator == selfObject.matrix
                                    [row - 1][c]][0]
                                open_wall("N", [other_cell, cell])


class Maze(Component):
    def __init__(self, x, y, algorithm="BT",  **kargs):
        Component.__init__(self, **kargs)
        self.x = x
        self.y = y
        self.matrix = get_matrix(x, y)
        self.cells = [
            Cell(indicator=i, name="")
            for i in [row[i] for row in self.matrix for i in range(
                         len(row))]]
        self.algorithm = algorithm

        self.boundaries = find_boundaries(
            self.matrix, algorithm=self.algorithm)
        self.unbroken_corridors = find_unbroken_corridors(
            self.matrix, algorithm="BT")
        self.corners = get_corners(self.matrix)
        self.generate()

    def generate(self):
        generate_maze(self)



    def __repr__(self):
        maze_string = ""
        for row in self.matrix:
            for section in ["section_3", "section_6", "section_9"]:
                for i in row:
                    for selected_cell in self.cells:
                        if selected_cell.indicator == i:
                            maze_string = maze_string + \
                                merge_objects(selected_cell[section])
                maze_string = maze_string + "\n"
        return maze_string

test_maze = Maze(x=14, y=10, indicator=1, name="test_maze")
matrix = get_matrix()
get_corners(matrix)
test_maze.matrix
test_maze.unbroken_corridors[0]
test_maze.corners
test_maze.boundaries
