import random
from collections import Counter

SUITS = ["H", "D", "C", "S"] # hearts, diamonds, clubs, and spades
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] # ace marked as highest for high card reasons


"""




"""

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

