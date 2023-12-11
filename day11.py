from common import aoc_23_common as aoc_23

class CompensatedImage:
    def __init__(self, image):
        self.original_image = image


    def col_has_no_galaxies(self, col):
        return all(map(lambda row: row[col] == "." , self.original_image))

    def add_col_at(self, current_image_state, col):
        return map(lambda r: r[:col] + "." + r[col:], current_image_state)
    
    def double_empty_columns(image):
        l = len(image[0])
        for idx in range(l, -1, -1):


# test_image = aoc_23.load_file("day11_test_input")
test_col_false = ["..", ".#", ".."]
compensated_image = CompensatedImage(test_col_false)
assert(compensated_image.col_has_no_galaxies(0) == True)
assert(compensated_image.col_has_no_galaxies(1) == False)
print(list(compensated_image.add_col_at(test_col_false, 1)))
