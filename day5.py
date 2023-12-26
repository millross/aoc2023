from common import aoc_23_common as aoc23
import re

MAPPING_TYPES_PATTERN="^([a-z]+)-to-([a-z]+) map"

class CategoryValueRange:
    
    def __init__(self, category, start, length):
        self.category = category
        self.start = start
        self.length = length

    def __str__(self):
        return self.category + ": " + str(self.start) + " for " + str(self.length)
    
    def __repr__(self):
        return str(self)

class CategoryValue:

    def __init__(self, category, value):
        self.category = category
        self.value = value

    def __str__(self):
        return ": ".join([self.category, str(self.value)])
    
    def __repr__(self):
        return str(self)

class MappingRange:

    def __init__(self, destination_range_start, source_range_start, range_length):
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

    def __str__(self):
        return "->".join([str(self.source_range_start), str(self.destination_range_start)]) + ", with length " + str(self.range_length)
    
    def __repr__(self):
        return str(self)

    def is_mapped(self, value):
        return value >= self.source_range_start and value < (self.source_range_start + self.range_length)
    
    def map_value(self, value):
        if not self.is_mapped(value):
            return None
        return value - self.source_range_start + self.destination_range_start

class MappingRangeParser:
    
    def __init__(self, mapping_range_line):
        numbers = list(map(int, mapping_range_line.split()))
        self.destination_range_start = numbers[0]
        self.source_range_start = numbers[1]
        self.range_length = numbers[2]

    def mapping_range(self):
        return MappingRange(self.destination_range_start, self.source_range_start, self.range_length)

class MappingGroup:
    def __init__(self, mapping_from, mapping_to, mapping_ranges):
        self.mapping_from = mapping_from
        self.mapping_to = mapping_to
        self.ranges = mapping_ranges

    def __str__(self):
        return self.mapping_from + "-to-" + self.mapping_to + " map" + "\nRanges: " + str(self.ranges)
    
    def __repr__(self):
        return str(self)
    
    def map(self, value):
        if (value.category != self.mapping_from):
            raise Exception("Attempting to map " + value.category + " with mapper for " + self.mapping_from)
        
        input = value.value
        ranges = list(filter(lambda r: r.is_mapped(input), self.ranges))
        if len(ranges) == 0:
            output = input
        else:
            output = ranges[0].map_value(input)
        return CategoryValue(self.mapping_to, output)
    
    def map_range(self, value_range):

        if value_range == None:
            return []

        # A range can break into multiple ranges so map_range should return a list of ranges
        if (value_range.category != self.mapping_from):
            raise Exception("Attempting to map " + value_range.category + " with mapper for " + self.mapping_from)
        
        mappers_for_range_start = list(filter(lambda r: r.is_mapped(value_range.start), self.ranges))
        print("Value range ", value_range)
        print("Mappers for range start\n", mappers_for_range_start)
        possible_next_mappers_in_range = list(filter(lambda r: r.source_range_start > value_range.start and r.source_range_start < (value_range.start + value_range.length), self.ranges))
        print("Next mappers in range ", possible_next_mappers_in_range)
        remainder = None
        if len(possible_next_mappers_in_range) > 0:
            # We do have a mapper, we will need to see if it happens 
            earliest_next_mapper_range_start = min(map(lambda r: r.source_range_start, possible_next_mappers_in_range))
            # Is this after the first mapper finishes
            if len(mappers_for_range_start) == 0:
                # We don't have a gap between the start mapper and the earliest next mapper so we can infer our range and remainder
                range_to_map_length = earliest_next_mapper_range_start - value_range.start
                range_to_map = CategoryValueRange(value_range.category, value_range.start, range_to_map_length)
                remainder = CategoryValueRange(value_range.category, earliest_next_mapper_range_start, value_range.length - range_to_map_length)
                if (remainder.length == None):
                    remainder = None
            else:
                # We may have a gap between the start mapper and the earliest next mapper so we need to do a little more checking
                # We have a mapper for the start of the range so does our range extend beyond the range covered by the mapper?
                range_end = value_range.start + value_range.length - 1
                mapper_for_range_start = mappers_for_range_start[0]
                mapper_range_end = mapper_for_range_start.source_range_start + mapper_for_range_start.range_length - 1
                if range_end <= mapper_range_end:
                    # This range is entirely contained within the mapper and there is no remainder
                    remainder = None
                    range_to_map = value_range
                else:
                    # We will have a remainder and need to separate out the remainder to be mapped separately
                    new_range_length = mapper_range_end + 1 - value_range.start
                    range_to_map = CategoryValueRange(value_range.category, value_range.start, new_range_length)
                    remainder = CategoryValueRange(value_range.category, mapper_range_end + 1, value_range.length - new_range_length)
        else:
            # No other mapping applies in range so we can map the whole range directly
            remainder = None
            range_to_map = value_range

        print("Remainder ", remainder)
        print("Range to map ", value_range)
        mapped_range_start = self.map(CategoryValue(value_range.category, value_range.start)).value
        mapped_first_value = CategoryValueRange(self.mapping_to, mapped_range_start, range_to_map.length)
        print("Mapped first value", mapped_first_value)
        result = [mapped_first_value]
        result.extend(self.map_range(remainder))
        print("About to return ", result)
        return result      

class MappingGroupParser:
    def __init__(self, lines):
        mapping_types = lines[0]
        types_match = re.match(MAPPING_TYPES_PATTERN, mapping_types)
        self.mapping_from = types_match[1]
        self.mapping_to = types_match[2]
        self.ranges = list(map(lambda l: MappingRangeParser(l).mapping_range(), lines[1:]))

    def __str__(self):
        return str(MappingGroup(self))
    
    def __repr__(self):
        return str(self)
    
    def mapping_group(self):
        return MappingGroup(self.mapping_from, self.mapping_to, self.ranges)

class ProblemFileParser:
    def __init__(self, file_name):
        raw_data = aoc23.load_file(file_name)
        seeds_line = raw_data[0][7:]
        self.seeds = list(map(int, seeds_line.split()))
        # Now we need to parse the mappings and create dictionary of maps
        mappings_groups_lines = raw_data[2:]
        self.mappings_groups = list(map(lambda l: MappingGroupParser(l).mapping_group(), aoc23.group_by_delimiter(mappings_groups_lines, "")))
        

class ProblemData:
    def __init__(self, file_name):
        raw_data = aoc23.load_file(file_name)

class SeedToLocationMapper:
    def __init__(self, filename):
        self.parser = ProblemFileParser(filename)

    def map_to_end(self):
        seeds = list(map(lambda s: CategoryValue("seed", s), self.parser.seeds))
        accumulator = seeds
        for mapper in self.parser.mappings_groups:
            accumulator = list(map(lambda cv: mapper.map(cv), accumulator))
        return accumulator
    
    def min_location(self):
        locations = self.map_to_end()
        return min(map(lambda v: v.value, locations))



class SeedRangeToLocationRangeMapper:
    def __init__(self, filename):
        self.parser = ProblemFileParser(filename)

    def extract_seed_ranges(self):
        # Each pair of numbers in the parser seed range represents a statrt and length
        seed_range_defs = aoc23.group_with_fixed_size(self.parser.seeds, 2)

        ranges = map(lambda r: CategoryValueRange("seed", r[0], r[1]), seed_range_defs)
        return list(ranges)

    def map_to_end(self, seed_ranges):
        accumulator = seed_ranges
        for mapper in self.parser.mappings_groups:
            mapping_accumulator = map(lambda cvr: mapper.map_range(cvr), accumulator)
            accumulator = []
            for mapped_range in mapping_accumulator:
                accumulator.extend(mapped_range)
            
        return accumulator
    
    def min_location(self, seed_range):
        locations = self.map_to_end(seed_range)
        result =  min(map(lambda v: v.value, locations))
        print("min location achieved for seed_range")
        return result
    
    def global_min_location(self):
        seed_ranges = self.extract_seed_ranges()
        return min(map(lambda r: self.min_location(r), seed_ranges))


test_mapper = SeedToLocationMapper("day5_test_input")
min_test_location = test_mapper.min_location()
print("Min test location ", min_test_location)

part_1_mapper = SeedToLocationMapper("day5_input")
print("Part 1 min location ", part_1_mapper.min_location())

part_2_test_mapper = SeedRangeToLocationRangeMapper("day5_test_input")
final_test_ranges = part_2_test_mapper.map_to_end(part_2_test_mapper.extract_seed_ranges())
print(final_test_ranges)
# min_part_2_test_location = part_2_test_mapper.global_min_location()
# print("Min test part 2 location ", min_part_2_test_location)

part_2_mapper = SeedRangeToLocationRangeMapper("day5_input")
final_ranges = part_2_mapper.map_to_end(part_2_mapper.extract_seed_ranges())
print(final_ranges)
min_location = min(map(lambda r: r.start, final_ranges))
print("Min location ", min_location)
# part_2_mapper = SeedRangeToLocationMapper("day5_input")
# min_part_2_location = part_2_mapper.global_min_location()
# print("Min part 2 location", min_part_2_location)
# test_range_1 = CategoryValueRange("seed", 79, 14)
# test_range_2 = CategoryValueRange("seed", 55, 13)

# test_input_ranges = [test_range_1, test_range_2]
# test_mapping_range_1 = MappingRange(50, 98, 2)
# test_mapping_range_2 = MappingRange(52, 50, 48)
# test_mapping_group = MappingGroup("seed", "soil", [test_mapping_range_1, test_mapping_range_2])

# print("Testing range mapping")
# mapped_ranges = test_mapping_group.map_range(test_range_1)
# print(mapped_ranges)

