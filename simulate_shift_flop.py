from typing import List, Tuple, Dict
import random
import eval7
from extract_features import extract_features_for_flop
from hand_utils import convert_hand_to_cards
from preflop_static_dict import get_static_preflop_winrate
from flop_generator import generate_flops_by_type

def simulate_shift_flop_with_features(
    hand_str: str,
    flop_candidates: List[List[str]],
    num_trials: int = 10000,
    sample_count: int = 10
) -> Tuple[float, Dict[str, Tuple[int, float]]]:

    hero_cards = convert_hand_to_cards(hand_str)
    preflop_winrate = get_static_preflop_winrate(hand_str)

    winrate_deltas = []
    feature_stats = {}

    for _ in range(num_trials):
        flop = random.choice(flop_candidates[:sample_count])
        board = [eval7.Card(card) for card in flop]

        deck = eval7.Deck()
        for card in hero_cards + board:
            deck.cards.remove(eval7.Card(card))

        win, tie = 0, 0

        for _ in range(100):  # モンテカルロ内試行
            deck.shuffle()
            opponent = deck.peek(2)
            full_board = board + deck.peek(2)
            hero_val = eval7.evaluate(hero_cards + full_board)
            opp_val = eval7.evaluate(opponent + full_board)

            if hero_val > opp_val:
                win += 1
            elif hero_val == opp_val:
                tie += 1

        postflop_winrate = (win + tie * 0.5) / 100 * 100
        delta = postflop_winrate - preflop_winrate
        winrate_deltas.append(delta)

        features = extract_features_for_flop(flop)
        for feat in features:
            if feat not in feature_stats:
                feature_stats[feat] = [0, 0.0]
            feature_stats[feat][0] += 1
            feature_stats[feat][1] += delta

    avg_shift = sum(winrate_deltas) / len(winrate_deltas) if winrate_deltas else 0.0
    summarized_stats = {k: (v[0], v[1] / v[0]) for k, v in feature_stats.items() if v[0] > 0}
    return avg_shift, summarized_stats
