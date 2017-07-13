# Game logic and design by arnisritins. https://github.com/arnisritins/15-Puzzle.

import time
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
    def __init__(self, config, parent, f, g, h):
         self.config = config
         self.parent = parent
         self.f = f
         self.g = g
         self.h = h


# find heuristics
def heuristic(node):
    dist = []
    for tile in node.config:
        for solved_tile in solved_grid:
            if solved_tile.num == tile.num:
                dist.append(str(manhattan_distance(tile, solved_tile)) + '-' + str(tile.num))

    return dist

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
            grid.append(Tile(i, j, str(tile)))


# find the taxicab distance between two points
def manhattan_distance(start, end):
    return abs(start.x - end.x) + abs(start.y - end.y)


# submit a number
def submit(tile):
    input_box = driver.find_element_by_id("number")
    input_box.send_keys(str(tile))
    submit_btn = driver.find_element_by_id("submit")
    submit_btn.click()


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


if __name__ == "__main__":
    main()
