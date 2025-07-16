import streamlit as st
import pandas as pd
from io import BytesIO

# Your reward logic stays unchanged
# ...

def breakdown_to_dataframe(steps):
    return pd.DataFrame([
        {
            "Count": count,
            "PK Points Used": count * cost,
            "Win per Match": win,
            "Total Win": count * win
        }
        for count, cost, win in steps
    ])

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='PK Breakdown')
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("PK Diamond Optimizer 🔍")
diamonds = st.number_input("Enter your diamond amount 💎", min_value=0)
pk_points = diamonds * 10

if diamonds:
    pk_type, win_total, steps, remainder = reward_breakdown(pk_points)
    remaining_diamonds = remainder // 10

    st.subheader("🎯 Optimal Strategy")
    st.markdown(f"**PK Type:** {pk_type}")
    st.markdown(f"**Total Win Points:** {win_total}")
    st.markdown(f"**Unused Diamonds:** {remaining_diamonds}")

    st.subheader("📊 Breakdown of Rewards")
    df = breakdown_to_dataframe(steps)
    st.dataframe(df)

    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="📥 Download Breakdown as Excel",
        data=excel_data,
        file_name="PK_Reward_Breakdown.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.caption("Export includes all PK cost and win details per match type.")