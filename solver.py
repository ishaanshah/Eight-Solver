# This is a program that solves the 8 puzzle using the a* algorithm
# Game logic and design by arnisritins. https://github.com/arnisritins/15-Puzzle.

import copy
import time
from collections import deque
from operator import attrgetter
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException

# Initialize web driver to communicate with web page
driver = webdriver.Chrome(r"C:\Users\ishaa\chromedriver.exe")
driver.get("file:///E:/PyCharm%20Projects/8-Puzzle/index.html")

# grid for puzzle
grid = [[i for i in range(3)] for j in range(3)]

# solved state of puzzle
solved_grid = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


# structure for nodes
class Node:
    def __init__(self, config, parent, f, g, h, num):
        self.config = config
        self.parent = parent
        self.f = f
        self.g = g
        self.h = h
        self.num = num


class Continue(Exception):
    pass


# check if alert is present
def alert_present():
    try:
        driver.switch_to.alert.dismiss()
    except NoAlertPresentException:
        return False
    return True


# algorithm for solving the puzzle
def a_star():
    get_current_state()
    start = Node(grid, None, heuristic(grid), 0, heuristic(grid), None)
    end = Node(solved_grid, None, None, None, 0, None)

    closed_set = deque()
    open_set = deque()
    open_set.appendleft(start)

    while len(open_set) != 0:
        current = min(open_set, key=attrgetter("f"))
        open_set.remove(current)
        for neighbour in find_neighbours(current):
            if same_state(neighbour.config, end.config):
                reconstruct_moves(current)
                return True

            # check if node is already evaluated
            try:
                for node in closed_set:
                    if same_state(node.config, neighbour.config):
                        raise Continue

            except Continue:
                continue

            # if not continue and save the node
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
        neighbours.append(Node(neighbour_1, node, None, None, None, neighbour_1[zero_x][zero_y]))

    if zero_x - 1 >= 0:
        neighbour_2 = copy.deepcopy(node.config)
        neighbour_2[zero_x - 1][zero_y],  neighbour_2[zero_x][zero_y] =  \
            neighbour_2[zero_x][zero_y],  neighbour_2[zero_x - 1][zero_y]
        neighbours.append(Node(neighbour_2, node, None, None, None, neighbour_2[zero_x][zero_y]))

    if zero_y + 1 <= 2:
        neighbour_3 = copy.deepcopy(node.config)
        neighbour_3[zero_x][zero_y + 1], neighbour_3[zero_x][zero_y] = \
            neighbour_3[zero_x][zero_y], neighbour_3[zero_x][zero_y + 1]
        neighbours.append(Node(neighbour_3, node, None, None, None, neighbour_3[zero_x][zero_y]))

    if zero_y - 1 >= 0:
        neighbour_4 = copy.deepcopy(node.config)
        neighbour_4[zero_x][zero_y - 1], neighbour_4[zero_x][zero_y] = \
            neighbour_4[zero_x][zero_y], neighbour_4[zero_x][zero_y - 1]
        neighbours.append(Node(neighbour_4, node, None, None, None, neighbour_4[zero_x][zero_y]))

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


# scramble the puzzle
def scramble():
    driver.find_element_by_id("scramble").click()  # wait for animation
    time.sleep(0.6)  # wait for animation


# check if the given grids have the same configuration
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
    time.sleep(0.5)  # wait for animation


def reconstruct_moves(node):
    moves = []
    # traverse upe the decision tree
    while node.num is not None:
        moves.append(node.num)
        node = node.parent

    moves.reverse()
    for move in moves:
        submit(move)

    # make the last move and close the alert
    submit(6)
    if alert_present():
        pass
    else:
        submit(8)
        driver.switch_to.alert.dismiss()


def main():
    scramble()
    a_star()


if __name__ == "__main__":
    main()
