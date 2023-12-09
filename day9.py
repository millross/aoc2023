from common import aoc_23_common as aoc_23

all_zeroes = [0, 0, 0, 0, 0]
all_threes = [3, 3, 3, 3, 3]


def next(sequence):
    if (all(x ==  0 for x in sequence)):
        return 0
    diffs = []
    for idx in range(1, len(sequence)):
        diffs.append(sequence[idx] - sequence[idx -1])
    return sequence[-1] + next(diffs)

def previous(sequence):
    if (all(x ==  0 for x in sequence)):
        return 0
    diffs = []
    for idx in range(1, len(sequence)):
        diffs.append(sequence[idx] - sequence[idx -1])
    return sequence[0] - previous(diffs)


def test_next(sequence, expected):
    actual = next(sequence)
    if actual == expected:
        print("Correct next result for " + str(sequence))
    else:
        raise(Exception("Next in sequence for " + str(sequence) + " Actual: " + str(actual) + ", Expected: " + str(expected)))        

def test_previous(sequence, expected):
    actual = previous(sequence)
    if actual == expected:
        print("Correct previous result for " + str(sequence))
    else:
        raise(Exception("Previous in sequence for " + str(sequence) + " Actual: " + str(actual) + ", Expected: " + str(expected)))        

def load_sequences_from_file(filename):
    return list(map(lambda s_s: list(map(int, s_s)), map(lambda l: l.split(" "), aoc_23.load_file(filename))))

test_next(all_zeroes, 0)
test_next(all_threes, 3)

test_previous(all_zeroes, 0)
test_previous(all_threes, 3)
test_previous([0, 3, 6, 9], -3)

test_sequences = load_sequences_from_file("day9_test_input")

tests_nexts = list(map(next, test_sequences))
print("Test sum part 1 is ", sum(tests_nexts))

part_1_sequences = load_sequences_from_file("day9_input")
part_1_nexts = list(map(next, part_1_sequences))
print("Part 1 result = ", sum(part_1_nexts))

test_previouses = list(map(previous, test_sequences))
print(test_previouses)
print("Test sum part 2 is ", sum(test_previouses))

part_2_previouses = list(map(previous, part_1_sequences))
print("Part 2 result is ", sum(part_2_previouses))