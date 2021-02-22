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


def find_unbroken_corridors(matrix, algorithm="BT"):
    if algorithm == "BT":
        northern_corridor = [e for e in matrix[0]]
        eastern_corridor = [max(r) for r in matrix]
        return (northern_corridor, eastern_corridor)

    if algorithm == "sidewinder":
        norhern_corridor = matrix[0]
        return norhern_corridor


def find_boundaries(matrix, combined=True, algorithm="BT"):
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
        if combined:
            return (horizontal, vertical)
        else:
            return [northern_corridor, southern_corridor,
                    eastern_corridor, western_corridor]

def get_base_components(size=3):
    cellmatrix = get_matrix(size, size)
    corners = [i for i in get_corners(cellmatrix)]

    NW_corner = Corner("NW", indicator=corners[0], name="NW_corner")
    NE_corner = Corner("NE", indicator=corners[1], name="NE_corner")
    SW_corner = Corner("SW", indicator=corners[2], name="SW_corner")
    SE_corner = Corner("SE", indicator=corners[3], name="SE_corner")
    north_wall, south_wall, east_wall, west_wall = find_boundaries(
        cellmatrix, combined=False)
    occupied_space = []
    for container in [corners, north_wall, south_wall, east_wall, west_wall]:
        occupied_space.extend(container)
    room_spaces = [i for i in range(size*size) if i not in occupied_space]

    N_walls = [Wall(orientation="N", indicator=i, name="N_wall")
               for i in north_wall]
    S_walls = [Wall(orientation="S", indicator=i, name="S_wall")
               for i in south_wall]
    rooms = [Room(indicator=i, name="room") for i in room_spaces]
    W_walls = [Wall(orientation="W", indicator=i, name="W_wall")
               for i in west_wall]
    E_walls = [Wall(orientation="E", indicator=i, name="E_wall")
               for i in east_wall]

    components = [
        NW_corner,
        N_walls,
        NE_corner,
        E_walls,
        rooms,
        W_walls,
        SE_corner,
        S_walls,
        SW_corner]

    return components

def get_middle_value(x):
    if x % 2 == 1:
        for i in range(x):
            first = list(range(0, i))
            second = list(range(i+1, x))
            if len(first) == len(second):
                return i
    else:
        result  = get_middle_value(x-1)
        return [result, result+1]

def open_wall(orientation, cells):
    # first cell is either northern or western
    wall_length = cells[0].wall_length
    if len(cells) == 2:
        if wall_length % 2 == 1:
            middle = str(get_middle_value(wall_length))

            if orientation == "N":

                getattr(cells[0], "S_wall"+middle).body = "╕ ╒"
                getattr(cells[1], "N_wall"+middle).body = "╛ ╘"

            if orientation == "E":
                getattr(cells[0], "E_wall"+middle).body = " "
                getattr(cells[1], "W_wall"+middle).body = " "

    else:
        pass

class Cell(Component):
    def __init__(self, size=3, **kargs):
        Component.__init__(self, **kargs)
        components = get_base_components(size=size)
        self.size = size
        self.components = []
        self.matrix = get_matrix(x=size, y=size)
        self.wall_length = self.size - 2
        for component in components:
            if isinstance(component, list):
                for i in range(len(component)):
                    if component[i].__class__.__name__ == "Room":
                        setattr(self, component[i].name + str(i), component[i])
                        self.components.append(component[i])
                    elif component[i].__class__.__name__ == "Wall":
                        setattr(self, component[i].name + str(i), component[i])
                        self.components.append(component[i])
            else:
                setattr(self, component.name, component)
                self.components.append(component)

        for i in [max(m)+1 for m in self.matrix]:
            section = []
            if i == size:
                r = range(i)
            else:
                r = range(i-size, i)
            for y in r:
                for component in self.components:
                    if y == component.indicator:
                        section.append(component)
            setattr(self, 'section_' + str(i), section)

    def __repr__(self):
        cellstring = ""
        for i in range(self.size*self.size):
            for component in self.components:
                if i == component.indicator:
                    if i in [max(e) for e in self.matrix]:
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
                        if cell.indicator not in collapse_to_list(
                                selfObject.unbroken_corridors):
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

    elif selfObject.algorithm == "sidewinder":
        container = []
        for row in range(len(selfObject.matrix)-1, -1, -1):
            for c in range(selfObject.x):
                selected_indicator = selfObject.matrix[row][c]
                for cell in selfObject.cells:
                    if cell.indicator == selected_indicator:
                        if cell.indicator in find_boundaries(selfObject.matrix, combined=False)[
                                                             2] or cell.indicator == selfObject.corners[3]:
                            other_cell = [
                                cell for cell in selfObject.cells
                                if cell.indicator == selfObject.matrix
                                [row - 1][c]][0]
                            open_wall("N", [other_cell, cell])
                        elif cell.indicator not in collapse_to_list(find_unbroken_corridors(
                                selfObject.matrix)):
                            v = rand.randint(0, 2)
                            if v == 0:
                                other_cell = [
                                    cell for cell in selfObject.cells
                                    if cell.indicator == selfObject.matrix[row]
                                    [c + 1]][0]
                                open_wall("E", [cell, other_cell])
                                container.append(cell)
                            elif v == 1:
                                container.append(cell)
                                selection = rand.randint(0, len(container))
                                selected_cell = container[selection]
                                container = []
                                for r in range(selfObject.y):
                                    if selected_cell.indicator in selfObject.matrix[r]:
                                        selected_cell_position = [
                                            i for i in range(selfObject.x)
                                            if selected_cell.indicator
                                            == selfObject.matrix[r][i]][0]
                                other_cell = [
                                    cell for cell in selfObject.cells
                                    if cell.indicator == selfObject.matrix
                                    [row - 1][selected_cell_position]][0]
                                open_wall("N", [other_cell, selected_cell])
                        elif cell.indicator in find_unbroken_corridors(selfObject.matrix)[0] and cell.indicator not in [selfObject.corners[i] for i in [1]]:
                            other_cell = [
                                cell for cell in selfObject.cells
                                if cell.indicator == selfObject.matrix[row]
                                [c + 1]][0]
                            open_wall("E", [cell, other_cell])


class Maze(Component):
    def __init__(self, x, y, cellsize=4, algorithm="BT",  **kargs):
        Component.__init__(self, **kargs)
        self.x = x
        self.y = y
        self.cellsize = cellsize
        self.matrix = get_matrix(x, y)
        self.cells = [
            Cell(indicator=i, size = self.cellsize, name="")
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
            for section in ['section_'+str(max(m)+1) for m in get_matrix(x=self.cellsize, y=self.cellsize)]:
                for i in row:
                    for selected_cell in self.cells:
                        if selected_cell.indicator == i:
                            maze_string = maze_string + \
                                merge_objects(selected_cell[section])
                maze_string = maze_string + "\n"
        return maze_string


# quick checks
test_maze = Maze(x=14, y=10, cellsize=3, indicator=1, name="test_maze")
test_maze2 = Maze(
    x=14,
    y=10,
    cellsize=3,
    algorithm="sidewinder",
    indicator=2,
    name="test2")

# TODO
# free isolated cells
# change cell size
# add items
# framerate
