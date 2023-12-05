# Create sparse representations of the numbers, symbols and their positions in the schematic
# and use positions to determine which numbers are next to a symbol so we can filter

from common import aoc_23_common as aoc_23
from common.position import Position
import re

NUMBER_REGEX = '(\\d+)'
SYMBOL_REGEX = '[^\\d\\.]'

class NumberAtLocation:
    def __init__(self, number, row, col):
        self.number = number
        self.position = Position(col, row)

    def __str__(self):
        return str(self.number) + " at " + str(self.position)
    
    def __repr__(self):
        return str(self)

class SymbolAtLocation:
    def __init__(self, symbol, row, col):
        self.symbol = symbol
        self.position = Position(col, row)

    def __str__(self):
        return str(self.symbol) + " at " + str(self.position)
    
    def __repr__(self):
        return str(self)


class Schematic:

    def __init__(self, lines):
        self.test = None
        matched_lines = map(lambda l: ParsedLine(l), lines)
        numbers = []
        symbols = {}
        for row, matched_line in enumerate(matched_lines):
            numbers_for_row = map(lambda m: NumberAtLocation(int(m.group()), row, m.span()[0]), matched_line.number_matches)
            symbols_for_row = map(lambda m: SymbolAtLocation(m.group(), row, m.span()[0]), matched_line.symbol_matches)
            # for symbol in symbols_for_row:
            #     print(str(symbol))

            if numbers_for_row:
                numbers.extend(numbers_for_row)

            if symbols_for_row:
                symbol_dict = {}
                for symbol in symbols_for_row:
                    symbol_dict[symbol.position.x] = symbol.symbol

            symbols[row] = symbol_dict

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
        # print (list(self.symbol_matches))



test_input_lines = aoc_23.load_file("day3_test_input")
schematic = Schematic(test_input_lines)
print(str(schematic))

# Analyse the schematic now

# test_line = "467..114.."
# test_line = "...."
# test_line = "..$..*"

# number_match = re.finditer(SYMBOL_REGEX, test_line)
# print(list(number_match))
# print(number_match.groups())
# print(number_match.span())