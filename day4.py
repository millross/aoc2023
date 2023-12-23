from common import aoc_23_common as aoc23
import re

CARD_ID_REGEX = "Card\s+(\d+)"

class ScratchCard:
    def __init__(self, id, winning_numbers, actual_numbers):
        self.id = id
        self.winning_numbers = winning_numbers
        self.actual_numbers = actual_numbers

    def __str__(self):
        return "Card " + str(self.id) + ": " + str(self.winning_numbers) + "| " + str(self.actual_numbers)
    
    def __repr__(self):
        return str(self)

class CardParser:

    def __parse_numbers_list(self, numbers_list_string):
        return set(map(int, numbers_list_string.split()))

    def __init__(self, line):
        line_components = line.split(":")
        card_id_match = re.match(CARD_ID_REGEX, line_components[0])
        self.card_id = int(card_id_match.group(1))
        numbers_lists = list(map(lambda s: s.strip(), line_components[1].split("|")))
        self.winning_numbers = self.__parse_numbers_list(numbers_lists[0])
        self.actual_numbers = self.__parse_numbers_list(numbers_lists[1])

    def scratch_card(self):
        return ScratchCard(self.card_id, self.winning_numbers, self.actual_numbers)

class CardScorer:
    def __init__(self, card):
        self.card = card

    def matches(self):
        return len(self.card.winning_numbers.intersection(self.card.actual_numbers))
    
    def score(self):
        common_count = self.matches()
        if (common_count == 0):
            return 0
        else:
            return pow(2, common_count - 1)

test_lines = aoc23.load_file("day4_test_input")

test_line = "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"

test_scratch_cards = list(map(lambda l: CardParser(l).scratch_card(), test_lines))
test_scores = map(lambda c: CardScorer(c).score(), test_scratch_cards)
print("Total test score:", sum(test_scores))

input_lines = aoc23.load_file("day4_input")
scratch_cards = list(map(lambda l: CardParser(l).scratch_card(), input_lines))
scores = map(lambda c: CardScorer(c).score(), scratch_cards)
print("Total part 1 score:", sum(scores))

# For part 2 add copies dictionary and track the copies we add, use a card accumulator to track the total
# and increase.
# Scoring has also changed to apply number of matches as score

class CardAccumulator:

    def __init__(self, cards):
        self.cards = cards
        self.counts = list(map(lambda c: 1, cards))

    def add_cards(self, card_idx, card):
        score = CardScorer(card).matches()
        multiplier = self.counts[card_idx]
        for idx in range (card_idx + 1, min(card_idx + score + 1, len(self.cards))):
            print("Incrementing at ", idx, " by ", multiplier)
            self.counts[idx] = self.counts[idx] + multiplier

    def accumulate(self):
        for (idx, card) in enumerate(self.cards):
            self.add_cards(idx, card)

test_accumulator = CardAccumulator(test_scratch_cards)
test_accumulator.accumulate()
print(test_accumulator.counts)

accumulator = CardAccumulator(scratch_cards)
accumulator.accumulate()
print("Total cards", sum(accumulator.counts))
