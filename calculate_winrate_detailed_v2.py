# calculate_winrate_detailed_v2.py

import eval7
import random
from hand_group_definitions import classify_hand
from extract_features import extract_features_for_turn
from opponent_hand_combos import opponent_hand_combos
from hand_utils import convert_hand_to_cards
import csv

def simulate_shift_turn_with_ranking(hero_cards, flop_list, opponent_hands):
    average_shifts = []

    for flop in flop_list:
        used = set(hero_cards + flop)
        turn_cards = [card for card in eval7.Deck() if card not in used]

        shift_total = 0
        shift_by_card = {}

        for turn in turn_cards:
            board = flop + [turn]
            win = 0
            total = 0

            for opp in opponent_hands:
                if any(c in used or c == turn for c in opp):
                    continue
                deck = eval7.Deck()
                for card in hero_cards + list(opp) + board:
                    deck.cards.remove(card)

                hero_hand = hero_cards
                opp_hand = list(opp)

                win_score = 0
                for _ in range(100):
                    deck.shuffle()
                    river = deck.peek(1)
                    hero_full = hero_hand + board + river
                    opp_full = opp_hand + board + river
                    hero_eval = eval7.evaluate(hero_full)
                    opp_eval = eval7.evaluate(opp_full)
                    if hero_eval < opp_eval:
                        win_score += 1
                    elif hero_eval == opp_eval:
                        win_score += 0.5

                win_rate = win_score / 100
                win += win_rate
                total += 1

            if total == 0:
                continue

            avg = win / total
            shift_total += avg
            shift_by_card[turn] = avg

        if len(turn_cards) == 0:
            continue

        avg_total = shift_total / len(turn_cards)
        average_shifts.append((flop, avg_total))

    average_shifts.sort(key=lambda x: x[1], reverse=True)
    top10 = average_shifts[:10]
    worst10 = average_shifts[-10:] if len(average_shifts) >= 10 else []

    return sum(x[1] for x in average_shifts) / len(average_shifts), top10, worst10

def save_to_csv(filename, hero_hand, flop_type, avg_shift, top10, worst10):
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Hero Hand', 'Flop Type', 'Average Shift'])
        writer.writerow([hero_hand, flop_type, avg_shift])
        writer.writerow([])
        writer.writerow(['Top 10 Flops', 'Avg Winrate'])
        for flop, shift in top10:
            writer.writerow([' '.join(str(card) for card in flop), shift])
        writer.writerow([])
        writer.writerow(['Worst 10 Flops', 'Avg Winrate'])
        for flop, shift in worst10:
            writer.writerow([' '.join(str(card) for card in flop), shift])
