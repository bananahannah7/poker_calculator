from collections import Counter
from itertools import combinations
from math import comb

import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image

"""
Texas Hold'em Poker Probability Calculator

This program takes in a series of cards provided and calculates your chance of having the best hand of the players. 
It depends on what cards you have, what cards are down, and how many people are playing.

It works specifically for texas hold 'em poker where you get two cards in your hand and three cards are placed down, then one more, 
then one last card, and you make the best hand of five using the total possible seven cards. 
"""
SUITS = ["H", "D", "C", "S"] # hearts, diamonds, clubs, and spades
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] # ace marked as highest for high card reasons
# indexes 0 to 12 for 2 to 13/A
SUIT_NAMES = {"H": "Hearts", "D": "Diamonds", "C": "Clubs", "S": "Spades"}
RANK_NAMES = {"2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "J": "Jack", "Q": "Queen", "K": "King", "A": "Ace"} # ace marked as highest for high card reasons

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
    """Creates a 52-card deck."""
    return [Card(rank, suit) for rank in RANKS for suit in SUITS]

def card_evaluator(card_str):
    """
    Takes string representation of card and makes it a Card object. 
    Input format is rank then suit. 
    """

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
    Evaluates a 5-card poker hand to return score and tie-breaker information. 

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
    
    Returns a tuple (score, [tie_breakers])
    """

    if len(cards) != 5:
        raise ValueError("We can only have a five card hand to evaluate.")
    
    sorted_cards = sorted(cards, key = lambda card: card.rank_value, reverse = True)
    
    ranks = [card.rank_value for card in sorted_cards]
    suits = [card.suit for card in sorted_cards]

    # Count occurrences of each rank
    rank_counts = Counter(ranks)

    # check for flush
    flush = len(set(suits)) == 1

    # checks for straight
    straight = False
    straight_high = -1 # default fails

    if len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4:
        straight = True
        straight_high = max(ranks)

    elif set(ranks) == {0, 1, 2, 3, 12}: # 12 is ace, checks for A-5 case
        straight = True
        straight_high = 3

    # Royal flush (straight, flush, A, K, Q, J, 10)
    if straight and flush and (12 in ranks) and (straight_high == 12):
        return (9, []) # no rank marker, this is best possible hand

    # Straight flush (straight and flush)
    if straight and flush: 
        return (8, [straight_high])

    # Four of a kind
    for rank, count in rank_counts.items():
        if count == 4:
            tie_breaker = [val for val in ranks if val != rank][0]
            return (7, [rank, tie_breaker])

    # Full house (three of a kind and pair)
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
    if flush:
        return (5, ranks)

    # straight
    if straight:
        return (4, [straight_high])

    # three of a kind
    for rank, count in rank_counts.items():
        if count == 3:
            other_cards = sorted([val for val in ranks if val != rank], reverse = True)
            return (3, [rank] + other_cards)
    
    # two pair
    pairs = []
    for rank, count in rank_counts.items(): 
        if count == 2:
            pairs.append(rank)

    if len(pairs) == 2:
        pairs.sort(reverse = True)
        tie_breaker = [val for val in ranks if val not in pairs][0]
        return (2, pairs + [tie_breaker])


    # one pair
    for rank, count in rank_counts.items():
        if count == 2:
            other_cards = sorted([val for val in ranks if val != rank], reverse = True)
            return (1, [rank] + other_cards)


    # high card
    return (0, sorted(ranks, reverse = True))


def compare_scores(score1, score2):
    """
    Compares two poker hands and returns:
    1 if score1 is better, 
    -1 if score2 is better,
    0 if equal
    """

    # compares type of hand
    if score1[0] > score2[0]:
        return 1
    
    elif score1[0] < score2[0]:
        return -1
    
    # looks at tie breakers and values if same type hand
    for val1, val2 in zip(score1[1], score2[1]):
        if val1 < val2:
            return -1
        if val2 < val1:
            return 1
        
    # exact tie, only differs in suits
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
            comparator = compare_scores(score, best_score)
            if comparator > 0:
                best_hand = hand
                best_score = score

    return best_hand

def probability_calculator(my_hand, community_cards, player_count):

    """ Looks at chance of winning with all five cards down, using number of players, 
    my hand, and cards down to find which hands can beat mine of total possible hands.
    Inputs: my_hand (two cards)
    community_cards (five cards)    
    player_count (number of players in game as integer)
    
    Returns: chances of winning
    """


    if len(my_hand) != 2:
        raise ValueError("You need exactly two cards in your hand")
    
    if len(community_cards) != 5:
        raise ValueError("All 5 community cards must be known in current functionality")
    
    my_best_hand = find_best_five(my_hand + community_cards)
    my_score = hand_evaluator(my_best_hand)

    # create deck, remove known cards
    full_deck = create_deck()
    known_cards = my_hand + community_cards

    remaining_deck = [card for card in full_deck
                      if not any(card.rank == known.rank and card.suit == known.suit for known in known_cards)]
    
    # calculate total number of opponent hands
    opp_hands_count = comb(len(remaining_deck), 2)

    wins = 0
    ties = 0

    # check my hand against all opponent hands
    for opp_cards in combinations(remaining_deck, 2):
        opp_best_hand = find_best_five(list(opp_cards) + community_cards)
        opp_score = hand_evaluator(opp_best_hand)
        comparator = compare_scores(my_score, opp_score)

        if comparator > 0: # win
            wins += 1
        elif comparator == 0:
            ties += 1

    # calculate chance against one opponent
    win_probability = (wins + ties/2) / opp_hands_count

    # calculate chance against multiple opponents (removes self)
    win_probability = win_probability ** (player_count - 1)

    return win_probability


class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Porbability Calculator")
        self.root.geometry("1200x800")
        self.root.configure(bg ="#FFFFFF")
        
        self.my_hand = []
        self.community_cards = []
        self.selected_cards = []
        self.card_images = {}

        # need to set up all card decks
        self.load_card_deck()

        # need to pick number of players
        self.select_player_count()

        # need to pick cards
        self.select_cards()

        self.status_label.config(text = "Select cards")

    def load_card_deck(self):
        self.card_images_dict = {}


        card_size = (80, 120)

        try: 
            back_path = "cards/Suit=Other, Number=Back Blue.png"
            back_img = Image.open(back_path).resize(card_size)
            self.card_back = Image.PhotoImage(back_img)
        
        except Exception as error:
            print(f"Warning: Could not load image: {error}")
            back_img = Image.new("RGB", card_size, color = "blue")
            self.card_back = Image.PhotoImage(back_img)


# def main(): 

#     # intro script
#     print("Poker Probability Calculator for Texas Hold'em")
#     print("----------------------------------------------")

#     print("\nEnter your two cards, with the card rank then suit (H, D, S, C). For example, AS for Ace of Spades, 10D for D of Diamonds.")
    
#     # get player hand
#     my_hand = []
#     while len(my_hand) < 2:
#         try:
#             card_str = input(f"Card {len(my_hand) + 1}: ")
#             card = card_evaluator(card_str)
#             if card in my_hand:
#                 print("This card has already been entered. Please enter a different card.")
#                 continue
#             my_hand.append(card)
#         except ValueError as error:
#             print(f"Invalid card: {error}")

#     # get community cards
#     print("\nEnter the five community cards: ")
#     community_cards = []

#     while len(community_cards) < 5:
#         try: 
#             card_str = input(f"Community card{len(community_cards) + 1}: ")
#             card = card_evaluator(card_str)
#             if card in my_hand or card in community_cards:
#                 print("This card has already been entered. Please enter a different card.")
#                 continue

#             community_cards.append(card)
#         except ValueError as error:
#             print(f"Invalid card: {error}")

#     # get player count
#     player_count = 0
#     while player_count < 2 or player_count > 10:
#         try: 
#             player_count = int(input("\nEnter the number of players, including yourself: "))
#             if player_count < 2:
#                 print("There must be at least 2 players.")
#             elif player_count > 10:
#                 print("There must not be more than 10 players.")

#         except ValueError as error:
#             print(f"{error} was invalid. Please enter a valid number.")

#     # calculate results
#     best_hand = find_best_five(my_hand + community_cards)
#     hand_score = hand_evaluator(best_hand)

#     hand_types = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]

#     # print results
#     print("\nCalculating probability of winning...")
#     probability = probability_calculator(my_hand, community_cards, player_count)
    
#     print(f"Your hand: {my_hand}")
#     print(f"Community cards: {community_cards}")
#     print(f"Your best five-card hand: {best_hand} ({hand_types[hand_score[0]]})")
#     print(f"Number of players: {player_count}")

#     print(f"Probability of winning: ({probability*100:.2f}%)")

if __name__ == "__main__":
    main()