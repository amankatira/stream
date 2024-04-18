import streamlit as st

def calculate_emi(principal, interest_rate, tenure_months):
    """Calculates the EMI based on loan amount, interest rate, and tenure."""
    interest_rate1 = interest_rate / 100  # Convert to decimal
    emi = (principal * interest_rate1 * pow(1 + interest_rate1, tenure_months)) / (pow(1 + interest_rate1, tenure_months) - 1)
    return emi

def is_numeric(value):
    """Check if a value is numeric."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def emi_calculator(principal, interest_rate, tenure_months, top_up, months_paid, top_up_amount):
    if not all(is_numeric(value) for value in [principal, interest_rate, tenure_months]):
        return "Please enter numeric values for principal, interest rate, and tenure."
    
    principal = float(principal)
    interest_rate = float(interest_rate)
    tenure_months = int(tenure_months)
    
    emi = calculate_emi(principal, interest_rate, tenure_months)
    
    if top_up:
        if not is_numeric(months_paid):
            return "Please enter a numeric value for months paid."
        months_paid = int(months_paid)
        
        if not is_numeric(top_up_amount):
            return "Please enter a numeric value for the top-up amount."
        top_up_amount = float(top_up_amount)
        
        remaining_principal = principal - (emi * months_paid) + top_up_amount
        new_emi = calculate_emi(remaining_principal, interest_rate, tenure_months - months_paid)
        return new_emi
    
    return emi

def main():
    st.title("EMI Calculator")
    
    principal = st.text_input("Principal:")
    interest_rate = st.text_input("Interest Rate (%):")
    tenure_months = st.text_input("Tenure (months):")
    
    top_up = st.checkbox("Top up loan?")
    
    if top_up:
        months_paid = st.text_input("Months Paid:")
        top_up_amount = st.text_input("Top-up Amount:")
        emi = emi_calculator(principal, interest_rate, tenure_months, True, months_paid, top_up_amount)
    else:
        emi = emi_calculator(principal, interest_rate, tenure_months, False, "", "")
    
    st.write("EMI:", emi)

if __name__ == '__main__':
    main()