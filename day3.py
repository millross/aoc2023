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


class ParsedLine:
    def __init__(self, line):
        self.number_matches = re.finditer(NUMBER_REGEX, line)
        self.symbol_matches = re.finditer(SYMBOL_REGEX, line)
        # print (list(self.symbol_matches))

class Schematic:

    def __init__(self, lines):
        matched_lines = map(lambda l: ParsedLine(l), lines)
        numbers = []
        symbols = {}

        for row, matched_line in enumerate(matched_lines):
            numbers_for_row = map(lambda m: NumberAtLocation(int(m.group()), row, m.span()[0]), matched_line.number_matches)
            symbols_for_row = map(lambda m: SymbolAtLocation(m.group(), row, m.span()[0]), matched_line.symbol_matches)

            if numbers_for_row:
                numbers.extend(numbers_for_row)

            if symbols_for_row:
                symbol_dict = {}
                for symbol in symbols_for_row:
                    symbol_dict[symbol.position.x] = symbol
            
            symbols[row] = symbol_dict

        self.numbers = numbers
        self.symbols = symbols

    def __str__(self):
        return "================= SCHEMATIC ===================\nNumbers: " + str(self.numbers) + "\nSymbols: " + str(self.symbols)
    
    def __repr__(self):
        return str(self)

    def __contains_any_symbol(self, row, start, end):
        symbols_for_row = self.symbols.get(row, {})
        result =  next(filter(lambda x: x, map(lambda col: col in symbols_for_row, range(start, end))), False) 
        return result
    

    def __number_is_adjacent_to_symbol(self, number_at_position):
        rows = range(number_at_position.position.y - 1, number_at_position.position.y + 2)
        start = number_at_position.position.x - 1
        end = number_at_position.position.x + len(str(number_at_position.number)) + 1
        if (number_at_position.number == 934):
            print("Looking at 934, at ", number_at_position.position.x, number_at_position.position.y)
            print("Start", start)
            print("End", end)
        return next(filter(lambda b: b, map(lambda row: self.__contains_any_symbol(row, start, end), rows)), False)
    
    def part_numbers(self):
        return map(lambda n: n.number, filter(self.__number_is_adjacent_to_symbol, self.numbers))
    

class GearRatioAnalyzer:
    
    def __init__(self, schematic):
        self.schematic = schematic
        self.gear_candidates = {}

    def __all_symbols_in_range(self, row, start, end):
        symbols_for_row = self.schematic.symbols.get(row, {})
        result =  filter(lambda x: x != None, map(lambda col: symbols_for_row.get(col, None), range(start, end)))
        return result
    
    def __matching_symbols_in_range(self, row, start, end, symbol_match):
        return filter (lambda s: s.symbol == symbol_match, self.__all_symbols_in_range(row, start, end))

    def __all_adjacent_symbols_for_number(self, number_at_position, symbol_match):
        rows = range(number_at_position.position.y - 1, number_at_position.position.y + 2)
        start = number_at_position.position.x - 1
        end = number_at_position.position.x + len(str(number_at_position.number)) + 1
        matching_adjacent_symbols = []
        for row in rows:
            new_gear_candidates_in_row = self.__matching_symbols_in_range(row, start, end, symbol_match)
            matching_adjacent_symbols.extend(new_gear_candidates_in_row)
        return matching_adjacent_symbols
    
    def __get_candidate_key(self, x, y):
        return str(x) + "-" + str(y)
    
    def identify_all_adjacent_numbers_for_potential_gears(self):
        gear_candidates = {}
        for number in self.schematic.numbers:
            adjacent_gear_candidates = self.__all_adjacent_symbols_for_number(number, "*")
            for candidate in adjacent_gear_candidates:
                candidate_key = self.__get_candidate_key(candidate.position.x, candidate.position.y)
                adjacent_numbers_for_candidate = gear_candidates.get(candidate_key, [])
                adjacent_numbers_for_candidate.append(number.number)
                gear_candidates[candidate_key] = adjacent_numbers_for_candidate
        return gear_candidates
    
    def gears(self):
        return filter(lambda a: len(a) == 2, iter(self.identify_all_adjacent_numbers_for_potential_gears().values()))
    
def gear_ratio(gear):
    return gear[0] * gear[1]

test_input_lines = aoc_23.load_file("day3_test_input")
test_schematic = Schematic(test_input_lines)
test_sum = sum(test_schematic.part_numbers())
print("Test sum ", test_sum)

part_one_input_lines = aoc_23.load_file("day_3_input")

part_one_input_lines_first_10 = part_one_input_lines[0:10]
part_one_first_10_schematic = Schematic(part_one_input_lines_first_10)
print(str(part_one_first_10_schematic))
print("PART NUMBERS")
print(str(list(part_one_first_10_schematic.part_numbers())))

part_one_schematic = Schematic(part_one_input_lines)
part_one_sum = sum(part_one_schematic.part_numbers())
print("Part one sum ", part_one_sum)                                    

part_two_test_analyzer = GearRatioAnalyzer(test_schematic)
print(list(map(gear_ratio, part_two_test_analyzer.gears())))
print(sum(map(gear_ratio, part_two_test_analyzer.gears())))

part_two_analyzer = GearRatioAnalyzer(part_one_schematic)
print(sum(map(gear_ratio, part_two_analyzer.gears())))
