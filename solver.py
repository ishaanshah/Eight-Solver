# Game logic and design by arnisritins. https://github.com/arnisritins/15-Puzzle.

import copy
import time
from collections import deque
from operator import attrgetter
from selenium import webdriver

# Initialize web driver to communicate with web page
driver = webdriver.Chrome(r"C:\Users\ishaa\chromedriver.exe")
driver.get("file:///E:/PyCharm%20Projects/8-Puzzle/index.html")

# grid for puzzle
grid = [[i for i in range(3)] for j in range(3)]

# solved state of puzzle
solved_grid = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


# structure for nodes
class Node:
    def __init__(self, config, parent, f, g, h):
        self.config = config
        self.parent = parent
        self.f = f
        self.g = g
        self.h = h


class Continue(Exception):
    pass


def a_star():
    get_current_state()
    start = Node(grid, None, heuristic(grid), 0, heuristic(grid))
    end = Node(solved_grid, None, None, None, 0)

    closed_set = deque()
    open_set = deque()
    open_set.appendleft(start)

    while len(open_set) != 0:
        current = min(open_set, key=attrgetter("f"))
        open_set.remove(current)
        for neighbour in find_neighbours(current):
            if same_state(neighbour.config, end.config):
                return True

            try:
                for node in closed_set:
                    if same_state(node.config, neighbour.config):
                        raise Continue

            except Continue:
                continue

            else:
                neighbour.g = current.g + 1
                neighbour.h = heuristic(neighbour.config)
                neighbour.f = neighbour.g + neighbour.h
                open_set.appendleft(neighbour)
        closed_set.appendleft(current)
    return False


# finds the neighbours of current config
def find_neighbours(node):
    j = [j for j in node.config if 0 in j][0]
    zero_x = node.config.index(j)
    zero_y = j.index(0)
    neighbours = []

    if zero_x + 1 <= 2:
        neighbour_1 = copy.deepcopy(node.config)
        neighbour_1[zero_x + 1][zero_y], neighbour_1[zero_x][zero_y] = \
            neighbour_1[zero_x][zero_y], neighbour_1[zero_x + 1][zero_y]
        neighbours.append(Node(neighbour_1, node, None, None, None))

    if zero_x - 1 >= 0:
        neighbour_2 = copy.deepcopy(node.config)
        neighbour_2[zero_x - 1][zero_y],  neighbour_2[zero_x][zero_y] =  \
            neighbour_2[zero_x][zero_y],  neighbour_2[zero_x - 1][zero_y]
        neighbours.append(Node(neighbour_2, node, None, None, None))

    if zero_y + 1 <= 2:
        neighbour_3 = copy.deepcopy(node.config)
        neighbour_3[zero_x][zero_y + 1], neighbour_3[zero_x][zero_y] = \
            neighbour_3[zero_x][zero_y], neighbour_3[zero_x][zero_y + 1]
        neighbours.append(Node(neighbour_3, node, None, None, None))

    if zero_y - 1 >= 0:
        neighbour_4 = copy.deepcopy(node.config)
        neighbour_4[zero_x][zero_y - 1], neighbour_4[zero_x][zero_y] = \
            neighbour_4[zero_x][zero_y], neighbour_4[zero_x][zero_y - 1]
        neighbours.append(Node(neighbour_4, node, None, None, None))

    return neighbours


# find heuristics
def heuristic(config):
    dist = 0
    for i in range(1, 9):
        j = [j for j in solved_grid if i in j][0]
        s_x = solved_grid.index(j)
        s_y = j.index(i)
        k = [k for k in config if i in k][0]
        n_x = config.index(k)
        n_y = k.index(i)
        dist += (abs(s_x - n_x) + abs(s_y - n_y))

    return dist


# get current state of board
def get_current_state():
    # empty the list
    grid[:] = []
    for i in range(3):
        row = []
        for j in range(3):
            tile = driver.find_element_by_id("cell-{}-{}".format(i, j)).text
            # check for black tile
            if tile == '':
                tile = "0"
            row.insert(j, int(tile))

        # insert row in grid
        grid.insert(i, row)


def scramble():
    driver.find_element_by_id("scramble").click()  # wait for animation
    time.sleep(0.6)  # wait for animation


def same_state(grid1, grid2):
    for i in range(3):
        for j in range(3):
            if grid1[i][j] != grid2[i][j]:
                return False

    return True


# submit a
def submit(tile):
    input_box = driver.find_element_by_id("number")
    input_box.send_keys(str(tile))
    submit_btn = driver.find_element_by_id("submit")
    submit_btn.click()
    time.sleep(0.3)  # wait for animation


def main():
    scramble()
    print(a_star())


if __name__ == "__main__":
    main()
