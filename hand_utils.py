def convert_hand_to_cards(hand_str):
    rank_map = {
        'A': ['Ah', 'Ad', 'Ac', 'As'],
        'K': ['Kh', 'Kd', 'Kc', 'Ks'],
        'Q': ['Qh', 'Qd', 'Qc', 'Qs'],
        'J': ['Jh', 'Jd', 'Jc', 'Js'],
        'T': ['Th', 'Td', 'Tc', 'Ts'],
        '9': ['9h', '9d', '9c', '9s'],
        '8': ['8h', '8d', '8c', '8s'],
        '7': ['7h', '7d', '7c', '7s'],
        '6': ['6h', '6d', '6c', '6s'],
        '5': ['5h', '5d', '5c', '5s'],
        '4': ['4h', '4d', '4c', '4s'],
        '3': ['3h', '3d', '3c', '3s'],
        '2': ['2h', '2d', '2c', '2s'],
    }

    if len(hand_str) == 2:  # ペア
        return [rank_map[hand_str[0]][0], rank_map[hand_str[1]][1]]
    r1, r2, suited = hand_str[0], hand_str[1], hand_str[2] == 's'
    if suited:
        return [rank_map[r1][0], rank_map[r2][0]]
    else:
        return [rank_map[r1][0], rank_map[r2][1]]
