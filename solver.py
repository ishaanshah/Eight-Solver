# Game logic and design by arnisritins. https://github.com/arnisritins/15-Puzzle.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Initialize webdriver to communicate with webpage
driver = webdriver.Chrome(r"C:\Users\ishaa\chromedriver.exe")
driver.get("file:///F:/Projects/PycharmProjects/fifteen_solver/15-Puzzle/index.html")


# structure to store coordinates
class Coordinate:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.tile = tile


# grid for puzzle
grid = []


def get_current_state():
    for i in range(0, 4):
        for j in range(0, 4):
            print(driver.find_element_by_id("cell-{}-{}".format(i, j)).text)


def main():
    i = 0
    for x in range(4):
        for y in range(4):
            grid.insert(i, Coordinate(x, y, i))
            i = i + 1

    get_current_state()
    driver.close()


if __name__ == "__main__":
    main()
