import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_emi(principal, interest_rate, tenure_months):
    """Calculates the EMI based on loan amount, interest rate, and tenure."""
    interest_rate1 = (interest_rate/12) / 100  # Convert to decimal
    emi = principal * (interest_rate1 * pow(1 + interest_rate1, tenure_months)) / (pow(1 + interest_rate1, tenure_months) - 1)
    return emi

def is_numeric(value):
    """Check if a value is numeric."""
    try:
        float(value)
        return True 
    except ValueError:
        return False

def emi_calculator(principal, interest_rate, tenure_months, top_up, months_paid, top_up_amount):
    try:
        if len(principal)>10:
            return ValueError("*******Principle must be of less than 10 figures********")
    
        elif not all(is_numeric(value) for value in [principal, interest_rate, tenure_months]):
            return ValueError("*******Please enter numeric values for principal, interest rate, and tenure *************")
    except ValueError:
        return False
    principal = float(principal)
    interest_rate = float(interest_rate)
    tenure_months = int(tenure_months)
    
    emi = calculate_emi(principal, interest_rate, tenure_months)
    
    if top_up:
        try:
            if not is_numeric(months_paid):
                return ValueError("******Please enter a numeric value for months paid**********.")
            months_paid = int(months_paid)
            if not is_numeric(top_up_amount):
                return ValueError("******Please enter a numeric value for the top-up amount******.")
        except ValueError:
            return False
        top_up_amount = float(top_up_amount)
        
        remaining_principal =  (principal * (((1 + (interest_rate/1200)) ** tenure_months) -((1+(interest_rate/1200))** months_paid))/(((1+(interest_rate/1200))**tenure_months)-1))- top_up_amount
        new_emi = calculate_emi(remaining_principal, interest_rate, tenure_months - months_paid)
        st.write("outstanding balance : ",round(remaining_principal,2))
        return round(new_emi, 2)
    
    
    return round(emi, 2)

def plot_pie_chart(principal, emi, tenure_months):
    total_amount = emi * tenure_months
    total_interest = emi * tenure_months - principal
    principal_percentage = (principal / total_amount) * 100
    interest_percentage = (total_interest / total_amount) * 100
    principal_amount = round(principal + (total_amount * (principal_percentage / 100)), 2)
    interest_amount = round(total_interest + (total_amount * (interest_percentage / 100)), 2)
    chart_data = [dict(labels=["Principal", "Interest"], values=[principal_amount, interest_amount], text=["Principal", "Interest"], hoverinfo='label+percent', hole=.4, type='pie'),]
    st.sidebar.plotly_chart(px.bar(dict(data=chart_data)), use_container_width=True)

def main():
    st.set_page_config(page_title="EMI Calculator",layout="wide")
    st.title("EMI Calculator")
    
    principal = st.text_input("Principal:")
    interest_rate = st.text_input("Interest Rate (%):")
    tenure_months = st.text_input("Tenure (months):")