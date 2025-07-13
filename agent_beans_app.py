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


#!/usr/bin/env python3


import math
from typing import Dict, Optional
from dataclasses import dataclass
import streamlit as st

@dataclass
class ConversionTier:
    min_beans: int
    max_beans: float
    diamonds_per_bean: float
    efficiency: float
    fixed_diamonds: Optional[int] = None

class BeansToDiamondsCalculator:
    def __init__(self):
        self.conversion_tiers = [
            ConversionTier(1, 8, 0.25, 25.00, 2),
            ConversionTier(9, 109, 0.2661, 26.61, 29),
            ConversionTier(110, 999, 0.2753, 27.53, 275),
            ConversionTier(1000, 3999, 0.2763, 27.63, 1105),
            ConversionTier(4000, 10999, 0.2768, 27.68, 3045),
            ConversionTier(11000, float('inf'), 0.2767, 27.67, None)
        ]

    def find_tier(self, beans: int) -> Optional[ConversionTier]:
        for tier in self.conversion_tiers:
            if tier.min_beans <= beans <= tier.max_beans:
                return tier
        return None

    def calculate_diamonds(self, beans: int) -> Optional[Dict]:
        if not beans or beans <= 0:
            return None

        tier = self.find_tier(beans)
        if not tier:
            return None

        if tier.fixed_diamonds and beans == tier.max_beans:
            diamonds = tier.fixed_diamonds
        else:
            diamonds = math.floor(beans * tier.diamonds_per_bean)

        remainder = beans % math.ceil(1 / tier.diamonds_per_bean)
        tier_number = self.conversion_tiers.index(tier) + 1

        return {
            'diamonds': diamonds,
            'remainder': remainder,
            'efficiency': tier.efficiency,
            'diamonds_per_bean': tier.diamonds_per_bean,
            'tier': tier_number
        }

    def optimize_beans(self, beans: int):
        breakdown = []
        total_diamonds = 0
        remaining_beans = beans

        for tier in reversed(self.conversion_tiers):
            if remaining_beans >= tier.min_beans:
                # Fix: handle infinite max_beans
                max_beans = tier.max_beans if tier.max_beans != float('inf') else remaining_beans
                beans_in_tier = min(remaining_beans, int(max_beans))
                if tier.fixed_diamonds and beans_in_tier == tier.max_beans:
                    diamonds = tier.fixed_diamonds
                else:
                    diamonds = math.floor(beans_in_tier * tier.diamonds_per_bean)
                breakdown.append({
                    'tier': self.conversion_tiers.index(tier) + 1,
                    'beans': beans_in_tier,
                    'diamonds': diamonds,
                    'rate': tier.diamonds_per_bean,
                    'efficiency': tier.efficiency
                })
                total_diamonds += diamonds
                remaining_beans -= beans_in_tier

        # If any beans remain, process them in the lowest tier
        if remaining_beans > 0:
            tier = self.conversion_tiers[0]
            diamonds = math.floor(remaining_beans * tier.diamonds_per_bean)
            breakdown.append({
                'tier': 1,
                'beans': remaining_beans,
                'diamonds': diamonds,
                'rate': tier.diamonds_per_bean,
                'efficiency': tier.efficiency
            })
            total_diamonds += diamonds

        breakdown = sorted(breakdown, key=lambda x: x['tier'])
        return breakdown, total_diamonds

    def get_efficiency_tip(self, beans: int) -> str:
        if beans < 109:
            return "💡 Tip: Efficiency increases significantly after 109 beans!"
        elif beans < 4000:
            return "💡 Tip: Maximum efficiency is reached at 4000+ beans!"
        else:
            return "💡 Great! You're at maximum efficiency tier!"

    def get_tier_table(self):
        rows = []
        for tier in self.conversion_tiers:
            max_beans_str = "∞" if tier.max_beans == float('inf') else f"{int(tier.max_beans):,}"
            range_str = f"{tier.min_beans:,} - {max_beans_str}"
            rate = f"{tier.diamonds_per_bean:.4f}"
            efficiency = f"{tier.efficiency:.2f}%"
            if tier.fixed_diamonds and tier.max_beans < float('inf'):
                example = f"{int(tier.max_beans):,} beans = {tier.fixed_diamonds} diamonds"
            else:
                example = efficiency
            rows.append((range_str, rate, efficiency, example))
        return rows

def main():
    st.set_page_config(page_title="Beans to Diamonds Calculator", page_icon="💎")

    st.title("💎 Beans to Diamonds Calculator")
    st.caption("Convert your beans to diamonds with tier-based efficiency rates")

    calculator = BeansToDiamondsCalculator()

    beans = st.number_input("Enter number of beans", min_value=1, step=1)

    if st.button("Calculate"):
        result = calculator.calculate_diamonds(beans)

        if result:
            st.success("✅ Conversion Result")
            st.metric("Diamonds", result['diamonds'])
            st.metric("Efficiency", f"{result['efficiency']}%")
            st.metric("Rate", f"{result['diamonds_per_bean']:.4f} per bean")
            if result['remainder'] > 0:
                st.info(f"Beans remainder: {result['remainder']} (may not convert)")
            st.info(f"Tier: {result['tier']}")
            st.markdown(f"**{calculator.get_efficiency_tip(beans)}**")

            # Optimization breakdown
            st.subheader("🔎 Optimized Conversion Breakdown")
            breakdown, total_diamonds = calculator.optimize_beans(beans)
            st.write(f"**Total Diamonds (Optimized): {total_diamonds}**")
            st.table({
                "Tier": [b['tier'] for b in breakdown],
                "Beans Used": [b['beans'] for b in breakdown],
                "Diamonds Earned": [b['diamonds'] for b in breakdown],
                "Rate": [f"{b['rate']:.4f}" for b in breakdown],
                "Efficiency": [f"{b['efficiency']}%" for b in breakdown],
            })
        else:
            st.error("❌ Unable to calculate conversion.")

    with st.expander("📊 View Conversion Tier Table"):
        tier_data = calculator.get_tier_table()
        st.table(
            {
                "Beans Range": [row[0] for row in tier_data],
                "Rate": [row[1] for row in tier_data],
                "Efficiency": [row[2] for row in tier_data],
                "Example": [row[3] for row in tier_data],
            }
        )

if __name__ == "__main__":
    main()

    st.markdown(
    "<div style='text-align: center; font-size: 14px; margin-top: 32px;'>© 2025 Alpha Agency & T Star Agency. All rights reserved.</div>",
    unsafe_allow_html=True
)
