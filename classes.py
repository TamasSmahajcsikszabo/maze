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


test = Cell(indicator=12, name="test_Cell")
test2 = Cell(indicator=13, name="test_Cell2")
test2.section_6
test2.section_3
test2.section_9
open_wall("N", [test, test2])
open_wall("E", [test, test2])
