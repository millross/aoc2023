import itertools as it

def load_file(filename):
    loaded = list()

    input_file = open(filename)
    for (line) in input_file:
        loaded.append(line.rstrip())
    input_file.close()
    return loaded

def group_by_delimiter(lines_list, delimiter):
    return  [list(group) for key, group in it.groupby(lines_list, lambda s: s == delimiter) if not key]

def group_with_fixed_size(lines_list, group_size):
    groups = list()
    for i in range (0, len(lines_list), group_size):
        group = list()
        for j in range(0, group_size):
            group.append(lines_list[i + j])
        groups.append(group)
    return groups
