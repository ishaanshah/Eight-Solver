# Game logic and design by arnisritins. https://github.com/arnisritins/15-Puzzle.

import time
from operator import attrgetter
from selenium import webdriver

# Initialize webdriver to communicate with webpage
driver = webdriver.Chrome(r"C:\Users\ishaa\chromedriver.exe")
driver.get("file:///F:/Projects/PycharmProjects/fifteen_solver/15-Puzzle/index.html")

# grid for puzzle
grid = []

# solved state of puzzle
solved_grid = []

# structure to store coordinates
class Tile:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

# structure for nodes
class Node:
    def __init__(self, config, parent, f, g):
         self.config = config
         self.parent = parent
         self.f = f
         self.g = g


def a_star():
    get_current_state()
    start = Node(grid, None, None, 0)
    start.f = heuristic(start)
    end = Node(solved_grid, None, None, None)

    closed_set = []
    open_set = [start]

    while len(open_set) != 0:
        current = min(open_set, key = attrgetter("f"))

        if current.config == end.config:
            return reconstruct_moves(closed_set, current)

        open_set.remove(current)
        closed_set.append(current)

        for neighbour in find_neighbours(current):
            if neighbour in closed_set:
                continue

            if neighbour not in open_set:
                open_set.append(neighbour)

            neighbour.parent = current
            neighbour.f = neighbour.g + heuristic(neighbour)

    return False


# finds the neighnours of current config
def find_neighbours(node):
    for tile in node.config:
        if tile.num == 0:
            zero_tile = tile
            break

    neighbours = []
    for tile in node.config:
        if zero_tile.x + 1 == tile.x and zero_tile.y == tile.y:
            neighbours.append(Node(swap(zero_tile, tile, node.config), None, None, node.g + 1))
            break

    for tile in node.config:
        if zero_tile.x - 1 == tile.x and zero_tile.y == tile.y:
            neighbours.append(Node(swap(zero_tile, tile, node.config), None, None, node.g + 1))
            break

    for tile in node.config:
        if zero_tile.y - 1 == tile.y and zero_tile.x == tile.x:
            neighbours.append(Node(swap(zero_tile, tile, node.config), None, None, node.g + 1))
            break

    for tile in node.config:
        if zero_tile.y + 1 == tile.y and zero_tile.x == tile.x:
            neighbours.append(Node(swap(zero_tile, tile, node.config), None, None, node.g + 1))
            break

    return neighbours


# find heuristics
def heuristic(node):
    dist = []
    for tile in node.config:
        for solved_tile in solved_grid:
            if solved_tile.num == tile.num:
                dist.append(manhattan_distance(tile, solved_tile))

    return sum(dist)

# get current state of board
def get_current_state():
    # empty the list
    grid[:] = []
    for i in range(0, 4):
        for j in range(0, 4):
            # get the tile from web page
            tile = driver.find_element_by_id("cell-{}-{}".format(i, j)).text

            # check for empty tile
            if tile == '':
                # set empty tile as 0
                tile = "0"

            # insert coordinates of tile in grid
            grid.append(Tile(i, j, int(tile)))


# find the taxicab distance between two points
def manhattan_distance(start, end):
    return abs(start.x - end.x) + abs(start.y - end.y)


def scramble():
    driver.find_element_by_id("scramble").click()# wait for animation
    time.sleep(0.6) # wait for animation


# submit a number
def submit(tile):
    input_box = driver.find_element_by_id("number")
    input_box.send_keys(str(tile))
    submit_btn = driver.find_element_by_id("submit")
    submit_btn.click()
    time.sleep(0.3) # wait for animation


def swap(tile1, tile2, temp):
    s_grid = [i for i in temp]
    t1_index = s_grid.index(tile1)
    t2_index = s_grid.index(tile2)
    s_grid[t2_index] = tile1
    s_grid[t1_index] = tile2
    return s_grid


def reconstruct_moves(open_set, current):
    total_path = [current]
    while current in open_set.parent.Keys:
        current = cameFrom[current]
        total_path.append(current)
    return total_path


def win(temp):
    

def main():
    # create a solved board
    num = 1
    for i in range(4):
        for j in range(4):
            if i == 3 and j == 3:
                solved_grid.append(Tile(i, j, 0))
            else:
                solved_grid.append(Tile(i, j, num))
                num += 1

    scramble()
    print(a_star())

if __name__ == "__main__":
    main()
