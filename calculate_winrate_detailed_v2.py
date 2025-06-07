import eval7
import random
from collections import Counter
from flop_generator import generate_flops_by_type
from extract_features import extract_features_for_flop
from hand_utils import convert_hand_to_cards
from preflop_static_winrates import get_static_preflop_winrate


def simulate_shift_flop_with_features(hand_str, flop_type, num_trials=10000):
    hero_cards = convert_hand_to_cards(hand_str)
    preflop_winrate = get_static_preflop_winrate(hand_str)

    all_candidate_flops = generate_flops_by_type(hero_cards, flop_type)
    if len(all_candidate_flops) == 0:
        return 0.0, {}

    shift_values = []
    feature_counts = Counter()

    for _ in range(num_trials):
        flop = random.choice(all_candidate_flops)

        deck = eval7.Deck()
        for card in hero_cards + flop:
            deck.cards.remove(card)

        villain_hand = deck.peek(2)
        board = flop
        full_board = flop + deck.peek(2, offset=2)  # ターン・リバーを仮に生成

        hero_hand = hero_cards
        villain_hand = deck.peek(2)

        hero_score = eval7.evaluate(hero_hand + full_board)
        villain_score = eval7.evaluate(villain_hand + full_board)

        if hero_score > villain_score:
            result = 1
        elif hero_score == villain_score:
            result = 0.5
        else:
            result = 0

        shift = result - preflop_winrate / 100
        shift_values.append(shift)

        features = extract_features_for_flop(hero_cards, flop)
        for feat in features:
            feature_counts[feat] += shift

    if not shift_values:
        return 0.0, {}

    avg_shift = sum(shift_values) / len(shift_values)

    # 特徴量ごとの平均変化量を算出
    feature_avg_shifts = {
        k: round(v / feature_counts[k], 5) if feature_counts[k] != 0 else 0.0
        for k, v in feature_counts.items()
    }

    return round(avg_shift * 100, 3), feature_avg_shifts
