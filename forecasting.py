"""
Forecasting Module
Handles future Bitcoin price predictions using multi-anchor point interpolation

The model uses expert consensus price targets at key years (2030, 2040, 2050)
and interpolates between them using logarithmic smoothing. This prevents
unrealistic exponential extrapolation while maintaining defensible projections.

Model Features:
- Multi-anchor point interpolation (2030, 2040, 2050 targets)
- Logarithmic interpolation for smooth, realistic growth curves
- Safety cap at $22M (theoretical maximum if BTC = all global wealth)
- Accounts for diminishing returns as market matures

Functions:
- calculate_future_price(): Calculate projected BTC price for a future date
- get_growth_rate(): Calculate the growth rate for a specific time period (legacy)
- interpolate_price_between_anchors(): Core interpolation logic
"""

import numpy as np
from datetime import datetime
from config import FORECAST_ANCHORS, MAX_THEORETICAL_BTC_PRICE, TARGET_PRICE_2030


# ============================================================================
# ANCHOR POINT INTERPOLATION
# ============================================================================

def interpolate_price_between_anchors(current_price, target_year):
    """
    Interpolate BTC price using multi-anchor point model

    This function finds the two nearest anchor points (2030, 2040, 2050) that
    bracket the target year, then performs logarithmic interpolation between them.
    This creates smooth growth curves that respect expert consensus targets.

    Args:
        current_price (float): Current BTC price in USD
        target_year (int): Year to project price for

    Returns:
        float: Projected BTC price, capped at MAX_THEORETICAL_BTC_PRICE

    Example:
        >>> price = interpolate_price_between_anchors(100000, 2035)
        >>> print(f"2035 projection: ${price:,.2f}")
    """
    current_year = datetime.now().year
    current_date = datetime.now()

    # Get sorted anchor years
    anchor_years = sorted(FORECAST_ANCHORS.keys())

    # CASE 1: Target year is at or before current year
    if target_year <= current_year:
        return current_price

    # CASE 2: Target year matches an anchor point exactly
    if target_year in FORECAST_ANCHORS:
        # Still need to interpolate from current price to anchor
        years_to_target = target_year - current_year
        growth_rate = np.log(FORECAST_ANCHORS[target_year] / current_price) / years_to_target
        projected = current_price * np.exp(growth_rate * years_to_target)
        return min(projected, MAX_THEORETICAL_BTC_PRICE)

    # CASE 3: Target year is before first anchor (e.g., 2027)
    first_anchor = anchor_years[0]
    if target_year < first_anchor:
        # Interpolate from current price to first anchor
        years_to_anchor = first_anchor - current_year
        years_to_target = target_year - current_year

        growth_rate = np.log(FORECAST_ANCHORS[first_anchor] / current_price) / years_to_anchor
        projected = current_price * np.exp(growth_rate * years_to_target)
        return min(projected, MAX_THEORETICAL_BTC_PRICE)

    # CASE 4: Target year is after last anchor (e.g., 2055)
    last_anchor = anchor_years[-1]
    if target_year > last_anchor:
        # Use diminished growth rate from last two anchors
        second_last_anchor = anchor_years[-2]

        # Calculate the slower growth rate between last two anchors
        years_between = last_anchor - second_last_anchor
        price_ratio = FORECAST_ANCHORS[last_anchor] / FORECAST_ANCHORS[second_last_anchor]
        growth_rate = np.log(price_ratio) / years_between

        # Apply this slower growth rate for years beyond last anchor
        years_beyond = target_year - last_anchor
        projected = FORECAST_ANCHORS[last_anchor] * np.exp(growth_rate * years_beyond)
        return min(projected, MAX_THEORETICAL_BTC_PRICE)

    # CASE 5: Target year is between two anchors (e.g., 2035 between 2030 and 2040)
    # Find bracketing anchors
    lower_anchor = None
    upper_anchor = None

    for i in range(len(anchor_years) - 1):
        if anchor_years[i] < target_year < anchor_years[i + 1]:
            lower_anchor = anchor_years[i]
            upper_anchor = anchor_years[i + 1]
            break

    if lower_anchor and upper_anchor:
        # Logarithmic interpolation between the two anchor prices
        lower_price = FORECAST_ANCHORS[lower_anchor]
        upper_price = FORECAST_ANCHORS[upper_anchor]

        # Calculate position between anchors (0 to 1)
        total_years = upper_anchor - lower_anchor
        years_from_lower = target_year - lower_anchor
        position = years_from_lower / total_years

        # Logarithmic interpolation
        log_lower = np.log(lower_price)
        log_upper = np.log(upper_price)
        log_interpolated = log_lower + position * (log_upper - log_lower)
        projected = np.exp(log_interpolated)

        return min(projected, MAX_THEORETICAL_BTC_PRICE)

    # Fallback: should never reach here
    return current_price


# ============================================================================
# GROWTH RATE CALCULATION (LEGACY - for backward compatibility)
# ============================================================================

def get_growth_rate(current_price):
    """
    Calculate the annual growth rate needed to reach target price by 2030

    NOTE: This is a legacy function maintained for backward compatibility.
    The new model uses interpolate_price_between_anchors() instead.

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

    Uses multi-anchor point interpolation model based on expert consensus targets
    for 2030, 2040, and 2050. This approach prevents unrealistic exponential
    extrapolation while maintaining defensible long-term projections.

    Model Features:
    - Interpolates between expert consensus price targets
    - Accounts for diminishing returns as market matures
    - Applies safety cap at $22M (theoretical maximum)
    - Smooth logarithmic growth curves between anchor points

    Args:
        target_year (int): Future year for projection
        target_month (int): Future month (1-12) for projection

    Returns:
        float: Projected BTC price in USD, or None if calculation fails

    Example:
        >>> price = calculate_future_price(2035, 6)  # June 2035
        >>> print(f"Projected BTC price in June 2035: ${price:,.2f}")

    Notes:
        - Projections based on expert consensus, not guaranteed outcomes
        - Should not be used for actual investment decisions
        - Model uses FORECAST_ANCHORS from config.py (2030: $800k, 2040: $2.5M, 2050: $6M)
        - Capped at MAX_THEORETICAL_BTC_PRICE ($22M) to prevent impossible projections
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

    # Use new multi-anchor point interpolation model
    projected_price = interpolate_price_between_anchors(current_price, target_year)

    # Month-level adjustment (optional fine-tuning within the year)
    # If target month is mid-year, interpolate between current year and target year
    if target_month != 1:
        # Get price for January of target year
        jan_price = interpolate_price_between_anchors(current_price, target_year)

        # Get price for January of next year
        next_jan_price = interpolate_price_between_anchors(current_price, target_year + 1)

        # Interpolate based on month position in the year
        month_fraction = (target_month - 1) / 12.0

        # Logarithmic interpolation for the month adjustment
        log_jan = np.log(jan_price)
        log_next_jan = np.log(next_jan_price)
        log_target = log_jan + month_fraction * (log_next_jan - log_jan)

        projected_price = np.exp(log_target)

    # Add realistic volatility for future projections
    # Bitcoin is known for its volatility, so add some ups and downs
    volatility_factor = add_bitcoin_volatility(target_year, target_month, projected_price)
    projected_price *= volatility_factor

    return projected_price


# ============================================================================
# VOLATILITY MODELING
# ============================================================================

def add_bitcoin_volatility(target_year, target_month, base_price):
    """
    Add realistic Bitcoin-style volatility to projected prices

    Creates predictable but realistic volatility patterns that simulate
    Bitcoin's characteristic price movements - overall upward trend with
    significant ups and downs along the way.

    Args:
        target_year (int): Target year for projection
        target_month (int): Target month (1-12)
        base_price (float): Base projected price before volatility

    Returns:
        float: Volatility multiplier (typically 0.7 to 1.4)
    """
    # Use year and month as seed for consistent volatility patterns
    # This ensures the same date always gets the same volatility factor
    seed_value = target_year * 100 + target_month

    # Create pseudo-random but consistent volatility
    # Using sine waves with different frequencies for realistic patterns
    volatility_1 = np.sin(seed_value * 0.1) * 0.15  # Primary cycle
    volatility_2 = np.sin(seed_value * 0.23) * 0.08  # Secondary cycle
    volatility_3 = np.sin(seed_value * 0.37) * 0.05  # Tertiary cycle

    # Combine volatilities and add slight upward bias (Bitcoin tends up over time)
    total_volatility = volatility_1 + volatility_2 + volatility_3 + 0.02

    # Convert to multiplier (ranges roughly from 0.75 to 1.35)
    volatility_factor = 1.0 + total_volatility

    # Add occasional "crash" and "moon" events (rare but realistic)
    crash_seed = (target_year * 17 + target_month * 7) % 100
    if crash_seed < 3:  # 3% chance of significant dip
        volatility_factor *= 0.6  # 40% crash
    elif crash_seed > 96:  # 3% chance of significant pump
        volatility_factor *= 1.8  # 80% pump

    # Ensure reasonable bounds (never more than 50% down or 100% up from base)
    return max(0.5, min(2.0, volatility_factor))


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_projection_info(current_price):
    """
    Get information about the projection model for display purposes

    Returns information about the multi-anchor point interpolation model,
    including growth rates to various anchor points and model methodology.

    Args:
        current_price (float): Current BTC price in USD

    Returns:
        dict: Dictionary containing projection model information
            - 'model_type': Description of forecasting methodology
            - 'anchor_points': Dictionary of year -> target price
            - 'growth_rate_to_2030': Annual growth rate to 2030 target (decimal)
            - 'growth_rate_to_2030_pct': Annual growth rate to 2030 (percentage)
            - 'max_cap': Maximum theoretical BTC price cap
            - 'years_to_2030': Years until 2030

    Example:
        >>> info = get_projection_info(112000)
        >>> print(f"Model uses {info['model_type']}")
        >>> print(f"2030 target: ${info['anchor_points'][2030]:,}")
    """
    current_date = datetime.now()
    target_date_2030 = datetime(2030, 1, 1)
    years_to_2030 = max((target_date_2030 - current_date).days / 365.25, 0)

    # Calculate growth rate to 2030 for reference
    if years_to_2030 > 0:
        growth_rate_2030 = np.log(TARGET_PRICE_2030 / current_price) / years_to_2030
    else:
        growth_rate_2030 = 0

    return {
        'model_type': 'Multi-anchor point interpolation with logarithmic smoothing',
        'anchor_points': FORECAST_ANCHORS.copy(),
        'growth_rate_to_2030': growth_rate_2030,
        'growth_rate_to_2030_pct': growth_rate_2030 * 100,
        'max_cap': MAX_THEORETICAL_BTC_PRICE,
        'years_to_2030': years_to_2030,
        'methodology': 'Expert consensus targets with diminishing returns'
    }


def get_model_description():
    """
    Get a human-readable description of the forecasting model

    Returns:
        str: Multi-line description of the model for UI display

    Example:
        >>> desc = get_model_description()
        >>> print(desc)
    """
    return f"""
**Forecasting Methodology:**

This model uses expert consensus price targets at key years:
- 2030: ${FORECAST_ANCHORS[2030]:,}
- 2040: ${FORECAST_ANCHORS[2040]:,}
- 2050: ${FORECAST_ANCHORS[2050]:,}

The model interpolates between these anchor points using logarithmic smoothing,
which accounts for diminishing returns as the market matures. A safety cap at
${MAX_THEORETICAL_BTC_PRICE:,} prevents physically impossible projections.

This approach is more realistic than simple exponential extrapolation and aligns
with crypto analyst consensus while remaining appropriately conservative.
""".strip()
