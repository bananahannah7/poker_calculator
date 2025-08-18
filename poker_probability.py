import random
from collections import Counter

"""
This project takes in a series of cards provided and calculates your chance of having the best hand of the players. 
It depends on what cards you have, what cards are down, and how many people are playing (and how many cards still need to be put down).

It works specifically for texas hold 'em poker where you get two cards in your hand and three cards are placed down, then one more, 
then one last card, and you make the best hand of five using the total possible seven cards. 
"""
SUITS = ["H", "D", "C", "S"] # hearts, diamonds, clubs, and spades
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] # ace marked as highest for high card reasons


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
        raise ValueError(f"Invalid rank: {rank}. Valid ranks are 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K")
    if suit not in SUITS: 
        raise ValueError(f"Invalid suit: {suit}. Valid suits are: H, D, C, S")
    return Card(rank, suit)

# not sure what to call the making of the hand

def hand_evaluator(cards):
    """
    Need to look at poker hand, two cards in hand, 3-5 cards down. From there, we pick the best five cards of the seven possible.
    """

    if len(cards) != 5:
        return ValueError("We can only have a five card hand to evaluate.")
    
    ranks = [card.rank_value for card in cards]
    suits = [card.suit for card in cards]

    flush = len(set(suits)) == 1 # this means all five are same suit

    unique_ranks = sorted(set(ranks))
    straight = False
    straight_high = -1

    # need one case for A-5 straight since A is at bottom not top
    # need one case for all other straights
    # might be worth making case for royal straight here? 

    # royal flush is straight and flush and A K Q J 10
    # use flush and straight and check for the five cards

    # straight flush is straight and flush
    # use flush and straight

    # four of a kind
    # check for sorted list, four of ranks are same

    # full house (three of a kind and pair)
    # check for sorted list, three of ranks are same, two of ranks are same


    # flush
    # use the flush marker

    # straight

    # three of a kind
    # check for sorted list, three of ranks are same
    
    # two pair
    # check for sorted list, two of ranks are same for two different ranks

    # one pair
    # check for sorted list, two of ranks are same

def compare_hands(hand1, hand2):
    score1 = hand_evaluator(hand1)
    score2 = hand_evaluator(hand2)

    return 0

