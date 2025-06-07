import streamlit as st
from calculate_winrate_detailed_v2 import simulate_shift_flop_with_ranking
from opponent_hand_combos import opponent_hand_combos
from hand_utils import all_starting_hands
import pandas as pd
import os

# タイトル
st.title("ShiftFlop 勝率変動ランキング + 特徴量分析")

# 自分のハンド選択
hand = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", [
    "High Card", "Paired", "Connected", "Suited", "Low", "Draw Heavy", "Rainbow"
])

# フロップ数（抽出数）選択
flop_count = st.selectbox("分析に使うフロップの枚数", [10, 20, 30])

# モンテカルロ試行数選択
monte_carlo_trials = st.selectbox("モンテカルロ試行数（1フロップにつき）", [1000, 5000, 10000])

# 計算開始ボタン
if st.button("ShiftFlop 計算開始"):
    st.write("計算中です...")
    avg_shift, top10, worst10, flop_details = simulate_shift_flop_with_ranking(
        hand, flop_type, flop_count, monte_carlo_trials, opponent_hand_combos
    )

    st.success(f"平均勝率変動: {avg_shift:.2f}%")

    st.subheader("勝率上昇 Top 10")
    st.table(top10)

    st.subheader("勝率下降 Worst 10")
    st.table(worst10)

    # CSV保存
    csv_df = pd.DataFrame(flop_details, columns=["Flop", "Shift", "Feature"])
    filename = f"shiftflop_{hand}_{flop_type.replace(' ', '')}.csv"
    csv_df.to_csv(filename, index=False)
    st.success(f"CSVファイル {filename} を保存しました。")
