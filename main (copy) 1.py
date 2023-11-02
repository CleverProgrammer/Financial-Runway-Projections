import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


# Function to calculate runway
def calculate_runway(cash, monthly_expenses, monthly_income, cash_injection):
  net_expenses = monthly_expenses - monthly_income
  adjusted_cash = cash + cash_injection
  cash_remaining_each_month = []

  # Calculate the cash remaining at the start of each month until it runs out
  while adjusted_cash > 0:
    cash_remaining_each_month.append(adjusted_cash)
    adjusted_cash -= net_expenses

  # Calculate runway in years
  runway_years = len(cash_remaining_each_month) / 12
  return cash_remaining_each_month, runway_years


# Streamlit app
st.title('Runway Calculator for Entrepreneurs')
st.subheader('Figure out how much time you got before your money runs out...')

# User inputs
cash = st.number_input('Enter your total cash on hand:',
                       min_value=0,
                       format='%d')
monthly_expenses = st.number_input('Enter your monthly expenses:',
                                   min_value=0,
                                   format='%d')
monthly_income = st.number_input(
    'Enter your monthly additional income (if any):', min_value=0, format='%d')
cash_injection = st.number_input(
    'Enter your cash injection (e.g., from a launch):',
    min_value=0,
    format='%d')

# Calculate runway
cash_remaining, runway_years = calculate_runway(cash, monthly_expenses,
                                                monthly_income, cash_injection)

if monthly_income >= monthly_expenses:
  st.subheader("🎉 You got infinite ∞ runway.")
else:
  if cash_remaining:
    # Calculate the end date of the runway
    end_month = datetime.now().replace(day=1) + pd.DateOffset(
        months=len(cash_remaining))
    end_month_str = end_month.strftime("%b '%y")

    # Update subheader with end date and runway in years
    st.subheader(
        f"⏰ You got till {end_month_str} ({runway_years:.2f} years) to get your 💩 together"
    )

    # Create DataFrame for the bar chart
    df = pd.DataFrame({
        'Month': np.arange(1,
                           len(cash_remaining) + 1),
        'Cash Remaining': cash_remaining
    })
    st.bar_chart(df.set_index('Month'))
  else:
    st.write("You don't have a runway because your cash on hand is zero.")
