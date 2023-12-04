# Create sparse representations of the numbers, symbols and their positions in the schematic
# and use positions to determine which numbers are next to a symbol so we can filter

from common import aoc_23_common as aoc_23
from common.position import Position
import re

NUMBER_REGEX = '(\\d+)'
SYMBOL_REGEX = '[^\\d\\.]'

class NumberAndLocation:
    def __init__(self, number, row, col):
        self.number = number
        self.position = Position(col, row)

    def __str__(self):
        return str(self.number) + " at " + str(self.position)
    
    def __repr__(self):
        return str(self)


class Schematic:

    def __init__(self, lines):
        self.test = None
        matched_lines = map(lambda l: ParsedLine(l), lines)
        numbers = []
        symbols = []
        for row, matched_line in enumerate(matched_lines):
            numbers_for_row = map(lambda m: NumberAndLocation(int(m.group()), row, m.span()[0]), matched_line.number_matches)
            numbers.extend(numbers_for_row)

        self.numbers = numbers
        self.symbols = symbols

    def __str__(self):
        return "================= SCHEMATIC ===================\nNumbers: " + str(self.numbers) + "\nSymbols: " + str(self.symbols)
    
    def __repr__(self):
        return str(self)



class ParsedLine:
    def __init__(self, line):
        self.number_matches = re.finditer(NUMBER_REGEX, line)
        self.symbol_matches = re.finditer(SYMBOL_REGEX, line)

    def of_interest(self):
        return self.number_matches or self.symbol_matches



test_input_lines = aoc_23.load_file("day3_test_input")
schematic = Schematic(test_input_lines)
print(str(schematic))

# test_line = "467..114.."
# test_line = "...."
# test_line = "..$..*"

# number_match = re.finditer(SYMBOL_REGEX, test_line)
# print(list(number_match))
# print(number_match.groups())
# print(number_match.span())