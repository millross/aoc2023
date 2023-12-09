from common import aoc_23_common as aoc_23

class LeftRightPair:
    def __init__(self, left_and_right):
        self._left_and_right = left_and_right

    def __str__(self):
        return "(" + self.left + ", " + self.right + ")"
    
    def __repr__(self):
        return str(self)

    @property
    def left(self):
        return self._left_and_right[0]
    
    @property
    def right(self):
        return self._left_and_right[1]
    
class NodeDefinitionParser:
    def __init__(self, node_definition):    
        components = map(lambda s: s.strip(), node_definition.split("="))
        self.node_index = components[0]
        self.destinations = LeftRightParser(components[1]).destinations

    def __str__(self):
        return self.node_index + " = " + self.destinations
    
    def __repr__(self):
        return str(self)
    
class LeftRightParser:
    def __init__(self, left_right_definition):
        destinations = map(lambda s: s.strip(), left_right_definition[1:-1].split(","))
        self.destinations = LeftRightPair(list(destinations))


class Network:
    def __init__(self, node_definitions):
        self.nodes = {}
        for definition in node_definitions:
            

test_input = aoc_23.load_file("day8_test_input")
test_route = test_input[0]
test_node_def_lines = test_input[2:]

print(test_node_def_lines)

# Initially we'll treat the network as a dictionary of tuples
print(LeftRightParser("(BBB, CCC)").destinations)
