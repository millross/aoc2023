import common.aoc_23_common as common
from collections import Counter
from enum import Enum
import functools

CARDS = "23456789TJQKA"
CARDS_ADJUSTED_FOR_JOKER = "J23456789TQKA"

class HAND_TYPE(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def card_value(card):
    return CARDS.index(card)

def hand_type(cards):
    counter = Counter(cards)
    max_matching = max(counter.values())
    match max_matching:

        case 5:
            return HAND_TYPE.FIVE_OF_A_KIND
        
        case 4:
            return HAND_TYPE.FOUR_OF_A_KIND
        
        case 3:
            if min(counter.values()) == 2:
                return HAND_TYPE.FULL_HOUSE
            else:
                return HAND_TYPE.THREE_OF_A_KIND
            
        case 2:
            # one or two pairs
            if len(counter.values()) == 3:
                return HAND_TYPE.TWO_PAIR
            else:
                return HAND_TYPE.ONE_PAIR

        case 1:
            return HAND_TYPE.HIGH_CARD
        
        case _:
            raise Exception("Unidentifiable hand " + cards)
        
    return counter

def hand_type_joker_adjusted(cards):
    non_jokers = cards.replace("J", "")
    jokers_count = len(cards) - len(non_jokers)
    counter = Counter(non_jokers)
    if len(counter.values()) == 0:
        # All jokers
        return HAND_TYPE.FIVE_OF_A_KIND
    max_matching = max(counter.values())
    match max_matching + jokers_count:

        case 5:
            return HAND_TYPE.FIVE_OF_A_KIND
        
        case 4:
            return HAND_TYPE.FOUR_OF_A_KIND
        
        case 3:
            # max matching must be 1, 2 or 3
            match max_matching:
                case 1:
                    # This means 2 jokers and 3 different cards
                    return HAND_TYPE.THREE_OF_A_KIND
                
                case 2 | 3: 
                    # Means 1 joker and possibly 2 pair so could be full house
                    # Or no joker and 3 of a kind or full house
                    if min(counter.values()) == 2:
                        return HAND_TYPE.FULL_HOUSE
                    else:
                        return HAND_TYPE.THREE_OF_A_KIND

        case 2:
            # 2 pairs only possible if no jokers involved, in this case we would have only 3 values
            if len(counter.values()) == 3:
                return HAND_TYPE.TWO_PAIR
            else:
                return HAND_TYPE.ONE_PAIR

        case 1:
            return HAND_TYPE.HIGH_CARD
        
        case _:
            raise Exception("Unidentifiable hand " + cards)        


def compare_hands(hand1, hand2, card_scores):
    types_diff = hand1.type.value - hand2.type.value
    if types_diff > 0:
        return 1
    elif types_diff < 0:
        return -1
    else:
        # We need to compare cards in hand in order
        for idx, card in enumerate(hand1.cards):
            card2 = hand2.cards[idx]
            card_score = card_scores.index(card)
            card2_score = card_scores.index(card2)
            if card_score > card2_score:
                return 1
            elif card_score < card2_score:
                return -1
            # Fall through to next card if we have exact match

class HandComparatorFactory:
    def __init__(self, card_scores):
        self.card_scores = card_scores

    def comparator(self):
        return lambda hand1, hand2: compare_hands(hand1, hand2, self.card_scores)    

class HandsLoader:

    def __line_to_hand(self, line, type_decider):
        components = line.split()
        cards = components[0]
        bid = int(components[1])
        return Hand(cards, bid, type_decider)

    def __init__(self, file_name, type_decider):
        lines = common.load_file(file_name)
        self._hands = list(map(lambda l: self.__line_to_hand(l, type_decider), lines))

    def hands(self):
        return self._hands


class Hand:
    def __init__(self, cards, bid, type_decider):
        self.cards = cards
        self.bid = bid
        self.type = type_decider(cards)

    def __str__(self):
        return "Hand " + self.cards + " with bid " + str(self.bid) + " and type " + str(self.type.name)

    def __repr__(self):
        return str(self)

    
class OrderedHands:
    def __init__(self, hands, card_scores):
        self._hands = hands
        self.card_scores = card_scores
        self.comparator = HandComparatorFactory(card_scores).comparator()

    def ordered(self):
        return sorted(self._hands, key=functools.cmp_to_key(self.comparator))
    
class WinningsCalculator:
    
    def __init__(self, ordered_hands):
        self.hands = ordered_hands

    def total_winnings(self):
        ranks = range(1, len(self.hands) + 1)
        winnings = map(lambda r: r * (self.hands[r - 1]).bid, ranks)
        return sum(winnings)

class Part1Analysis:
    def __init__(self, filename, type_decider, card_scores):
        self._hands = HandsLoader(filename, type_decider).hands()
        self.card_scores = card_scores

    def total_winnings(self):
        ordered_hands = OrderedHands(self._hands, self.card_scores).ordered()
        return WinningsCalculator(ordered_hands).total_winnings()

part1_test_wiinnings = Part1Analysis("day7_test_input", hand_type, CARDS).total_winnings()
print ("Part 1 test winnings ", part1_test_wiinnings)

part1_winnings = Part1Analysis("day7_input", hand_type, CARDS).total_winnings()
print("Part 1 winnings ", part1_winnings)

part2_test_winnings = Part1Analysis("day7_test_input", hand_type_joker_adjusted, CARDS_ADJUSTED_FOR_JOKER).total_winnings()
print("Part 2 test winnings", part2_test_winnings)

part_2_winnings = Part1Analysis("day7_input", hand_type_joker_adjusted, CARDS_ADJUSTED_FOR_JOKER).total_winnings()
print("Part 2 winnings", part_2_winnings)