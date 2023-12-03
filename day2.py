from common import aoc_23_common as aoc_23
# Want a collection class for marbles of each colour, and a "can contain" check

class CubeCollection:
    def __init__(self, green, blue, red):
        self.red = red
        self.green = green
        self.blue = blue

    def can_contain(self, other):
        return self.red >= other.red and self.green >= other.green and self.blue >= other.blue
    
    def __str__(self):
        return str(self.green) + " green, " + str(self.blue) + " blue, " + str(self.red) + " red"
    
    def __repr__(self):
        return str(self)
        
class GameOne:
    def __init__(self, id, handfuls):
        self.id = id
        self.handfuls = handfuls

    def __str__(self):
        return "Game " + str(self.id) + ":" + ";".join(map(str, self.handfuls))

    def is_possible(self, bag):
        mapped = map(lambda handful: bag.can_contain(handful), self.handfuls)
        possible = next(filter(lambda b: b == False, mapped), True)
        return possible
    
    def minimal_bag(self):
        maximum_green = max(map(lambda handful: handful.green, self.handfuls))
        maximum_red = max(map(lambda handful: handful.red, self.handfuls))
        maximum_blue = max(map(lambda handful: handful.blue, self.handfuls))
        return CubeCollection(maximum_green, maximum_blue, maximum_red)
    
    def power(self):
        minimum_bag = self.minimal_bag()
        return minimum_bag.green * minimum_bag.red * minimum_bag.blue
    

class HandfulParser():
    def __init__(self, textual_handful):
        self.green = 0
        self.blue = 0
        self.red = 0
        colour_counts = list(map(lambda s: s.strip(), textual_handful.split(",")))
        for colour_count in colour_counts:
            count_and_colour = colour_count.split(" ")
            count = int(count_and_colour[0])
            colour = count_and_colour[1]

            match colour:
                case "green":
                    self.green = count
                case "blue":
                    self.blue = count
                case "red":
                    self.red = count

    def handful(self):
        return CubeCollection(self.green, self.blue, self.red)
    
class GameDefinitionParser():
    def __init__(self, line):
        id_split = line.split(":")
        self.game_id = int(id_split[0][5:])
        print(id_split)
        print(self.game_id)
        handfuls_textual = id_split[1].split(";")
        self.handfuls = list(map(lambda h: HandfulParser(h).handful(), handfuls_textual))

    def game(self):
        return GameOne(self.game_id, self.handfuls)
        
        
games_one_test_data_as_text = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
]



games_one_test_data = [
    GameOne(1, [CubeCollection(0, 3, 4), CubeCollection(2, 6, 1), CubeCollection(2, 0 ,0)]),
    GameOne(2, [CubeCollection(2, 1, 0), CubeCollection(3, 4, 1), CubeCollection(1, 1, 0)]),
    GameOne(3, [CubeCollection(8, 6, 20), CubeCollection(13, 5, 4), CubeCollection(5, 0, 1)]),
    GameOne(4, [CubeCollection(1, 6, 3), CubeCollection(3, 3, 6), CubeCollection(3, 15, 14)]),
    GameOne(5, [CubeCollection(3, 1, 6), CubeCollection(2,2,1)])
]

games_one_test_bag = CubeCollection(13, 14, 12)

def possible_games(games, bag):
    return filter(lambda game: game.is_possible(bag), games)

def sum_possible_game_ids(games, bag):
    return sum(map(lambda game: game.id, possible_games(games, bag)))

first_game_test_sum = sum_possible_game_ids(games_one_test_data, games_one_test_bag)
print ("First game test sum ", first_game_test_sum)

game_from_text = GameDefinitionParser(games_one_test_data_as_text[0]).game()
print(game_from_text)

first_games_test_data_from_text = list(map(lambda line: GameDefinitionParser(line).game(), games_one_test_data_as_text))
# for game in first_games_test_data_from_text:
#     print(str(game))
#     print("Possible: ", game.is_possible(games_one_test_bag))
print("First test sum from text", sum_possible_game_ids(first_games_test_data_from_text, games_one_test_bag))

print(list(possible_games(first_games_test_data_from_text, games_one_test_bag)))

part_1_input_lines = aoc_23.load_file("day_2_input_1")
part_one_data_from_text = list(map(lambda line: GameDefinitionParser(line).game(), part_1_input_lines))
part_1_game_sum = sum_possible_game_ids(part_one_data_from_text, games_one_test_bag)
print(part_1_game_sum)
# part_1_possible_games = possible_games(part_one_data_from_text, games_one_test_bag)
# print("POSSIBLE GAMES")
# for game in part_1_possible_games:
#     print(game)

for game in first_games_test_data_from_text:
    print ("For game " + str(game.id) + " minimum bag is " + str(game.minimal_bag()))

test_power_sum = sum(map(lambda game: game.power(), first_games_test_data_from_text))

print ("Test power sum ", test_power_sum)

power_sum = sum(map(lambda game: game.power(), part_one_data_from_text))
print ("Power sum ", power_sum)