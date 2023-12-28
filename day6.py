from common import aoc_23_common as common
import re
import functools
import operator

NUMBERS_PATTERN = "\d+"

class Race:
    def __init__(self, time, record_distance):
        self.time = time
        self.record_distance = record_distance

    def __str__(self):
        return ("Race time " + str(self.time) + " record distance " + str(self.record_distance))    
    
    def __repr__(self):
        return str(self)

class InputDataParser:

    def __init__(self, filename):
        lines = common.load_file(filename)
        times = common.extract_numbers_from_string(lines[0])
        distances = list(common.extract_numbers_from_string(lines[1]))
        races = []
        for index, time in enumerate(times):
            record_distance = distances[index]
            races.append(Race(time, record_distance))
        self._races = races

    def races(self):
        return self._races
    
class ErrorMarginCalculator:

    def __init__(self, race):
        self.race = race

    def distance(self, race_time, button_hold_time):
        return button_hold_time * (race_time - button_hold_time)

    def all_race_distances(self):
        button_hold_times = range(0, self.race.time)
        return list(map(lambda t: self.distance(self.race.time, t), button_hold_times))
    
    def winning_distance_count(self):
        return len(list(filter(lambda d: d > self.race.record_distance, self.all_race_distances())))

class Part1Analysis:
    def __init__(self, parser):
        self.races = parser.races()

    def winning_distance_counts(self):
        return list(map(lambda r: ErrorMarginCalculator(r).winning_distance_count(), self.races))
    
    def winning_permutations_count(self):
        return functools.reduce(operator.mul, self.winning_distance_counts(), 1)
    
test_races_analysis = Part1Analysis(InputDataParser("day6_test_input"))
print(test_races_analysis.winning_permutations_count())

part_1_analysis = Part1Analysis(InputDataParser("day6_input"))
print("Part 1", part_1_analysis.winning_permutations_count())
# Part 1 brute force = 275724 for reference

# For part 2 analysis I think we can find each end of the winning combinations and use that to determine the number of winning for a race
# We will need a new parser and a fix to determine via beginning and end of winning combinations via a binary tree

class SingleRaceInputParser:
    def __init__(self, filename):

        lines = common.load_file(filename)
        time_components = common.extract_numbers_from_string(lines[0])
        distance_components = list(common.extract_numbers_from_string(lines[1]))

        time = int("".join(map(str, time_components)))
        distance = int("".join(map(str, distance_components)))

        self._races = [Race(time, distance)]

    def races(self):
        return self._races


part_2_test_analysis = Part1Analysis(SingleRaceInputParser("day6_test_input"))
print("Part 2 test result: ", part_2_test_analysis.winning_permutations_count())

part_2_analysis = Part1Analysis(SingleRaceInputParser("day6_input"))
print("Part 2 analysis", part_2_analysis.winning_permutations_count())

# Surprised the above worked reasonably quickly without having to make an efficient search for the boundaries of winning button hold times, but I'll take it