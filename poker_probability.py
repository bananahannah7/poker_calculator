# import random
from collections import Counter

from itertools import combinations

from math import comb

"""
This project takes in a series of cards provided and calculates your chance of having the best hand of the players. 
It depends on what cards you have, what cards are down, and how many people are playing (and how many cards still need to be put down).

It works specifically for texas hold 'em poker where you get two cards in your hand and three cards are placed down, then one more, 
then one last card, and you make the best hand of five using the total possible seven cards. 
"""
SUITS = ["H", "D", "C", "S"] # hearts, diamonds, clubs, and spades
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] # ace marked as highest for high card reasons
# indexes 0 to 12 for 2 to 13/A

class Card: 
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        
        self.rank = rank
        self.suit = suit
        self.rank_value = RANKS.index(rank)

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False
    
def create_deck():
    return [Card(rank, suit) for rank in RANKS for suit in SUITS]

def card_evaluator(card_str):
    if len(card_str) < 2 or len(card_str) > 3:
        raise ValueError(f"Invalid format of card: {card_str}. Use format like AS or 10D)")
    rank, suit = card_str[:-1].upper(), card_str[-1].upper()

    if rank not in RANKS: 
        raise ValueError(f"Invalid rank: {rank}. Valid ranks are 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A")
    if suit not in SUITS: 
        raise ValueError(f"Invalid suit: {suit}. Valid suits are: H, D, C, S")
    return Card(rank, suit)

def hand_evaluator(cards):
    """
    Need to look at poker hand, two cards in hand, 3-5 cards down. From there, we pick the best five cards of the seven possible.
    """

    """
    Hand rankings by score
    9: Royal Flush (straight, flush, AKQJ10)
    8: Straight Flush (straight, flush, need to know what highest card value is)
    7: Four of a Kind (all four same card rank, need to know value)
    6: Full House (three of a kind, pair, need to know values of each)
    5: Flush (all five one suit, need to know values)
    4: Straight (five in a row, need to know high card)
    3: Three of a Kind (three of same value, need to know value)
    2: Two Pair (two pairs, need to know values)
    1: One Pair (one pair, need to know value)
    0: High Card (purely value based)
    
    """

    if len(cards) != 5:
        raise ValueError("We can only have a five card hand to evaluate.")
    
    sorted_cards = sorted(cards, key = lambda card: card.rank_value, reverse = True)
    
    ranks = [card.rank_value for card in sorted_cards]
    suits = [card.suit for card in sorted_cards]

    # how many of each rank, used for high, pair, 2 pair, 3 of kind, 4 of kind
    rank_counts = Counter(ranks)

    # check for flush
    flush = len(set(suits)) == 1


    # need one case for A-5 straight since A is at bottom not top
    # need one case for all other straights
    # might be worth making case for royal straight here? 

    straight = False
    straight_high = -1 # default fails

    if len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4:
        straight = True
        straight_high = max(ranks)

    elif set(ranks) == {0, 1, 2, 3, 12}: # 12 is ace
        straight = True
        straight_high = 3

    # royal flush is straight and flush and A K Q J 10
    # use flush and straight and check for the five cards

    if straight and flush and (12 in ranks) and (straight_high == 12):
        return (9, []) # no rank marker, this is best possible hand

    # straight flush is straight and flush
    # use flush and straight

    if straight and flush: 
        return (8, [straight_high])

    # four of a kind
    # check for sorted list, four of ranks are same

    for rank, count in rank_counts.items():
        if count == 4:
            tie_breaker = [val for val in ranks if val != rank][0]
            return (7, [rank, tie_breaker])

    # full house (three of a kind and pair)
    # check for sorted list, three of ranks are same, two of ranks are same

    three_val = None
    pair_val = None
    for rank, count, in rank_counts.items():
        if count == 3: 
            three_val = rank
        elif count == 2:
            pair_val = rank
    
    if three_val is not None and pair_val is not None:
        return (6, [three_val, pair_val])

    # flush
    # use the flush marker

    if flush:
        return (5, ranks)

    # straight

    if straight:
        return (4, [straight_high])

    # three of a kind
    # check for sorted list, three of ranks are same

    for rank, count in rank_counts.items():
        if count == 3:
            other_cards = sorted([val for val in ranks if val != rank], reverse = True)
            return (3, [rank] + other_cards)
    
    # two pair
    # check for sorted list, two of ranks are same for two different ranks
    pairs = []
    for rank, count in rank_counts.items(): 
        if count == 2:
            pairs.append(rank)

    if len(pairs) == 2:
        pairs.sort(reverse = True)
        tie_breaker = [val for val in ranks if val not in pairs][0]
        return (2, pairs + [tie_breaker])


    # one pair
    # check for sorted list, two of ranks are same

    for rank, count in rank_counts.items():
        if count == 2:
            other_cards = sorted([val for val in ranks if val != rank], reverse = True)
            return (1, [rank] + other_cards)


    # high card

    return (0, sorted(ranks, reverse = True))


def compare_hands(hand1, hand2):
    score1 = hand_evaluator(hand1)
    score2 = hand_evaluator(hand2)

    if score1[0] > score2[0]:
        return 1
    
    elif score1[0] < score2[0]:
        return -1
    
    for val1, val2 in zip(score1[1], score2[1]):
        if val1 < val2:
            return -1
        if val2 < val1:
            return 1
        
    # exact tie, only diff in suits, most likely
    return 0

def find_best_five(cards):
    """ Finds the best five cards of seven (five down, two in hand) for you to play."""

    if len(cards) < 5: 
        raise ValueError("Need at least 5 cards to make hand")
    
    best_hand = None
    best_score = (-1, []) # dummy low score, empty tie breakers

    for five_cards in combinations(cards, 5):
        hand = list(five_cards)
        score = hand_evaluator(hand)

        if best_hand is None:
            best_hand = hand
            best_score = score
        else:
            comparator = compare_hands(hand, best_hand)
            if comparator > 0:
                best_hand = hand
                best_score = score

    return best_hand

def probability_calculator(my_hand, community_cards, player_count):

    """ Looks at chance of winning with all five cards down, using number of players, my hand, and cards down to find which hands can beat mine of total possible hands."""


    if len(my_hand) != 2:
        raise ValueError("You need exactly two cards in your hand")
    
    if len(community_cards) != 5:
        raise ValueError("All 5 community cards must be known in current functionality")
    

    my_best_hand = find_best_five(my_hand + community_cards)

    full_deck = create_deck()
    known_cards = my_hand + community_cards

    remaining_deck = [card for card in full_deck
                      if not any(card.rank == known.rank and card.suit == known.suit for known in known_cards)]
    
    opp_hands_count = comb(len(remaining_deck), 2)

    wins = 0
    ties = 0

    for opp_cards in combinations(remaining_deck, 2):
        opp_best_hand = find_best_five(list(opp_cards) + community_cards)
        comparator = compare_hands(my_best_hand, opp_best_hand)

        if comparator > 0: # win
            wins += 1
        elif comparator == 0:
            ties += 1

    win_probability = (wins + ties/2) / opp_hands_count

    win_probability = win_probability ** (player_count - 1)

    return win_probability



def main(): 
    my_hand = [card_evaluator("9S"), card_evaluator("8S")]
    community_cards = [card_evaluator("QS"), card_evaluator("JS"), card_evaluator("10S"), card_evaluator("2H"), card_evaluator("3C")]


    player_count = 4

    probability = probability_calculator(my_hand, community_cards, player_count)
    print(f"Probability of winning: ({probability*100:.2f}%)")


if __name__ == "__main__":
    main()