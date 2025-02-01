import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def calculate_old_regime(salary):
    # Standard deduction
    std_deduction = 50000
    
    # Assuming standard deductions under 80C and others
    standard_80c = min(150000, salary * 0.15)  # Assuming 15% of salary goes to 80C investments
    standard_health_insurance = 25000  # Standard health insurance premium
    standard_deductions = standard_80c + standard_health_insurance
    
    # Calculate taxable income
    taxable_income = salary - std_deduction - standard_deductions
    if taxable_income < 0:
        taxable_income = 0
    
    # Calculate tax
    tax = 0
    if taxable_income > 250000:
        tax += min(taxable_income - 250000, 250000) * 0.05
    if taxable_income > 500000:
        tax += min(taxable_income - 500000, 500000) * 0.20
    if taxable_income > 1000000:
        tax += (taxable_income - 1000000) * 0.30
    
    # Add cess
    cess = tax * 0.04
    total_tax = tax + cess
    
    return taxable_income, standard_deductions, tax, cess, total_tax

def calculate_new_regime(salary):
    # Standard deduction
    std_deduction = 75000
    
    # Calculate taxable income
    taxable_income = salary - std_deduction
    if taxable_income < 0:
        taxable_income = 0
    
    # Calculate tax
    tax = 0
    if taxable_income > 400000:
        tax += min(taxable_income - 400000, 400000) * 0.05
    if taxable_income > 800000:
        tax += min(taxable_income - 800000, 400000) * 0.10
    if taxable_income > 1200000:
        tax += min(taxable_income - 1200000, 400000) * 0.15
    if taxable_income > 1600000:
        tax += min(taxable_income - 1600000, 400000) * 0.20
    if taxable_income > 2000000:
        tax += min(taxable_income - 2000000, 400000) * 0.25
    if taxable_income > 2400000:
        tax += (taxable_income - 2400000) * 0.30
    
    # Add cess
    cess = tax * 0.04
    total_tax = tax + cess
    
    return taxable_income, tax, cess, total_tax

def create_monthly_breakdown(total_tax):
    monthly_tax = total_tax / 12
    tds_data = {
        'Month': ['April', 'May', 'June', 'July', 'August', 'September', 
                 'October', 'November', 'December', 'January', 'February', 'March'],
        'TDS Amount': [monthly_tax] * 12
    }
    return pd.DataFrame(tds_data)

def main():
    st.set_page_config(layout="wide", page_title="Indian Tax Calculator 2024")
    
    # Title and Introduction
    st.title("🇮🇳 Indian Income Tax Calculator 2024")
    st.markdown("---")
    
    # Single input for salary
    salary = st.number_input("Enter Your Annual Salary (₹)", 
                            min_value=0, 
                            value=1000000, 
                            step=50000,
                            help="Enter your total annual salary before any deductions")
    
    # Calculate taxes for both regimes
    old_taxable, standard_deductions, old_tax, old_cess, old_total = calculate_old_regime(salary)
    new_taxable, new_tax, new_cess, new_total = calculate_new_regime(salary)
    
    # Create three columns for the layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Old Tax Regime")
        st.info(f"""
        💰 Gross Annual Salary: ₹{salary:,}
        
        Deductions Breakdown:
        - Standard Deduction: ₹50,000
        - Estimated 80C Investments: ₹{min(150000, int(salary * 0.15)):,}
        - Health Insurance Premium: ₹25,000
        
        📊 Calculations:
        - Total Deductions: ₹{standard_deductions + 50000:,}
        - Taxable Income: ₹{old_taxable:,}
        - Base Tax: ₹{old_tax:,}
        - Health & Education Cess (4%): ₹{old_cess:,}
        
        🔸 Total Annual Tax: ₹{old_total:,}
        🔸 Monthly Tax (TDS): ₹{old_total/12:,.2f}
        """)
        
    with col2:
        st.markdown("### New Tax Regime")
        st.success(f"""
        💰 Gross Annual Salary: ₹{salary:,}
        
        Deductions Breakdown:
        - Standard Deduction: ₹75,000
        - No other deductions available
        
        📊 Calculations:
        - Total Deductions: ₹75,000
        - Taxable Income: ₹{new_taxable:,}
        - Base Tax: ₹{new_tax:,}
        - Health & Education Cess (4%): ₹{new_cess:,}
        
        🔸 Total Annual Tax: ₹{new_total:,}
        🔸 Monthly Tax (TDS): ₹{new_total/12:,.2f}
        """)
    
    # Comparison Visualizations
    st.markdown("### 📊 Tax Comparison Visualization")
    
    # Create comparison chart
    fig = go.Figure(data=[
        go.Bar(name='Annual Tax', 
               x=['Old Regime', 'New Regime'],
               y=[old_total, new_total],
               text=[f'₹{old_total:,}', f'₹{new_total:,}'],
               textposition='auto',
               marker_color=['#FF9999', '#99FF99'])
    ])
    
    fig.update_layout(
        title='Tax Comparison Between Regimes',
        yaxis_title='Tax Amount (₹)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show savings and recommendation
    savings = abs(old_total - new_total)
    better_regime = "New" if new_total < old_total else "Old"
    
    st.markdown("### 💡 Recommendation")
    st.markdown(f"""
    Based on your salary of ₹{salary:,}:
    
    - The **{better_regime} Tax Regime** would be more beneficial for you
    - Potential annual savings: ₹{savings:,}
    - Monthly savings: ₹{savings/12:,.2f}
    
    """)
    
    # Monthly TDS Breakdown
    st.markdown("### 📅 Monthly TDS Breakdown")
    col_tds1, col_tds2 = st.columns(2)
    
    with col_tds1:
        st.markdown("#### Old Regime Monthly TDS")
        old_monthly_df = create_monthly_breakdown(old_total)
        st.dataframe(old_monthly_df.style.format({'TDS Amount': '₹{:,.2f}'}))
        
    with col_tds2:
        st.markdown("#### New Regime Monthly TDS")
        new_monthly_df = create_monthly_breakdown(new_total)
        st.dataframe(new_monthly_df.style.format({'TDS Amount': '₹{:,.2f}'}))

if __name__ == "__main__":
    main()
