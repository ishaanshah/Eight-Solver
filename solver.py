# Game logic and design by arnisritins. https://github.com/arnisritins/15-Puzzle.

from selenium import webdriver

# Initialize webdriver to communicate with web page
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
            # get the tile from web page
            tile = driver.find_element_by_id("cell-{}-{}".format(i, j)).text

            # check for empty tile
            if tile == '':
                # set empty tile as 0
                num_tile = 0
            else:
                # convert to integer
                num_tile = int(tile)

            # insert coordinates of tile in grid
            grid.insert(num_tile, Coordinate(i, j, str(num_tile)))


def submit(tile):
    input_box = driver.find_element_by_id("number")
    input_box.send_keys(str(tile))
    submit_btn = driver.find_element_by_id("submit")
    submit_btn.click()


def main():
    get_current_state()
    driver.close()

if __name__ == "__main__":
    main()
