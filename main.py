import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


# Function to calculate runway and format the message
def calculate_runway_and_format(cash, monthly_expenses, monthly_income,
                                cash_injection):
  net_expenses = monthly_expenses - monthly_income
  if net_expenses <= 0:  # This means the cash will never run out because income >= expenses
    return [], "infinite", ""

  months_until_run_out = (cash + cash_injection) // net_expenses
  cash_remaining_each_month = [(cash + cash_injection) - net_expenses * month
                               for month in range(months_until_run_out)]

  end_date = datetime.now() + pd.DateOffset(months=months_until_run_out)
  end_date_str = end_date.strftime("%b %Y")

  years, months = divmod(months_until_run_out, 12)
  if years > 0 and months > 0:
    runway_formatted = f"{years} yr {months} mos"
  elif years > 0:
    runway_formatted = f"{years} yr"
  else:
    runway_formatted = f"{months} mos"

  return cash_remaining_each_month, runway_formatted, end_date_str


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
if monthly_income >= monthly_expenses:
  st.subheader("🎉 You got infinite ∞ runway.")
  cash_remaining, runway_formatted, end_date_str = [], "infinite", ""
else:
  cash_remaining, runway_formatted, end_date_str = calculate_runway_and_format(
      cash, monthly_expenses, monthly_income, cash_injection)
  if cash_remaining:
    # Update subheader with runway formatted in the most appropriate unit
    st.subheader(
        f"⏰ You got till {end_date_str} ({runway_formatted}) to get your 💩 together"
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
