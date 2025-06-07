import streamlit as st
from calculate_shiftflop import simulate_shift_flop
from hand_utils import all_starting_hands
from opponent_hand_combos import opponent_hand_combos
from flop_generator import generate_flops_by_type

st.title("ShiftFlop: フロップタイプによる勝率変動")

# 自分のハンドを169通りから選択
hand = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプを選択
flop_type = st.selectbox("フロップタイプを選択", [
    "High Card", "Low Card", "Paired", "Monotone",
    "Two-tone", "Connected", "Disconnected"
])

# フロップ枚数を選択（10枚、20枚、30枚）
flop_count = st.selectbox("フロップの枚数を選択", [10, 20, 30])

# モンテカルロ試行回数を選択（10～50回）
mc_trials = st.selectbox("モンテカルロ試行回数（フロップ抽出）", list(range(10, 51, 10)))

if st.button("計算開始"):
    with st.spinner("計算中..."):
        flop_list = generate_flops_by_type(flop_type, count=flop_count)
        avg_shift = simulate_shift_flop(hand, flop_list, opponent_hand_combos, mc_trials)
    st.success("完了！")
    st.write(f"平均勝率変動: {avg_shift:.2f}%")
