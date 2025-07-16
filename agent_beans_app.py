import streamlit as st
import pandas as pd
from io import BytesIO

# PK reward data
pk_data = {
    "Daily PK": [(7000, 210), (10000, 300), (20000, 600), (30000, 900),
                 (50000, 1000), (100000, 1800), (150000, 2700)],
    "Talent PK": [(5000, 150), (10000, 350), (20000, 700), (30000, 1000),
                  (50000, 1700)],
    "Agency 2 vs 2 PK": [(5000, 150), (10000, 300), (25000, 800), (50000, 1700),
                         (70000, 2300), (100000, 3500)],
    "Star Tasks PK": [(2000, 60), (10000, 320), (50000, 1700), (80000, 2800),
                      (100000, 3500), (120000, 4000)]
}

# Greedy breakdown logic
def reward_breakdown(pk_points):
    best_type = None
    best_win = 0
    best_steps = []
    remainder = pk_points
    for pk_type, rewards in pk_data.items():
        rewards_sorted = sorted(rewards, reverse=True)
        temp_points = pk_points
        temp_win = 0
        steps = []
        for cost, win in rewards_sorted:
            count = temp_points // cost
            if count:
                temp_points -= count * cost
                temp_win += count * win
                steps.append((count, cost, win))
        if temp_win > best_win:
            best_win = temp_win
            best_type = pk_type
            best_steps = steps
            remainder = temp_points
    return best_type, best_win, best_steps, remainder

def breakdown_to_dataframe(steps):
    return pd.DataFrame([
        {
            "Matches": count,
            "PK Points Used": count * cost,
            "Win per Match": win,
            "Total Win Points": count * win
        }
        for count, cost, win in steps
    ])

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='PK Breakdown')
    return output.getvalue()

# UI
st.set_page_config(page_title="PK Diamond Optimizer", layout="centered")
st.title("PK Diamond Optimizer 💎")

diamonds = st.number_input("Enter your diamond amount", min_value=0, step=100)
pk_points = diamonds * 10

if diamonds:
    pk_type, win_total, steps, remainder = reward_breakdown(pk_points)
    remaining_diamonds = remainder // 10
    df = breakdown_to_dataframe(steps)
    excel_data = convert_df_to_excel(df)

    st.subheader("🎯 Optimal Strategy")
    st.markdown(f"**Best PK Type:** {pk_type}")
    st.markdown(f"**Total Win Points:** {win_total}")
    st.markdown(f"**Unused Diamonds:** {remaining_diamonds}")

    st.subheader("📊 Reward Breakdown")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="📥 Download Breakdown as Excel",
        data=excel_data,
        file_name="PK_Reward_Breakdown.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.caption("Powered by openpyxl — export is clean and compatible.")