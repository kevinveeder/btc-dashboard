"""
Forecasting Module
Handles future Bitcoin price predictions using exponential growth model

The model is calibrated to reach approximately $800k by 2030 based on
historical growth trends.

Functions:
- calculate_future_price(): Calculate projected BTC price for a future date
- get_growth_rate(): Calculate the growth rate needed to reach target price
"""

import numpy as np
from datetime import datetime
from config import TARGET_PRICE_2030


# ============================================================================
# GROWTH RATE CALCULATION
# ============================================================================

def get_growth_rate(current_price):
    """
    Calculate the annual growth rate needed to reach target price by 2030

    Uses exponential growth formula: future_price = current_price * e^(growth_rate * years)
    Solves for growth_rate: ln(future_price / current_price) / years

    Args:
        current_price (float): Current BTC price in USD

    Returns:
        float: Annual growth rate (as a decimal, not percentage)

    Example:
        >>> current_price = 50000
        >>> rate = get_growth_rate(current_price)
        >>> print(f"Annual growth rate: {rate*100:.2f}%")
    """
    current_date = datetime.now()
    target_date_2030 = datetime(2030, 1, 1)

    # Calculate years from now until 2030
    years_to_2030 = (target_date_2030 - current_date).days / 365.25

    # Handle edge case: if we're past 2030, use a smaller time window
    if years_to_2030 <= 0:
        years_to_2030 = 1  # Use 1 year as minimum

    # Calculate growth rate using natural logarithm
    # Formula: growth_rate = ln(target_price / current_price) / years
    growth_rate = np.log(TARGET_PRICE_2030 / current_price) / years_to_2030

    return growth_rate


# ============================================================================
# FUTURE PRICE PROJECTION
# ============================================================================

def calculate_future_price(target_year, target_month):
    """
    Calculate projected Bitcoin price for a future date

    Uses exponential growth model calibrated to reach TARGET_PRICE_2030 by 2030.
    Formula: projected_price = current_price * e^(growth_rate * years_from_now)

    Args:
        target_year (int): Future year for projection
        target_month (int): Future month (1-12) for projection

    Returns:
        float: Projected BTC price in USD, or None if calculation fails

    Example:
        >>> price = calculate_future_price(2028, 6)  # June 2028
        >>> print(f"Projected BTC price in June 2028: ${price:,.2f}")

    Notes:
        - This is a simple exponential model and should not be used for actual investment decisions
        - The projection assumes consistent exponential growth, which may not reflect reality
        - Model is calibrated based on TARGET_PRICE_2030 from config.py
    """
    # Import here to avoid circular dependency
    from api_handler import get_current_btc_price

    # Get current BTC price as baseline for projection
    current_price = get_current_btc_price()

    if current_price is None:
        return None

    # Calculate time difference from now to target date
    current_date = datetime.now()
    target_date = datetime(target_year, target_month, 1)
    years_diff = (target_date - current_date).days / 365.25

    # Handle edge case: if target date is in the past, return None
    if years_diff < 0:
        return None

    # Get the growth rate calibrated to reach target price by 2030
    growth_rate = get_growth_rate(current_price)

    # Calculate projected price using exponential growth
    # Formula: projected_price = current_price * e^(growth_rate * years)
    projected_price = current_price * np.exp(growth_rate * years_diff)

    return projected_price


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_projection_info(current_price):
    """
    Get information about the projection model for display purposes

    Args:
        current_price (float): Current BTC price in USD

    Returns:
        dict: Dictionary containing projection model information
            - 'growth_rate': Annual growth rate (decimal)
            - 'growth_rate_pct': Annual growth rate (percentage)
            - 'target_price': Target price for 2030
            - 'years_to_target': Years until 2030

    Example:
        >>> info = get_projection_info(50000)
        >>> print(f"Model assumes {info['growth_rate_pct']:.2f}% annual growth")
    """
    growth_rate = get_growth_rate(current_price)
    current_date = datetime.now()
    target_date_2030 = datetime(2030, 1, 1)
    years_to_2030 = max((target_date_2030 - current_date).days / 365.25, 0)

    return {
        'growth_rate': growth_rate,
        'growth_rate_pct': growth_rate * 100,
        'target_price': TARGET_PRICE_2030,
        'years_to_target': years_to_2030
    }
