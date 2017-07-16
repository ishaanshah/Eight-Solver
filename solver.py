# Game logic and design by arnisritins. https://github.com/arnisritins/15-Puzzle.

import time
from operator import attrgetter
from selenium import webdriver

# Initialize webdriver to communicate with webpage
driver = webdriver.Chrome(r"C:\Users\ishaa\chromedriver.exe")
driver.get("file:///F:/Projects/PycharmProjects/fifteen_solver/15-Puzzle/index.html")

# grid for puzzle
grid = [[i for i in range(4)] for j in range(4)]

# solved state of puzzle
solved_grid = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,0]]

# structure for nodes
class Node:
    def __init__(self, config, parent, f, g):
         self.config = config
         self.parent = parent
         self.f = f
         self.g = g


def a_star():
    get_current_state()
    start = Node(grid, None, 0, 0)
    end = Node(solved_grid, None, None, None)

    closed_list = []
    open_list = [start]

    while len(open_set) != 0:
        current = min(open_set, key = attrgetter("f"))

        if win(current.config):
            return True

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
    j = [j for j in node.config if 0 in j][0]
    zero_x = node.config.index(j)
    zero_y = j.index(0)
    neigbours = []
    neigbour = [i for i in node.config]

    if zero_x + 1 <= 3:
        neigbour[zero_x + 1][zero_y], neigbour[zero_x][zero_y] = neigbour[zero_x][zero_y], neigbour[zero_x + 1][zero_y]
        neigbours.append(neigbour)

    if zero_x - 1 >= 0:
        neigbour[zero_x - 1][zero_y], neigbour[zero_x][zero_y] = neigbour[zero_x][zero_y], neigbour[zero_x - 1][zero_y]
        neigbours.append(neigbour)

    if zero_y + 1 <= 3:
        neigbour[zero_x][zero_y + 1], neigbour[zero_x][zero_y] = neigbour[zero_x][zero_y], neigbour[zero_x][zero_y + 1]
        neigbours.append(neigbour)

    if zero_y - 1 >= 0:
        neigbour[zero_x][zero_y - 1], neigbour[zero_x][zero_y] = neigbour[zero_x][zero_y], neigbour[zero_x][zero_y - 1]
        neigbours.append(neigbour)

    return neigbours

# find heuristics
def heuristic(node):
    dist = []
    for i in range(16):
        j = [j for j in solved_grid if i in j][0]
        s_x = solved_grid.index(j)
        s_y = j.index(i)
        k = [k for k in node.config if i in k][0]
        n_x = node.config.index(k)
        n_y = k.index(i)
        dist.append(abs(s_x - n_x) + abs(s_y - n_y))

    return sum(dist)

# get current state of board
def get_current_state():
    # empty the list
    grid[:] = []
    for i in range(4):
        row = []
        for j in range(4):
            tile = driver.find_element_by_id("cell-{}-{}".format(i, j)).text
            # check for black tile
            if tile == '':
                tile ="0"
            row.insert(j,int(tile))

        # insert row in grid
        grid.insert(i, row)


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


def swap(tile1, tile2, grid):


    return s_grid


def main():
    scramble()
    get_current_state()
    node = Node(grid, None, None, None)
    for neighbour in find_neighbours(node):
        print(neighbour)

if __name__ == "__main__":
    main()
