import streamlit as st
import pandas as pd
from io import BytesIO

# Tiered salary structure
TIERED_SALARY = [
    (6000000, 10200),
    (5000000, 9200),
    (4000000, 7650),
    (3000000, 5900),
    (2000000, 3925),
    (1500000, 2950),
    (1000000, 2000),
    (800000, 1613),
    (600000, 1220),
    (450000, 945),
    (350000, 735),
    (250000, 525),
    (170000, 361),
    (130000, 281),
    (120000, 263),
    (110000, 243),
    (100000, 221),
    (90000, 200),
    (80000, 178),
    (70000, 156),
    (60000, 134),
    (50000, 112),
    (40000, 89),
    (30000, 67),
    (20000, 45),
    (10000, 23),
    (5000, 23),
    (0, 0)
]

def get_salary_usd(beans_earned):
    for threshold, salary in TIERED_SALARY:
        if beans_earned >= threshold:
            return salary
    return 0

# Function to calculate salary in beans, commission, and total
def calculate_total_beans(beans_earned, salary_usd):
    salary_beans = salary_usd * 210
    commission = beans_earned * 0.05
    total = salary_beans + commission
    return salary_beans, commission, total

# Function to convert beans to diamonds
def convert_beans_to_diamonds(beans):
    conversions = [
        {"diamonds": 3045, "beans": 10999},
        {"diamonds": 1105, "beans": 3999},
        {"diamonds": 275,  "beans": 999},
        {"diamonds": 29,   "beans": 109},
        {"diamonds": 2,    "beans": 8}
    ]
    diamonds = 0
    breakdown = []

    for pack in conversions:
        count = beans // pack["beans"]
        if count > 0:
            diamonds += count * pack["diamonds"]
            beans -= count * pack["beans"]
            breakdown.append(f"{int(count)}×{pack['diamonds']}d")

    return diamonds, ', '.join(breakdown)

# Streamlit app configuration
st.set_page_config(page_title="Agency Commission Calculator", layout="centered")
st.title("🎯 Agency Commission Calculator")

# Form input
with st.form("bean_calc_form"):
    num_agents = st.number_input("How many Hosts?", min_value=1, step=1)
    agents_input = []

    for i in range(int(num_agents)):
        with st.expander(f"🧝 Host {i+1} Details", expanded=True):
            name = st.text_input("Name", key=f"name_{i}")
            beans_earned = st.number_input("Beans🫘 Earned by Host 🎭", min_value=0, step=100, key=f"beans_{i}")
            salary_usd = get_salary_usd(beans_earned)
            agents_input.append({
                "name": name.strip(),
                "beans_earned": beans_earned,
                "salary_usd": salary_usd
            })

    submitted = st.form_submit_button("Calculate")

# Process form data
if submitted:
    if any(agent["name"] == "" for agent in agents_input):
        st.error("🚫 Please enter a name for every Host.")
    else:
        results = []
        for agent in agents_input:
            salary_beans, commission, total = calculate_total_beans(agent["beans_earned"], agent["salary_usd"])
            diamonds, breakdown = convert_beans_to_diamonds(total)

            results.append({
                "Agent": agent["name"],
                "Beans Earned": int(agent["beans_earned"]),
                "Salary (USD)": int(agent["salary_usd"]),
                "Salary in Beans": int(salary_beans),
                "5% Commission": int(commission),
                "Total Beans": int(total),
                "Diamonds": int(diamonds),
                "Diamond Breakdown": breakdown
            })

        # Remove breakdown from main table
        df = pd.DataFrame([{k: v for k, v in r.items() if k != "Diamond Breakdown"} for r in results])
        df = df.sort_values(by="Total Beans", ascending=False)

        st.success("✅ Calculations complete!")
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}), use_container_width=True)

        # Totals
        total_all = df["Total Beans"].sum()
        total_diamonds = df["Diamonds"].sum()
        st.info(f"💰 **Total Beans Across All Hosts:** {int(total_all)}")
        st.success(f"💎 **Total Diamonds for Agency:** {total_diamonds}")

        # Excel download
        output = BytesIO()
        df.to_excel(output, index=False, sheet_name='Agent Beans')
        st.download_button(
            "📅 Download Results as Excel",
            output.getvalue(),
            file_name="agent_bean_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Per-agent breakdown
        st.subheader("📊 Agency Totals Summary")
        for row in results:
            st.metric(label=row['Agent'], value=f"{row['Total Beans']} Beans / {row['Diamonds']} Diamonds")
            st.caption(f"💎 Breakdown: {row['Diamond Breakdown']}")

st.markdown(
    "<div style='text-align: center; font-size: 14px; margin-top: 32px;'>© 2025 Alpha Agency & T Star Agency. All rights reserved.</div>",
    unsafe_allow_html=True
)
