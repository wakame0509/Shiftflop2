import itertools
import eval7

def classify_flop(flop):
    suits = [card.suit for card in flop]
    ranks = [card.rank for card in flop]
    unique_suits = set(suits)
    unique_ranks = set(ranks)

    is_monotone = len(unique_suits) == 1
    is_two_tone = len(unique_suits) == 2
    is_paired = len(unique_ranks) < 3

    numeric_ranks = [card_rank_to_int(r) for r in ranks]
    max_gap = max(numeric_ranks) - min(numeric_ranks)

    if is_monotone:
        return "Monotone"
    elif is_two_tone:
        return "Two Tone"
    elif is_paired:
        return "Paired"
    elif max_gap <= 4:
        if all(n >= 10 for n in numeric_ranks):
            return "High Rainbow"
        elif all(n <= 8 for n in numeric_ranks):
            return "Low Mixed"
        else:
            return "Middle Connected"
    else:
        return "Connected Suited"

def card_rank_to_int(rank):
    conversion = {'2': 2, '3': 3, '4': 4, '5': 5,
                  '6': 6, '7': 7, '8': 8, '9': 9,
                  'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return conversion[rank]

def generate_flops_by_type(flop_type):
    deck = list(eval7.Deck())
    all_flops = list(itertools.combinations(deck, 3))
    matched = [list(f) for f in all_flops if classify_flop(f) == flop_type]
    return matched
