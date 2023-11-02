import streamlit as st
import pandas as pd
import numpy as np


# Function to calculate runway
def calculate_runway(cash, monthly_expenses, monthly_income, cash_injection):
  net_expenses = monthly_expenses - monthly_income
  adjusted_cash = cash + cash_injection
  cash_remaining_each_month = []

  # Calculate the cash remaining at the start of each month until it runs out
  while adjusted_cash > 0:
    cash_remaining_each_month.append(adjusted_cash)
    adjusted_cash -= net_expenses

  return cash_remaining_each_month


# Streamlit app
st.title('Financial Runway Cash Remaining Bar Graph')

# User inputs
cash = st.number_input('Enter your total cash on hand:', min_value=0)
monthly_expenses = st.number_input('Enter your monthly expenses:', min_value=0)
monthly_income = st.number_input(
    'Enter your monthly additional income (if any):', min_value=0)
cash_injection = st.number_input(
    'Enter your cash injection (e.g., from a launch):', min_value=0)

if monthly_expenses <= monthly_income:
  st.error(
      'Monthly expenses must be greater than monthly income to calculate the runway.'
  )
else:
  # Calculate runway
  cash_remaining = calculate_runway(cash, monthly_expenses, monthly_income,
                                    cash_injection)

  # Check if we have any cash remaining to plot
  if cash_remaining:
    # Create DataFrame for the bar chart
    df = pd.DataFrame({
        'Month': np.arange(1,
                           len(cash_remaining) + 1),
        'Cash Remaining': cash_remaining
    })
    st.bar_chart(df.set_index('Month'))
  else:
    st.write("You don't have a runway because your cash on hand is zero.")
