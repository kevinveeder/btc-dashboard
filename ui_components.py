"""
UI Components Module
Handles all Streamlit UI styling and component rendering

Functions:
- apply_custom_css(): Apply Bitcoin-themed CSS styling
- render_page_header(): Render the dashboard title and description
- render_input_section(): Render user input fields
- render_results_section(): Render calculation results and metrics
- render_footer(): Render footer with disclaimers
"""

import streamlit as st
from datetime import datetime
from config import (
    PAGE_TITLE,
    PAGE_ICON,
    PAGE_LAYOUT,
    MIN_YEAR,
    CURRENT_YEAR,
    MAX_YEAR,
    MIN_BTC_AMOUNT,
    MAX_BTC_AMOUNT,
    DEFAULT_BTC_AMOUNT,
    BTC_DECIMAL_PLACES,
    PROJECTION_DISCLAIMER,
    FOOTER_TEXT,
    BITCOIN_ORANGE,
    MAIN_BG_COLOR,
    SECONDARY_TEXT_COLOR,
    BUTTON_HOVER_COLOR,
    INFO_BOX_BG_COLOR
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

def configure_page():
    """
    Configure Streamlit page settings

    Sets page title, icon, and layout mode.
    Should be called once at the start of the app.
    """
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT
    )


# ============================================================================
# CUSTOM STYLING
# ============================================================================

def apply_custom_css():
    """
    Apply custom CSS for Bitcoin orange theme and minimalistic design

    This function injects custom CSS to style the Streamlit app with:
    - Bitcoin orange (#F7931A) for primary elements
    - Clean white background
    - Minimalistic design with subtle borders and hover effects
    """
    st.markdown(f"""
        <style>
        /* ===== MAIN BACKGROUND ===== */
        .stApp {{
            background-color: {MAIN_BG_COLOR};
        }}

        /* ===== HEADERS ===== */
        h1 {{
            color: {BITCOIN_ORANGE} !important;
            font-weight: 600;
            text-align: center;
            margin-bottom: 0.5rem;
        }}

        h2, h3 {{
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        /* ===== ALL TEXT ELEMENTS ===== */
        .stMarkdown, p, span, label, div {{
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        /* ===== INPUT LABELS ===== */
        .stNumberInput label, .stSelectbox label, .stRadio label {{
            color: {SECONDARY_TEXT_COLOR} !important;
            font-weight: 500;
        }}

        /* ===== METRIC CONTAINERS ===== */
        [data-testid="stMetricValue"] {{
            color: {BITCOIN_ORANGE} !important;
            font-weight: 600;
        }}

        [data-testid="stMetricLabel"] {{
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        [data-testid="stMetricDelta"] {{
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        /* ===== INPUT WIDGETS ===== */
        .stNumberInput > div > div > input {{
            border-color: {BITCOIN_ORANGE};
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        .stSelectbox > div > div {{
            border-color: {BITCOIN_ORANGE};
        }}

        .stSelectbox div[data-baseweb="select"] {{
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        /* ===== BUTTONS ===== */
        .stButton > button {{
            background-color: {BITCOIN_ORANGE};
            color: white !important;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }}

        .stButton > button:hover {{
            background-color: {BUTTON_HOVER_COLOR};
        }}

        /* ===== DIVIDERS ===== */
        hr {{
            border-color: {BITCOIN_ORANGE};
            opacity: 0.3;
        }}

        /* ===== ALERT/WARNING BOXES ===== */
        .stAlert {{
            background-color: {INFO_BOX_BG_COLOR};
            border-left: 4px solid {BITCOIN_ORANGE};
        }}

        .stAlert p, .stAlert span, .stAlert div {{
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        /* ===== RADIO BUTTONS ===== */
        .stRadio > label {{
            color: {SECONDARY_TEXT_COLOR} !important;
            font-weight: 500;
        }}

        .stRadio div[role="radiogroup"] label {{
            color: {SECONDARY_TEXT_COLOR} !important;
        }}

        /* ===== REMOVE EXTRA PADDING ===== */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        </style>
        """, unsafe_allow_html=True)


# ============================================================================
# HEADER SECTION
# ============================================================================

def render_page_header():
    """
    Render the dashboard title and description

    Displays:
    - Main title with Bitcoin symbol
    - Subtitle describing the dashboard purpose
    - Horizontal divider
    """
    st.title(f"{PAGE_ICON} Bitcoin Investment Calculator")
    st.markdown("### See the power of Bitcoin's historic growth")
    st.markdown("---")


# ============================================================================
# INPUT SECTION
# ============================================================================

def render_input_section():
    """
    Render user input fields for BTC/USD amount and dates

    Returns:
        dict: Dictionary containing all user inputs:
            - 'input_type': "BTC Amount" or "USD Investment"
            - 'btc_amount': Amount of BTC (if input_type is BTC)
            - 'usd_amount': Amount of USD (if input_type is USD)
            - 'purchase_year': Purchase year
            - 'purchase_month': Purchase month
            - 'comparison_type': "Today's Value" or "Future Projection"
            - 'future_year': Future year (if applicable)
            - 'future_month': Future month (if applicable)
    """
    # Create two columns for inputs
    col1, col2 = st.columns(2)

    inputs = {}

    # LEFT COLUMN: Investment Details
    with col1:
        st.subheader("Investment Details")

        # Input type toggle (BTC or USD)
        inputs['input_type'] = st.radio(
            "Input Type",
            options=["BTC Amount", "USD Investment"],
            horizontal=True,
            help="Choose to input BTC amount or USD investment amount"
        )

        # Conditional input based on selection
        if inputs['input_type'] == "BTC Amount":
            inputs['btc_amount'] = st.number_input(
                "BTC Amount",
                min_value=MIN_BTC_AMOUNT,
                max_value=MAX_BTC_AMOUNT,
                value=DEFAULT_BTC_AMOUNT,
                step=MIN_BTC_AMOUNT,
                format=f"%.{BTC_DECIMAL_PLACES}f",
                help=f"Enter the amount of Bitcoin (minimum {MIN_BTC_AMOUNT} BTC)"
            )
            inputs['usd_amount'] = None
        else:  # USD Investment
            inputs['usd_amount'] = st.number_input(
                "USD Investment",
                min_value=1.0,
                max_value=10000000.0,
                value=1000.0,
                step=100.0,
                format="%.2f",
                help="Enter the USD amount you want to invest"
            )
            inputs['btc_amount'] = None

        # Purchase date selection
        st.write("**Purchase Date**")

        inputs['purchase_year'] = st.selectbox(
            "Year",
            options=list(range(MIN_YEAR, CURRENT_YEAR + 1)),
            index=len(list(range(MIN_YEAR, CURRENT_YEAR + 1))) - 3,  # Default to ~2 years ago
            key="purchase_year"
        )

        inputs['purchase_month'] = st.selectbox(
            "Month",
            options=list(range(1, 13)),
            format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
            index=0,  # Default to January
            key="purchase_month"
        )

    # RIGHT COLUMN: Comparison Options
    with col2:
        st.subheader("Comparison Options")

        # Comparison type selection
        inputs['comparison_type'] = st.radio(
            "Compare to:",
            options=["Today's Value", "Future Projection"],
            help="Choose whether to see current value or project future value"
        )

        # If future projection is selected, show date inputs
        if inputs['comparison_type'] == "Future Projection":
            st.write("**Target Future Date**")

            inputs['future_year'] = st.selectbox(
                "Year",
                options=list(range(CURRENT_YEAR, MAX_YEAR + 1)),
                index=min(5, MAX_YEAR - CURRENT_YEAR),  # Default to 5 years from now
                key="future_year"
            )

            inputs['future_month'] = st.selectbox(
                "Month",
                options=list(range(1, 13)),
                format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
                index=0,  # Default to January
                key="future_month"
            )
        else:
            # Set future date to None if not using projection
            inputs['future_year'] = None
            inputs['future_month'] = None

    st.markdown("---")

    return inputs


# ============================================================================
# RESULTS SECTION
# ============================================================================

def render_results_section(results_data):
    """
    Render calculation results with metrics and details

    Args:
        results_data (dict): Dictionary containing calculation results:
            - 'input_type': "BTC Amount" or "USD Investment"
            - 'btc_amount': Amount of BTC
            - 'purchase_price': Purchase price per BTC
            - 'purchase_value': Total purchase value
            - 'purchase_date': Purchase date string
            - 'current_price': Current/future price per BTC
            - 'current_value': Current/future total value
            - 'comparison_date': Comparison date string
            - 'profit_loss': Profit or loss amount
            - 'profit_loss_pct': Profit or loss percentage
            - 'is_projection': Whether this is a future projection
            - 'projection_info': Additional projection info (if applicable)
    """
    is_projection = results_data.get('is_projection', False)

    # Show disclaimer for projections
    if is_projection:
        st.warning(PROJECTION_DISCLAIMER)

    # Success message
    success_title = "### Projected Investment Results" if is_projection else "### Investment Results"
    st.success(success_title)

    # Create 3 columns for main metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric(
            "Purchase Value",
            f"${results_data['purchase_value']:,.2f}",
            results_data['purchase_date']
        )

    with metric_col2:
        value_label = "Projected Value" if is_projection else "Current Value"
        st.metric(
            value_label,
            f"${results_data['current_value']:,.2f}",
            f"{results_data['profit_loss_pct']:+.2f}%"
        )

    with metric_col3:
        profit_label = "Projected Profit" if is_projection else "Profit/Loss"
        st.metric(
            profit_label,
            f"${results_data['profit_loss']:,.2f}",
            results_data['comparison_date']
        )

    # Additional details section
    st.markdown("---")

    # Show input type and relevant details
    input_type = results_data.get('input_type', 'BTC Amount')
    if input_type == "USD Investment":
        st.write(f"**Investment Type:** USD Investment → {results_data['btc_amount']:.8f} BTC purchased")
        st.write(f"**Purchase Price:** ${results_data['purchase_price']:,.2f} per BTC")
    else:
        st.write(f"**BTC Amount:** {results_data['btc_amount']:.4f} BTC")
        st.write(f"**Purchase Price:** ${results_data['purchase_price']:,.2f} per BTC")

    price_label = "Projected Price" if is_projection else "Current Price"
    st.write(f"**{price_label} ({results_data['comparison_date']}):** ${results_data['current_price']:,.2f} per BTC")

    # Show projection model info if applicable
    if is_projection and 'projection_info' in results_data:
        st.write(f"**Projection Model:** {results_data['projection_info']}")


# ============================================================================
# FOOTER SECTION
# ============================================================================

def render_footer():
    """
    Render footer with data source and disclaimer information
    """
    st.markdown("---")
    st.markdown(FOOTER_TEXT, unsafe_allow_html=True)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def show_error(message):
    """
    Display an error message to the user

    Args:
        message (str): Error message to display
    """
    st.error(message)


def show_success(message):
    """
    Display a success message to the user

    Args:
        message (str): Success message to display
    """
    st.success(message)


def show_info(message):
    """
    Display an info message to the user

    Args:
        message (str): Info message to display
    """
    st.info(message)
