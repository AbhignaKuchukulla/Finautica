import streamlit as st
from dashboard import (
    risk_assessment_chart,
    financial_health_meter,
    cashflow_calendar_heatmap,
    budget_sunburst
)
from backend.tools.risk_assessment import RiskAssessor, RiskProfile
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Finautica Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0E1117 0%, #1E293B 100%);
    }
    .metric-card {
        background: #1E293B;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stPlotlyChart {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sample data loader
@st.cache_data
def load_sample_data():
    return pd.read_csv("backend/data/sample_data/transactions.csv")

# Initialize risk assessor
risk_assessor = RiskAssessor()

# Sidebar
with st.sidebar:
    st.title("Finautica")
    st.subheader("Profile Settings")
    
    age = st.slider("Age", 18, 80, 35)
    income = st.number_input("Annual Income ($)", 10000, 1000000, 75000)
    risk_tolerance = st.select_slider(
        "Risk Tolerance",
        options=["Conservative", "Moderate", "Aggressive"],
        value="Moderate"
    )
    
    st.subheader("Navigation")
    page = st.radio(
        "Go to",
        ["Dashboard", "Budget", "Investments", "Goals"],
        label_visibility="collapsed"
    )

# Main content
if page == "Dashboard":
    st.title("Financial Dashboard")
    
    # Load data
    transactions = load_sample_data()
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Monthly Spend", f"${transactions['amount'].sum()/12:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Savings Rate", "28%", "+3% from target")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Net Worth", "$142,500", "+8.2% YoY")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Debt/Income", "22%", "Excellent")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk assessment section
    st.header("Risk Analysis")
    
    # Create risk profile from user inputs
    risk_profile = RiskProfile(
        volatility=0.6 if risk_tolerance == "Aggressive" else 0.3,
        liquidity_needs=0.4,
        concentration=0.5,
        time_horizon=min(1.0, (80 - age)/60),
        loss_capacity=0.7 if income > 100000 else 0.4
    )
    
    risk_result = risk_assessor.calculate_risk_score(risk_profile)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.plotly_chart(
            risk_assessment_chart(
                risk_result["score"],
                risk_result["benchmarks"]
            ),
            use_container_width=True
        )
    
    with col_right:
        st.plotly_chart(
            financial_health_meter(78),
            use_container_width=True
        )
        st.metric(
            "Risk Classification",
            risk_result["classification"],
            delta=f"Score: {risk_result['score']}/100"
        )
    
    # Cashflow visualization
    st.header("Spending Patterns")
    tab1, tab2 = st.tabs(["Calendar View", "Budget Variance"])
    
    with tab1:
        st.plotly_chart(
            cashflow_calendar_heatmap(transactions),
            use_container_width=True
        )
    
    with tab2:
        sample_budget = {
            "Groceries": 15000,
            "Dining": 8000,
            "Transport": 12000,
            "Housing": 60000,
            "Utilities": 18000,
            "Entertainment": 10000
        }
        st.plotly_chart(
            budget_sunburst(transactions, sample_budget),
            use_container_width=True
        )
        # In your main Streamlit app:
from dashboard import (
    risk_assessment_chart,
    financial_health_meter,
    cashflow_calendar_heatmap,
    budget_sunburst
)

# Sample risk benchmarks
risk_benchmarks = {
    'conservative': [30, 70, 20, 40, 80],
    'moderate': [50, 50, 50, 50, 50],
    'aggressive': [80, 30, 70, 80, 30]
}

# Usage example
risk_score = 65  # Calculated from user profile
st.plotly_chart(
    risk_assessment_chart(risk_score, risk_benchmarks),
    use_container_width=True
)

health_score = 78  # Calculated from financial metrics
st.plotly_chart(
    financial_health_meter(health_score),
    use_container_width=True
)