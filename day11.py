from common import aoc_23_common as aoc_23
from common.position import Position
import re

GALAXY = "#"

def col_has_no_galaxies(image, col):
    return all(map(lambda row: row[col] == "." , image))

def row_has_no_galaxies(image, row):
    return "#" not in image[row]
    
class CompensatedImage:

    def __init__(self, image):
        self.original_image = image

    def add_col_at(self, current_image_state, col):
        return list(map(lambda r: r[:col] + "." + r[col:], current_image_state))
    
    def double_empty_columns(self, starting_image):
        l = len(starting_image[0]) - 1
        image = starting_image
        for idx in range(l, -1, -1):
            # print(self.col_has_no_galaxies(starting_image, idx))
            if (col_has_no_galaxies(starting_image, idx)):
                image = self.add_col_at(image, idx)            
        return list(image)
    
    def add_empty_row_at(self, current_image_state, row):
        row_length = len(current_image_state[0])
        current_image_state = current_image_state[:row] + [(row_length * ".")] + current_image_state[row:]
        return current_image_state
    
    def double_empty_rows(self, starting_image):
        l = len(starting_image) - 1
        image = starting_image
        for idx in range(l, -1, -1):
            if (row_has_no_galaxies(starting_image, idx)):
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

# Part 2 needs a sparse approach to this, which I considered earlier, bad mistake not to do it at the time.
# Maybe map original x/y possible values to updated and then apply this delta to list of galaxies found from
# original (uncompensated image) before determining distances

class ExpansionEffect:
    def __init__(self, image, impact):
        
        self._column_widths = list(map(lambda idx: self.__column_width(image, idx, impact) , range(0, len(image[0]))))
        self._row_heights = list(map(lambda idx: self.__row_height(image, idx, impact), range(0, len(image))))

    def __column_width(self, image, col_index, expansion_impact):
        if (col_has_no_galaxies(image, col_index)):
            return expansion_impact
        else:
            return 1
        
    def __row_height(self, image, row_index, expansion_impact):
        if (row_has_no_galaxies(image, row_index)):
            return expansion_impact
        else:
            return 1
        
    @property
    def column_widths(self):
        test = list(self._column_widths)
        return test
    
    @property
    def row_heights(self):
        return list(self._row_heights)
        
class ExpansionSimulator:

    def __init__(self, galaxies, expansion_effect):
        self._galaxies = galaxies
        self._expansion_impact = expansion_effect

    def __adjust_position(self, galaxy_position):
        x_range = range(0, galaxy_position.x)
        y_range = range(0, galaxy_position.y)
        col_widths = map(lambda col_idx: self._expansion_impact.column_widths[col_idx], x_range)
        row_heights = map(lambda row_idx: self._expansion_impact.row_heights[row_idx], y_range)
        return Position(sum(col_widths), sum(row_heights))

    def adjusted_galaxy_positions(self):
        return list(map(lambda galaxy: self.__adjust_position(galaxy), self._galaxies))
    
test_part_1_expansion_effect = ExpansionEffect(test_image, 2)
test_part_1_galaxy_finder = GalaxyFinder(test_image)
test_expansion_simulator = ExpansionSimulator(test_part_1_galaxy_finder.find_galaxies(), test_part_1_expansion_effect)
test_part_1_adjusted_positions = test_expansion_simulator.adjusted_galaxy_positions()
test_part_1_separations = GalaxySeparationFinder(test_part_1_adjusted_positions).all_separations()
print(sum(test_part_1_separations))

test_part_2_expansion_effect = ExpansionEffect(test_image, 10)
test_part_2_expansion_simulator = ExpansionSimulator(test_part_1_galaxy_finder.find_galaxies(), test_part_2_expansion_effect)
test_part_2_adjusted_positions = test_part_2_expansion_simulator.adjusted_galaxy_positions()
test_part_2_separations = GalaxySeparationFinder(test_part_2_adjusted_positions).all_separations()
print(sum(test_part_2_separations))

def determine_adjusted_separations(image, expansion_impact):
    galaxy_finder = GalaxyFinder(image)
    expansion_effect = ExpansionEffect(image, expansion_impact)
    expansion_simulator = ExpansionSimulator(galaxy_finder.find_galaxies(), expansion_effect)
    adjusted_positions = expansion_simulator.adjusted_galaxy_positions()
    separations = GalaxySeparationFinder(adjusted_positions).all_separations()
    return sum(separations)

print("Test, 2", determine_adjusted_separations(test_image, 2))
print("Test, 10", determine_adjusted_separations(test_image, 10))
print("Test, 100", determine_adjusted_separations(test_image, 100))
print("Actual, 2", determine_adjusted_separations(part_1_image, 2))
print("Actual, 1000000", determine_adjusted_separations(part_1_image, 1000000))

