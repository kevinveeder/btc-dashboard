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

    Uses CoinGecko's market_chart/range endpoint to get historical price data.
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
        date_str = f"{year}-{month:02d}-01"
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Convert to Unix timestamp (required by CoinGecko API)
        timestamp_start = int(date_obj.timestamp())
        timestamp_end = timestamp_start + 86400  # Add 24 hours (1 day in seconds)

        # Construct API endpoint for historical data
        url = f"{COINGECKO_API_BASE_URL}/coins/bitcoin/market_chart/range"
        params = {
            'vs_currency': 'usd',
            'from': timestamp_start,
            'to': timestamp_end
        }

        # Make API request
        response = requests.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Extract price from response
        # Response format: {'prices': [[timestamp, price], ...]}
        if 'prices' in data and len(data['prices']) > 0:
            return data['prices'][0][1]  # Return first price in the range
        else:
            st.warning(f"No price data available for {month}/{year}")
            return None

    except requests.exceptions.Timeout:
        st.error(f"Request timed out while fetching price for {month}/{year}. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Network error fetching historical price: {e}")
        return None
    except (KeyError, ValueError) as e:
        st.error(f"Error parsing historical price data: {e}")
        return None


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
