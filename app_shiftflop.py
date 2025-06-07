import streamlit as st
import pandas as pd
from calculate_winrate_detailed_v2 import simulate_shiftflop_montecarlo
from flop_generator import generate_flops_by_type
from hand_utils import all_starting_hands
import datetime

st.title("ShiftFlop: 勝率変動シミュレーター（モンテカルロ方式）")

# 自分のハンド選択
hand_str = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", [
    "High Rainbow", "Low Connected", "Paired", "Monotone", "Two Tone", "Wet", "Dry"
])

# モンテカルロ試行回数選択
mc_trials = st.selectbox("モンテカルロ試行回数", [1000, 5000, 10000, 20000])

if st.button("シミュレーション実行"):
    with st.spinner("計算中..."):
        result_df = simulate_shiftflop_montecarlo(hand_str, flop_type, mc_trials)
        st.dataframe(result_df)

        # CSV保存機能
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"shiftflop_{hand_str}_{flop_type}_{mc_trials}_{now}.csv"
        result_df.to_csv(csv_path, index=False)
        st.success(f"結果をCSVで保存しました: {csv_path}")
        with open(csv_path, "rb") as f:
            st.download_button("📥 CSVをダウンロード", f, file_name=csv_path)
