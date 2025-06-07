import streamlit as st
from calculate_winrate_detailed_v2 import simulate_shift_flop_with_features
from flop_generator import generate_flops_by_type

# 全169通りのスターティングハンド
all_starting_hands = [
    "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
    "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
    "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
    "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
    "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
    "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
    "98s", "97s", "96s", "95s", "94s", "93s", "92s",
    "87s", "86s", "85s", "84s", "83s", "82s",
    "76s", "75s", "74s", "73s", "72s",
    "65s", "64s", "63s", "62s",
    "54s", "53s", "52s",
    "43s", "42s",
    "32s",
    "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o", "A2o",
    "KQo", "KJo", "KTo", "K9o", "K8o", "K7o", "K6o", "K5o", "K4o", "K3o", "K2o",
    "QJo", "QTo", "Q9o", "Q8o", "Q7o", "Q6o", "Q5o", "Q4o", "Q3o", "Q2o",
    "JTo", "J9o", "J8o", "J7o", "J6o", "J5o", "J4o", "J3o", "J2o",
    "T9o", "T8o", "T7o", "T6o", "T5o", "T4o", "T3o", "T2o",
    "98o", "97o", "96o", "95o", "94o", "93o", "92o",
    "87o", "86o", "85o", "84o", "83o", "82o",
    "76o", "75o", "74o", "73o", "72o",
    "65o", "64o", "63o", "62o",
    "54o", "53o", "52o",
    "43o", "42o",
    "32o"
]

# Streamlit UI
st.title("ShiftFlop 勝率変動解析")
selected_hand = st.selectbox("自分のハンドを選択", all_starting_hands)

flop_type = st.selectbox("フロップタイプを選択", [
    "High Rainbow", "High Two-tone", "Middle Rainbow", "Middle Two-tone",
    "Low Rainbow", "Low Two-tone", "Paired Board"
])

num_trials = st.selectbox("モンテカルロ試行回数", [1000, 10000, 50000, 100000])
flop_count = st.selectbox("試行ごとのフロップ生成数", [10, 20, 30])

if st.button("計算開始"):
    with st.spinner("計算中..."):
        flops = generate_flops_by_type(flop_type)
        avg_shift, feature_stats = simulate_shift_flop_with_features(
            selected_hand, flops, num_trials=num_trials, sample_count=flop_count
        )

    st.success("計算完了")
    st.markdown(f"### 平均勝率変動: `{avg_shift:.2f}%`")
    st.markdown("### 特徴量別の出現頻度と勝率変動")

    for feat, (count, avg_delta) in feature_stats.items():
        st.markdown(f"- **{feat}**: 出現 `{count}` 回, 平均変化 `{avg_delta:.2f}%`")
