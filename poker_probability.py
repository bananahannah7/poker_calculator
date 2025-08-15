import random
from collections import Counter

SUITS = ["H", "D", "C", "S"] # hearts, diamonds, clubs, and spades
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] # ace marked as highest for high card reasons


"""




"""

class Card: 
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.rank_value = RANKS.index(rank)

    
    def __str__(self):
        return f"{self.rank} of {self.suit}"


    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    

def create_deck():
    for rank in RANKS:
        for suit in SUITS:
            yield Card(rank, suit)
    

def parse_hand(hand_str):
    