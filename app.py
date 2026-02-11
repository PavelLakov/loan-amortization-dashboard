import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize session state for chart toggle
if 'show_charts' not in st.session_state:
    st.session_state.show_charts = False

# Custom CSS for fancy styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem;
    }

    /* Title Styling */
    .st-emotion-cache-1guc3i1 h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-size: 3rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Metrics Cards */
    .stMetric > label {
        color: white !important;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stMetric > div > div {
        color: #FFD700 !important;
        font-size: 1.5rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Columns for Metrics */
    .row-widget.stHorizontalBlock > div {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Slider Styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        border-radius: 10px;
    }

    /* DataFrame Styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 12px;
    }
    .dataframe td {
        padding: 12px;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    .dataframe tr:hover {
        background: rgba(102, 126, 234, 0.1);
    }

    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #333;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    /* Button for Charts */
    .stButton > button {
        background: linear-gradient(135deg, #00BFFF, #1E90FF);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    /* Headers */
    h2, h3 {
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        padding-bottom: 0.5rem;
    }

    /* Plotly Chart Container */
    .plotly-chart {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Info Box */
    .stInfo {
        background: rgba(255, 215, 0, 0.2);
        border-radius: 10px;
        border-left: 4px solid #FFD700;
    }

    /* Success Message (if any) */
    .stSuccess {
        background: rgba(0, 255, 0, 0.1);
        border-radius: 10px;
        border-left: 4px solid #00FF00;
    }
</style>
""", unsafe_allow_html=True)

# Title of the app
st.title("Loan Calculator with Amortization Schedule and Interactive Dashboard")

# Sidebar for inputs
st.sidebar.header("Loan Parameters")
currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "CAD"], index=0)
currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "CAD": "C$"}
symbol = currency_symbols[currency]

principal = st.sidebar.number_input("Loan Amount", min_value=0.0, value=100000.0, step=1000.0)
annual_rate = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0, step=0.1) / 100
years = st.sidebar.number_input("Loan Term (Years)", min_value=1, value=30, step=1)

# Calculate monthly rate and payments
monthly_rate = annual_rate / 12
num_payments = years * 12

# Monthly payment formula
if monthly_rate == 0:
    monthly_payment = principal / num_payments
else:
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / (
                (1 + monthly_rate) ** num_payments - 1)

# Total payment and interest
total_payment = monthly_payment * num_payments
total_interest = total_payment - principal

# Display summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Monthly Payment", f"{symbol}{monthly_payment:,.2f}")
col2.metric("Total Payment", f"{symbol}{total_payment:,.2f}")
col3.metric("Total Interest", f"{symbol}{total_interest:,.2f}")
col4.metric("Loan Term", f"{years} years")

# Generate schedule (full for download and use)
schedule = []
balance = principal
for payment_num in range(1, num_payments + 1):
    interest_payment = balance * monthly_rate
    principal_payment = monthly_payment - interest_payment
    balance -= principal_payment
    if balance < 0:
        balance = 0
    schedule.append({
        'Payment #': payment_num,
        'Payment Amount': monthly_payment,
        'Interest': interest_payment,
        'Principal': principal_payment,
        'Balance': balance
    })

df = pd.DataFrame(schedule)

# Buttons in columns: Download CSV and Toggle Charts
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    csv = df.to_csv(index=False)
    st.download_button("Download Full Schedule (CSV)", csv, "amortization_schedule.csv", "text/csv")
with btn_col2:
    if st.button("Charts"):
        st.session_state.show_charts = not st.session_state.show_charts
        st.rerun()

# Amortization Schedule
st.header("Amortization Schedule")
st.dataframe(df)

# Show charts if toggled
if st.session_state.show_charts:
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Remaining Balance Over Time', 'Cumulative Interest vs Principal', 'Total Breakdown Pie',
                        'Interest vs Principal per Payment'),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "scatter"}]]
    )

    # 1. Line chart: Balance over time (full)
    cumulative_balance = df['Balance'].values
    fig.add_trace(
        go.Scatter(x=df['Payment #'], y=cumulative_balance, mode='lines', name='Balance', line=dict(color='blue')),
        row=1, col=1
    )

    # 2. Bar chart: Cumulative Interest and Principal Paid (full)
    df['Cumulative Interest'] = df['Interest'].cumsum()
    df['Cumulative Principal'] = df['Principal'].cumsum()
    fig.add_trace(
        go.Bar(x=df['Payment #'], y=df['Cumulative Interest'], name='Cum. Interest', marker_color='red'),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=df['Payment #'], y=df['Cumulative Principal'], name='Cum. Principal', marker_color='green'),
        row=1, col=2
    )

    # 3. Pie chart: Total Interest vs Principal (full)
    fig.add_trace(
        go.Pie(labels=['Total Interest', 'Total Principal'], values=[total_interest, principal], name='Breakdown'),
        row=2, col=1
    )

    # 4. Scatter: Interest vs Principal per payment (full)
    fig.add_trace(
        go.Scatter(x=df['Principal'], y=df['Interest'], mode='markers', name='Interest vs Principal',
                   marker=dict(size=3, color=df['Payment #'], colorscale='Viridis')),
        row=2, col=2
    )

    fig.update_layout(height=800, showlegend=True, title_text=f"Loan Amortization Dashboard - Currency: {currency}")
    st.plotly_chart(fig, use_container_width=True)