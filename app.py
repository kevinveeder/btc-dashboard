"""
Bitcoin Investment Dashboard - Main Application
A minimalistic dashboard to calculate historical and projected Bitcoin values

This is the main entry point for the Streamlit application.
Run with: streamlit run app.py

Author: Built with Claude Code
"""

from datetime import datetime
from config import TARGET_PRICE_2030, FORECAST_ANCHORS
from api_handler import get_price_for_date, get_current_btc_price
from forecasting import calculate_future_price, get_model_description
from visualization import generate_price_history_chart
from ui_components import (
    configure_page,
    apply_custom_css,
    render_page_header,
    render_input_section,
    render_results_section,
    render_footer,
    show_error
)
import streamlit as st


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """
    Main application function

    This function orchestrates the entire dashboard:
    1. Configures the page and applies styling
    2. Renders the UI components
    3. Handles user interactions and calculations
    4. Displays results and charts
    """

    # Configure page settings (must be called first)
    configure_page()

    # Apply custom CSS styling
    apply_custom_css()

    # Render page header
    render_page_header()

    # Render input section and get user inputs
    inputs = render_input_section()

    # Create calculate button
    if st.button("Calculate Value", type="primary", use_container_width=True):
        calculate_and_display_results(inputs)

    # Render footer
    render_footer()


# ============================================================================
# CALCULATION AND DISPLAY LOGIC
# ============================================================================

def calculate_and_display_results(inputs):
    """
    Calculate investment results and display them to the user

    This function:
    1. Fetches the purchase price for the selected date
    2. Fetches the comparison price (current or future)
    3. Calculates profit/loss metrics
    4. Displays results using metric cards
    5. Generates and displays a price history chart

    Args:
        inputs (dict): User input data from render_input_section()
    """

    # Extract inputs
    input_type = inputs['input_type']
    purchase_year = inputs['purchase_year']
    purchase_month = inputs['purchase_month']
    comparison_type = inputs['comparison_type']
    future_year = inputs.get('future_year')
    future_month = inputs.get('future_month')

    # ========== STEP 1: Get purchase price ==========
    purchase_price, _ = get_price_for_date(purchase_year, purchase_month)

    if purchase_price is None:
        show_error(
            f"Unable to fetch Bitcoin price for "
            f"{datetime(2000, purchase_month, 1).strftime('%B')} {purchase_year}. "
            f"Please try a different date."
        )
        return

    # ========== STEP 2: Calculate BTC amount and purchase value based on input type ==========
    if input_type == "BTC Amount":
        # User entered BTC directly
        btc_amount = inputs['btc_amount']
        purchase_value = btc_amount * purchase_price
    else:  # USD Investment
        # User entered USD, calculate how much BTC they could buy
        usd_amount = inputs['usd_amount']
        btc_amount = usd_amount / purchase_price
        purchase_value = usd_amount

    # ========== STEP 3: Get comparison price ==========
    if comparison_type == "Today's Value":
        # Get current price
        current_price = get_current_btc_price()

        if current_price is None:
            show_error("Unable to fetch current Bitcoin price. Please try again.")
            return

        # Set comparison values
        comparison_price = current_price
        is_projection = False
        comparison_year = datetime.now().year
        comparison_month = datetime.now().month

    else:  # Future Projection
        # Get projected price
        projected_price = calculate_future_price(future_year, future_month)

        if projected_price is None:
            show_error("Unable to calculate future projection. Please try again.")
            return

        # Set comparison values
        comparison_price = projected_price
        is_projection = True
        comparison_year = future_year
        comparison_month = future_month

    # ========== STEP 4: Calculate metrics ==========
    current_value = btc_amount * comparison_price
    profit_loss = current_value - purchase_value
    profit_loss_pct = ((current_value - purchase_value) / purchase_value) * 100

    # ========== STEP 5: Prepare results data ==========
    results_data = {
        'input_type': input_type,
        'btc_amount': btc_amount,
        'purchase_price': purchase_price,
        'purchase_value': purchase_value,
        'purchase_date': f"{datetime(2000, purchase_month, 1).strftime('%b')} {purchase_year}",
        'current_price': comparison_price,
        'current_value': current_value,
        'comparison_date': f"{datetime(2000, comparison_month, 1).strftime('%b')} {comparison_year}",
        'profit_loss': profit_loss,
        'profit_loss_pct': profit_loss_pct,
        'is_projection': is_projection
    }

    # Add projection info if applicable
    if is_projection:
        # Use the new model description with anchor points
        anchor_str = ", ".join([f"{year}: ${price:,}" for year, price in sorted(FORECAST_ANCHORS.items())])
        results_data['projection_info'] = f"Multi-anchor interpolation model (Targets: {anchor_str})"
        results_data['model_details'] = get_model_description()

    # ========== STEP 6: Display results ==========
    render_results_section(results_data)

    # ========== STEP 7: Generate and display chart ==========
    st.markdown("---")

    # Show loading spinner while generating chart
    with st.spinner("Generating price chart..."):
        chart = generate_price_history_chart(
            purchase_year,
            purchase_month,
            comparison_year,
            comparison_month,
            btc_amount
        )

    # Display chart
    st.plotly_chart(chart, use_container_width=True)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Application entry point

    When this script is run directly (e.g., `streamlit run app.py`),
    the main() function is called to start the dashboard.
    """
    main()
