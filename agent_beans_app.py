import streamlit as st
import pandas as pd
from io import BytesIO

# Function to calculate salary in beans, commission, and total
def calculate_total_beans(beans_earned, salary_usd):
    salary_beans = salary_usd * 210
    commission = beans_earned * 0.05
    total = salary_beans + commission
    return salary_beans, commission, total

# Streamlit app configuration
st.set_page_config(page_title="Agent Bean Calculator", layout="centered")
st.title("🎯 Agent Bean Calculator")

# Form input
with st.form("bean_calc_form"):
    num_agents = st.number_input("How many agents?", min_value=1, step=1)
    agents_input = []

    for i in range(int(num_agents)):
        with st.expander(f"🧍 Agent {i+1} Details", expanded=True):
            name = st.text_input("Name", key=f"name_{i}")
            beans_earned = st.number_input("Beans Earned by Host 🎭", min_value=0.0, step=100.0, key=f"beans_{i}")
            salary_usd = st.number_input("Basic Salary 💵 (USD)", min_value=0.0, step=100.0, key=f"salary_{i}")
            agents_input.append({
                "name": name.strip(),
                "beans_earned": beans_earned,
                "salary_usd": salary_usd
            })

    submitted = st.form_submit_button("Calculate")

# Output calculation
if submitted:
    # Basic validation
    if any(agent["name"] == "" for agent in agents_input):
        st.error("🚫 Please enter a name for every agent.")
    else:
        results = []
        for agent in agents_input:
            salary_beans, commission, total = calculate_total_beans(
                agent["beans_earned"],
                agent["salary_usd"]
            )
            results.append({
                "Agent": agent["name"],
                "Beans Earned": round(agent["beans_earned"], 2),
                "Salary (USD)": round(agent["salary_usd"], 2),
                "Salary in Beans": round(salary_beans, 2),
                "5% Commission": round(commission, 2),
                "Total Beans": round(total, 2)
            })

        df = pd.DataFrame(results)
        df = df.sort_values(by="Total Beans", ascending=False)

        st.success("✅ Calculations complete!")
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}), use_container_width=True)

        # Summary metric
        total_all = df["Total Beans"].sum()
        st.info(f"💰 **Total Beans Across All Agents:** {round(total_all, 2)}")

        # Download option
        output = BytesIO()
        df.to_excel(output, index=False, sheet_name='Agent Beans')
        st.download_button(
            "📥 Download Results as Excel",
            output.getvalue(),
            file_name="agent_bean_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Optional metrics per agent
        st.subheader("📊 Agent Totals Summary")
        for row in results:
            st.metric(label=f"{row['Agent']}", value=f"{row['Total Beans']:.2f} Beans")
