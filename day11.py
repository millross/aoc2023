from common import aoc_23_common as aoc_23

class CompensatedImage:
    def __init__(self, image):
        self.original_image = image


    def col_has_no_galaxies(self, image, col):
        return all(map(lambda row: row[col] == "." , image))

    def add_col_at(self, current_image_state, col):
        return list(map(lambda r: r[:col] + "." + r[col:], current_image_state))
    
    def double_empty_columns(self, starting_image):
        l = len(starting_image[0]) - 1
        image = starting_image
        for idx in range(l, -1, -1):
            print(idx)
            # print(self.col_has_no_galaxies(starting_image, idx))
            if (self.col_has_no_galaxies(starting_image, idx)):
                image = self.add_col_at(image, idx)
                print("WIP 1", list(image))
            else:
                print("WIP 2", list(image))
            
        return list(image)



# test_image = aoc_23.load_file("day11_test_input")
test_col_false = ["...", ".#.", "..."]
compensated_image = CompensatedImage(test_col_false)
assert(compensated_image.col_has_no_galaxies(test_col_false, 0) == True)
assert(compensated_image.col_has_no_galaxies(test_col_false, 1) == False)
print(compensated_image.col_has_no_galaxies(test_col_false, 1))
print(list(compensated_image.double_empty_columns(test_col_false)))
