import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def calculate_old_regime(salary, deductions=0):
    # Standard deduction
    std_deduction = 50000
    
    # Calculate taxable income
    taxable_income = salary - std_deduction - deductions
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
    
    return taxable_income, tax, cess, total_tax

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

def main():
    st.set_page_config(layout="wide", page_title="Indian Tax Calculator 2024")
    
    # Title and Introduction
    st.title("🇮🇳 Indian Income Tax Calculator 2024")
    st.markdown("---")
    
    # Create two columns for the layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Tax Calculator")
        
        # Input fields
        salary = st.number_input("Enter Annual Salary (₹)", min_value=0, value=1000000, step=50000)
        deductions = st.number_input("Enter Total Deductions (for Old Regime)", min_value=0, value=150000, step=10000)
        
        # Calculate taxes for both regimes
        old_taxable, old_tax, old_cess, old_total = calculate_old_regime(salary, deductions)
        new_taxable, new_tax, new_cess, new_total = calculate_new_regime(salary)
        
        # Display results in a nice format
        st.markdown("### 📈 Comparison Results")
        
        col_results1, col_results2 = st.columns(2)
        
        with col_results1:
            st.markdown("#### Old Regime")
            st.info(f"""
            Gross Salary: ₹{salary:,}
            Standard Deduction: ₹50,000
            Additional Deductions: ₹{deductions:,}
            Taxable Income: ₹{old_taxable:,}
            Base Tax: ₹{old_tax:,}
            Health & Education Cess: ₹{old_cess:,}
            **Total Tax: ₹{old_total:,}**
            """)
            
        with col_results2:
            st.markdown("#### New Regime")
            st.success(f"""
            Gross Salary: ₹{salary:,}
            Standard Deduction: ₹75,000
            Additional Deductions: N/A
            Taxable Income: ₹{new_taxable:,}
            Base Tax: ₹{new_tax:,}
            Health & Education Cess: ₹{new_cess:,}
            **Total Tax: ₹{new_total:,}**
            """)
        
        # Create comparison chart
        comparison_data = {
            'Regime': ['Old Regime', 'New Regime'],
            'Tax Amount': [old_total, new_total]
        }
        fig = px.bar(comparison_data, x='Regime', y='Tax Amount',
                    title='Tax Comparison',
                    color='Regime',
                    color_discrete_map={'Old Regime': '#ff9999', 'New Regime': '#99ff99'})
        st.plotly_chart(fig)
        
        # Show savings
        savings = abs(old_total - new_total)
        better_regime = "New Regime" if new_total < old_total else "Old Regime"
        st.markdown(f"### 💰 Potential Savings")
        st.markdown(f"**{better_regime}** is better for you by **₹{savings:,}**")
        
    with col2:
        st.subheader("ℹ️ About Tax Regimes")
        
        # Tax regime explanations
        with st.expander("Old Tax Regime"):
            st.markdown("""
            ### Old Tax Regime Features:
            - Standard Deduction: ₹50,000
            - Allows various deductions and exemptions
            
            #### Tax Slabs:
            - 0 to 2.5L: No tax
            - 2.5L to 5L: 5%
            - 5L to 10L: 20%
            - Above 10L: 30%
            
            #### Available Deductions:
            - Section 80C (up to ₹1.5L)
            - HRA
            - Home Loan Interest
            - NPS
            - Medical Insurance
            - And many more...
            """)
            
        with st.expander("New Tax Regime"):
            st.markdown("""
            ### New Tax Regime Features:
            - Standard Deduction: ₹75,000
            - No additional deductions
            - More tax slabs for gradual increase
            
            #### Tax Slabs:
            - 0 to 4L: No tax
            - 4L to 8L: 5%
            - 8L to 12L: 10%
            - 12L to 16L: 15%
            - 16L to 20L: 20%
            - 20L to 24L: 25%
            - Above 24L: 30%
            
            #### Benefits:
            - Simplified tax calculation
            - Higher standard deduction
            - More tax slabs for smoother progression
            - Better for those with fewer investments
            """)
            
        with st.expander("Which Regime is better "):
            st.markdown("""
      
            
            👉Old Regime is better if :
            - You have significant investments
            - You pay home loan EMI
            - You can claim deductions > ₹8L
            - You have multiple income sources
            
            👉New Regime is Better if:
            - You prefer simplicity
            - You don't have many investments
            - Your salary is below ₹15L
            - You're starting your career
            
        
            """)

if __name__ == "__main__":
    main()
