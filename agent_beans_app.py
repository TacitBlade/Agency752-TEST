import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO

git add requirements.txt agent_beans_app.py
git commit -m "Fix: correct openpyxl import syntax and ensure dependency version"
git push origin main


def calculate_total_beans(beans_earned, salary_usd):
    salary_beans = salary_usd * 210
    commission = beans_earned * 0.05
    total = salary_beans + commission
    return salary_beans, commission, total

st.set_page_config(page_title="Agent Bean Calculator", layout="centered")
st.title("🎯 Agent Bean Calculator")

with st.form("bean_calc_form"):
    num_agents = st.number_input("How many agents?", min_value=1, step=1)
    agents_input = []
    for i in range(int(num_agents)):
        st.markdown(f"#### Agent {i+1}")
        name = st.text_input(f"Name", key=f"name_{i}")
        beans_earned = st.number_input("Beans Earned by Host", key=f"beans_{i}")
        salary_usd = st.number_input("Basic Salary (USD)", key=f"salary_{i}")
        agents_input.append({
            "name": name,
            "beans_earned": beans_earned,
            "salary_usd": salary_usd
        })
    submitted = st.form_submit_button("Calculate")

if submitted:
    results = []
    for agent in agents_input:
        salary_beans, commission, total = calculate_total_beans(
            agent["beans_earned"],
            agent["salary_usd"]
        )
        results.append({
            "Agent": agent["name"],
            "Beans Earned": agent["beans_earned"],
            "Salary (USD)": agent["salary_usd"],
            "Salary in Beans": salary_beans,
            "5% Commission": commission,
            "Total Beans": total
        })

    df = pd.DataFrame(results)
    st.success("✅ Calculations complete!")
    st.dataframe(df)

    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    st.download_button(
        "📥 Download Excel File",
        data=buffer.getvalue(),
        file_name="agent_beans_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
