"""
API Handler Module
Handles all API calls to fetch Bitcoin price data from CoinGecko

Functions:
- get_current_btc_price(): Fetch current BTC price
- get_historical_btc_price(): Fetch historical BTC price for a specific month/year
- get_price_for_date(): Universal function to get price for any date (past, present, or future)
"""

import requests
import streamlit as st
from datetime import datetime
from config import COINGECKO_API_BASE_URL, API_TIMEOUT
from historical_prices import get_fallback_price


# ============================================================================
# CURRENT PRICE FETCHING
# ============================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour to reduce API calls
def get_current_btc_price():
    """
    Fetch the current Bitcoin price in USD from CoinGecko API

    This function is cached for 1 hour to minimize API calls and improve performance.

    Returns:
        float: Current BTC price in USD, or None if fetch fails

    Example:
        >>> price = get_current_btc_price()
        >>> print(f"Current BTC price: ${price:,.2f}")
    """
    try:
        # Construct API endpoint for current price
        url = f"{COINGECKO_API_BASE_URL}/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        }

        # Make API request with timeout
        response = requests.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()  # Raise exception for bad status codes

        # Parse JSON response
        data = response.json()
        return data['bitcoin']['usd']

    except requests.exceptions.Timeout:
        st.error("Request timed out while fetching current BTC price. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Network error fetching current BTC price: {e}")
        return None
    except (KeyError, ValueError) as e:
        st.error(f"Error parsing BTC price data: {e}")
        return None


# ============================================================================
# HISTORICAL PRICE FETCHING
# ============================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_historical_btc_price(year, month):
    """
    Fetch historical Bitcoin price for a specific month and year

    Uses CoinGecko's market_chart endpoint with days parameter (free tier friendly).
    Fetches the price for the first day of the specified month.

    Args:
        year (int): Year of the historical price (e.g., 2015)
        month (int): Month of the historical price (1-12)

    Returns:
        float: BTC price in USD for that month, or None if unavailable

    Example:
        >>> price = get_historical_btc_price(2015, 6)  # June 2015
        >>> print(f"BTC price in June 2015: ${price:,.2f}")
    """
    try:
        # Create date for the first day of the specified month
        date_obj = datetime(year, month, 1)
        now = datetime.now()

        # Calculate days from the target date to now
        days_diff = (now - date_obj).days

        # CoinGecko free tier limits: max 365 days for detailed data
        # For dates beyond 365 days, use max available and find closest match
        if days_diff < 1:
            # For current month, use current price
            return get_current_btc_price()
        elif days_diff > 365:
            # Use 'max' for all historical data (daily granularity)
            url = f"{COINGECKO_API_BASE_URL}/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': 'max'
            }
        else:
            # Within 365 days, use exact days
            url = f"{COINGECKO_API_BASE_URL}/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days_diff
            }

        # Make API request
        response = requests.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Extract price from response
        # Response format: {'prices': [[timestamp, price], ...]}
        if 'prices' in data and len(data['prices']) > 0:
            # Convert target date to timestamp
            target_timestamp = int(date_obj.timestamp() * 1000)  # milliseconds

            # Find the closest price to the target date
            closest_price = None
            min_diff = float('inf')

            for price_point in data['prices']:
                timestamp, price = price_point
                diff = abs(timestamp - target_timestamp)
                if diff < min_diff:
                    min_diff = diff
                    closest_price = price

            return closest_price if closest_price else None
        else:
            st.warning(f"No price data available for {month}/{year}")
            return None

    except requests.exceptions.Timeout:
        st.warning(f"API timeout for {month}/{year}. Using historical reference data.")
        return get_fallback_price(year, month)
    except requests.exceptions.RequestException as e:
        # API failed, use fallback data
        st.info(f"Using historical reference data for {month}/{year}.")
        return get_fallback_price(year, month)
    except (KeyError, ValueError) as e:
        st.warning(f"Error parsing API data for {month}/{year}. Using historical reference data.")
        return get_fallback_price(year, month)


# ============================================================================
# UNIVERSAL DATE HANDLER
# ============================================================================

def get_price_for_date(year, month, is_future=False):
    """
    Universal function to get BTC price for any date (historical, current, or future)

    This function acts as a router:
    - For past/current dates: fetches real historical data
    - For future dates: delegates to forecasting module

    Args:
        year (int): Year
        month (int): Month (1-12)
        is_future (bool): If True, indicates this is a future projection

    Returns:
        tuple: (price, is_projected)
            - price (float): BTC price in USD, or None if unavailable
            - is_projected (bool): True if this is a projected price, False for historical

    Example:
        >>> price, is_proj = get_price_for_date(2020, 6)
        >>> if is_proj:
        >>>     print(f"Projected price: ${price:,.2f}")
        >>> else:
        >>>     print(f"Historical price: ${price:,.2f}")
    """
    current_date = datetime.now()
    target_date = datetime(year, month, 1)

    # Check if target date is in the past or present
    if target_date <= current_date:
        # Current month - get live price
        if year == current_date.year and month == current_date.month:
            price = get_current_btc_price()
            return (price, False)
        else:
            # Historical data
            price = get_historical_btc_price(year, month)
            return (price, False)
    else:
        # Future date - import forecasting module to avoid circular dependency
        from forecasting import calculate_future_price
        price = calculate_future_price(year, month)
        return (price, True)
