from common import aoc_23_common as aoc_23
from common.position import Position
import re

GALAXY = "#"

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
            # print(self.col_has_no_galaxies(starting_image, idx))
            if (self.col_has_no_galaxies(starting_image, idx)):
                image = self.add_col_at(image, idx)            
        return list(image)
    
    def row_has_no_galaxies(self, image, row):
        return "#" not in image[row]
    
    def add_empty_row_at(self, current_image_state, row):
        row_length = len(current_image_state[0])
        current_image_state = current_image_state[:row] + [(row_length * ".")] + current_image_state[row:]
        return current_image_state
    
    def double_empty_rows(self, starting_image):
        l = len(starting_image) - 1
        image = starting_image
        for idx in range(l, -1, -1):
            if (self.row_has_no_galaxies(starting_image, idx)):
                image = self.add_empty_row_at(image, idx)
        return image
    
    def compensated(self):
        image = self.original_image
        columns_added = self.double_empty_columns(image)
        rows_and_columns_added = self.double_empty_rows(columns_added)
        return rows_and_columns_added

class ImagePrinter:
    def __init__(self, image):
        self.image = image

    def print(self):
        for row in self.image:
            print(row) 

class GalaxyFinder:
    def __init__(self, image):
        self.image = image

    def find_galaxies(self):
        galaxies = []
        for idx, row in enumerate(self.image):
            galaxy_positions = map(lambda col: Position(col, idx), [m.start() for m in re.finditer(GALAXY, row)])
            galaxies.extend(galaxy_positions)
        return galaxies


class GalaxySeparationFinder:
    
    def __init__(self, galaxies):
        print("Creating finder for ", galaxies)
        self.galaxies = galaxies

    def shortest_separation(self, pos1, pos2):
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
    
    def all_separations(self):
        separations = []
        for idx, galaxy in enumerate(self.galaxies):
            # compile distances from this galaxy to remaining galaxies
            remaining_galaxies = self.galaxies[(idx + 1):]
            distances = map(lambda g: self.shortest_separation(galaxy, g), remaining_galaxies)
            separations.extend(distances)

        return separations

test_image = aoc_23.load_file("day11_test_input")

compensated_test_image = CompensatedImage(test_image).compensated()
ImagePrinter(compensated_test_image).print()
test_galaxy_finder = GalaxyFinder(compensated_test_image)
test_galaxies = test_galaxy_finder.find_galaxies()
test_galaxy_separation_finder = GalaxySeparationFinder(test_galaxies)
test_separations = test_galaxy_separation_finder.all_separations()
print(test_separations)
print(sum(test_separations))

print ("Actual day 11 part 1")
part_1_image = aoc_23.load_file("day11_input")
compensated_part_1_image = CompensatedImage(part_1_image).compensated()
part_1_galaxies = GalaxyFinder(compensated_part_1_image).find_galaxies()
part_1_separations = GalaxySeparationFinder(part_1_galaxies).all_separations()
print(sum(part_1_separations))
