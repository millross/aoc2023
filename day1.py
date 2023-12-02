# Calibration based on lines
from common import aoc_23_common as aoc_23

def line_to_digits(line):
    numbers = [c for c in line if c.isdecimal() ]
    return (numbers)

def get_calibration_value(digits):
    first = digits[0]
    last = digits[len(digits) - 1]
    return int(first + last)

def get_calibration_value_for_line(line):
    digits = line_to_digits(line)
    return int(get_calibration_value(digits))

def get_calibration_value_for_lines(lines):
    calibration_values = list(map(get_calibration_value_for_line, lines))
    return calibration_values

def sum_calibration_values_for_lines(lines):
    return sum(get_calibration_value_for_lines(lines))

test_result = sum_calibration_values_for_lines(["1abc2", "pqr3stu8vwx","a1b2c3d4e5f", "treb7uchet"])
print("test_result ", test_result)

step_1_input = aoc_23.load_file("day1_input")
step_1_result = sum_calibration_values_for_lines(step_1_input)
print(step_1_result)

# step 2 - some numbers spelled out
subs = ["one","two","three","four","five","six","seven","eight","nine"]
def convert_words_to_numbers(line,index):
    # We can stop when the index >= length(line) - length("one") since we have no numbers shorter than 3 characters
    # print("Line, index:", line, index)
    # print(line[index:index+3])
    # print(len(line) - 3)
    if (index > len(line) - 3):
        return line
    
    for (num_index, num_word) in enumerate(subs):
        # print("Checking ", line[index:(index + len(num_word))])
        if (line[index:(index + len(num_word))] == num_word):
            return convert_words_to_numbers(line[0:index] + str(1 + num_index) + line[index + len(num_word):], index + 1)
        
    return convert_words_to_numbers(line, index + 1)

convert_result = convert_words_to_numbers("two1nine", 0)
convert_failing_result = convert_words_to_numbers("2jvdfdcsnnsonejbxqrmhdjthreesix", 0)
print("Failing result " , convert_failing_result)

def convert_line(line):
    converted = convert_words_to_numbers(line, 0)
    print(line + " => " + converted)
    return converted

step_2_test_input = ["two1nine", "eightwothree","abcone2threexyz","xtwone3four","4nineeightseven2","zoneight234","7pqrstsixteen","two29eighteight1",
                     "2jvdfdcsnnsonejbxqrmhdjthreesix"]
converted_lines = list(map(convert_line, step_2_test_input))
print(converted_lines)
step_2_test_result = sum_calibration_values_for_lines(converted_lines)
print(step_2_test_result)
step_2_converted_input = list(map(convert_line, step_1_input))
step_2_result = sum_calibration_values_for_lines(step_2_converted_input)
print("Step 2 result", step_2_result)

# Suspect conversion is wrong and threetwone should really give 31 as three is first digit and one is effectively last digit - this example isn't present
# so we want the word combination or number with lowest index  and word combination or number with highest index
def get_calibration_value_allowing_for_words(line):
    
    last_index = -1
    last = -1
    first_index = len(line)
    first = -1
    for (num_index, num_word) in enumerate(subs):
        first_index_of_word = line.find(num_word)
        if (first_index_of_word == -1):
            first_index_of_word = len(line)
        first_index_of_number = line.find(str(num_index + 1))
        if (first_index_of_number == -1):
            first_index_of_number = len(line)
        if (first_index_of_word < first_index) or (first_index_of_number < first_index):
            first_index = min(first_index_of_word, first_index_of_number)
            first = num_index + 1

        last_index_of_word = line.rfind(num_word)
        last_index_of_number = line.rfind(str(num_index + 1))
        if (last_index_of_word > last_index) or (last_index_of_number > last_index):
            last_index = max(last_index_of_number, last_index_of_word)
            last = num_index + 1

    return 10 * first + last
    
print(get_calibration_value_allowing_for_words("twone"))
step_2_calibration_values = list(map(get_calibration_value_allowing_for_words, step_1_input))
calibration_sum = sum(step_2_calibration_values)
print("Alternate calibration sub step 2 ", calibration_sum)



