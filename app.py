import streamlit as st

# ---------------------------
# SET PAGE CONFIGURATION
# ---------------------------
st.set_page_config(
    page_title="New Tax Regime Calculator",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------
# CUSTOM CSS FOR BETTER DESIGN
# ---------------------------
custom_css = """
<style>
/* Center title and add spacing */
.main .block-container{
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Style for the calculation button */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    padding: 0.8em 1.2em;
    border: none;
    border-radius: 8px;
    font-size: 1.1em;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #45a049;
}

/* Style the sidebar header */
[data-testid="stSidebar"] .css-1d391kg {
    font-size: 1.1em;
    font-weight: 600;
}

/* Custom markdown styling */
.markdown-text {
    font-size: 1.05em;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------
# INTRODUCTION
# ---------------------------
st.title("New Tax Regime Calculator")
st.markdown(
    """
    This app calculates your income tax under the new tax regime in India.
    
    **Key features of the new regime:**
    - **Nil tax** for annual incomes up to **₹12,00,000** (for non-salaried) 
      and **₹12,75,000** (for salaried taxpayers with a standard deduction of ₹75,000).
    - **Progressive tax slabs** apply on income exceeding the nil tax limit.
    
    Enter your annual income below and select whether you are salaried to see:
    - The tax you need to pay, and
    - The money you take home after tax.
    """
)

# ---------------------------
# TAX CALCULATION FUNCTIONS
# ---------------------------
def compute_tax(income: float, is_salaried: bool) -> float:
    """
    Compute tax based on a simplified version of the new tax regime.
    
    For non-salaried taxpayers:
      - Income up to ₹12,00,000: 0%
      - ₹12,00,001 - ₹15,00,000: 10%
      - ₹15,00,001 - ₹18,00,000: 15%
      - ₹18,00,001 - ₹21,00,000: 20%
      - ₹21,00,001 - ₹24,00,000: 25%
      - Above ₹24,00,000: 30%
      
    For salaried taxpayers (accounting for a standard deduction of ₹75,000):
      - Income up to ₹12,75,000: 0%
      - ₹12,75,001 - ₹15,75,000: 10%
      - ₹15,75,001 - ₹18,75,000: 15%
      - ₹18,75,001 - ₹21,75,000: 20%
      - ₹21,75,001 - ₹24,75,000: 25%
      - Above ₹24,75,000: 30%
      
    You can adjust the slabs and rates as required.
    """
    if is_salaried:
        exemption_limit = 12_75_000
        slabs = [
            (15_75_000, 0.10),
            (18_75_000, 0.15),
            (21_75_000, 0.20),
            (24_75_000, 0.25),
            (float('inf'), 0.30)
        ]
    else:
        exemption_limit = 12_00_000
        slabs = [
            (15_00_000, 0.10),
            (18_00_000, 0.15),
            (21_00_000, 0.20),
            (24_00_000, 0.25),
            (float('inf'), 0.30)
        ]
        
    # If income is within the nil tax limit, tax is zero.
    if income <= exemption_limit:
        return 0.0

    tax = 0.0
    taxable_income = income - exemption_limit
    previous_limit = exemption_limit

    for upper_limit, rate in slabs:
        # Calculate the slab range
        slab_range = upper_limit - previous_limit
        if taxable_income > slab_range:
            tax += slab_range * rate
            taxable_income -= slab_range
            previous_limit = upper_limit
        else:
            tax += taxable_income * rate
            taxable_income = 0
            break

    return tax

# ---------------------------
# USER INPUT IN SIDEBAR
# ---------------------------
st.sidebar.header("Your Details")

# Toggle for salaried or not
is_salaried = st.sidebar.radio(
    "Are you a salaried taxpayer?",
    ("Yes", "No")
) == "Yes"

# Income input (in rupees)
income = st.sidebar.number_input(
    "Enter your annual income (in ₹)",
    min_value=0.0,
    format="%.2f",
    step=10000.0,
    value=15_00_000.0,
)

# ---------------------------
# MAIN SECTION: CALCULATION & RESULT
# ---------------------------
if st.button("Calculate Tax"):
    tax_amount = compute_tax(income, is_salaried)
    take_home = income - tax_amount

    # Display the results in a nicely formatted way.
    st.markdown("### Calculation Results")
    st.markdown(
        f"""
        - **Total Annual Income:** ₹{income:,.2f}
        - **Tax Payable:** ₹{tax_amount:,.2f}
        - **Take Home Income:** ₹{take_home:,.2f}
        """
    )

    # Additional info for clarity.
    if is_salaried:
        st.info("Since you are salaried, your nil-tax limit is ₹12,75,000 (after a standard deduction of ₹75,000).")
    else:
        st.info("Since you are not salaried, your nil-tax limit is ₹12,00,000.")
else:
    st.markdown(
        """
        Enter your details from the sidebar and click **Calculate Tax** to see your results.
        """
    )
