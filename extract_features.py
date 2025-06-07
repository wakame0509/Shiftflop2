def extract_features_for_flop(flop: list) -> list:
    suits = [card[1] for card in flop]
    ranks = [card[0] for card in flop]

    # ランクを数値に変換
    rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                  '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    rank_values = sorted([rank_order[r] for r in ranks])

    features = []

    # スートの種類
    if len(set(suits)) == 1:
        features.append("monosuit")
    elif len(set(suits)) == 2:
        features.append("twotone")
    else:
        features.append("rainbow")

    # ペア・セット
    if len(set(ranks)) < 3:
        features.append("pair_or_set")

    # ストレートの可能性
    if rank_values[2] - rank_values[0] <= 4:
        features.append("straight_possible")

    # オーバーカード（Q以上）
    if any(r >= 12 for r in rank_values):
        features.append("overcard_present")

    # ローカードのみ
    if all(r <= 9 for r in rank_values):
        features.append("low_cards")

    return features
