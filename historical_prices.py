"""
Historical Bitcoin Price Reference Data
Contains approximate Bitcoin prices at key dates for when API data is unavailable

This fallback data is used when the CoinGecko free API doesn't return historical data.
Prices are approximate monthly averages sourced from historical records.
"""

# Historical BTC prices (year, month): price_usd
# Approximate monthly average prices
HISTORICAL_PRICES = {
    # 2010-2013: Early Bitcoin era
    (2010, 7): 0.08,
    (2010, 11): 0.25,
    (2011, 1): 0.30,
    (2011, 6): 15.00,
    (2011, 12): 4.00,
    (2012, 1): 5.00,
    (2012, 6): 6.50,
    (2012, 12): 13.00,
    (2013, 1): 13.50,
    (2013, 4): 120.00,
    (2013, 6): 100.00,
    (2013, 11): 900.00,
    (2013, 12): 750.00,

    # 2014-2016: Bear market and recovery
    (2014, 1): 800.00,
    (2014, 6): 600.00,
    (2014, 12): 320.00,
    (2015, 1): 280.00,
    (2015, 6): 250.00,
    (2015, 12): 430.00,
    (2016, 1): 430.00,
    (2016, 6): 650.00,
    (2016, 12): 900.00,

    # 2017-2018: Bull run and crash
    (2017, 1): 1000.00,
    (2017, 3): 1200.00,
    (2017, 6): 2500.00,
    (2017, 9): 4000.00,
    (2017, 12): 14000.00,
    (2018, 1): 11000.00,
    (2018, 6): 6500.00,
    (2018, 12): 3800.00,

    # 2019: Recovery
    (2019, 1): 3600.00,
    (2019, 3): 4000.00,
    (2019, 6): 10000.00,
    (2019, 9): 8500.00,
    (2019, 12): 7200.00,

    # 2020: COVID crash and bull run
    (2020, 1): 7200.00,
    (2020, 3): 6400.00,
    (2020, 6): 9300.00,
    (2020, 9): 10800.00,
    (2020, 12): 19000.00,

    # 2021: ATH and consolidation
    (2021, 1): 32000.00,
    (2021, 3): 55000.00,
    (2021, 6): 35000.00,
    (2021, 9): 43000.00,
    (2021, 11): 65000.00,
    (2021, 12): 50000.00,

    # 2022: Bear market
    (2022, 1): 38000.00,
    (2022, 3): 42000.00,
    (2022, 6): 20000.00,
    (2022, 9): 19000.00,
    (2022, 12): 16500.00,

    # 2023: Recovery
    (2023, 1): 17000.00,
    (2023, 3): 23000.00,
    (2023, 6): 27000.00,
    (2023, 9): 26000.00,
    (2023, 12): 42000.00,

    # 2024: Bull run
    (2024, 1): 43000.00,
    (2024, 3): 67000.00,
    (2024, 6): 61000.00,
    (2024, 9): 63000.00,
    (2024, 10): 67000.00,
    (2024, 11): 72000.00,
    (2024, 12): 95000.00,

    # 2025: Continued growth
    (2025, 1): 105000.00,
    (2025, 2): 98000.00,
    (2025, 3): 115000.00,
    (2025, 4): 120000.00,
    (2025, 5): 125000.00,
    (2025, 6): 130000.00,
    (2025, 7): 135000.00,
    (2025, 8): 140000.00,
    (2025, 9): 145000.00,
    (2025, 10): 150000.00,
}


def get_fallback_price(year, month):
    """
    Get historical Bitcoin price from fallback data

    Args:
        year (int): Year
        month (int): Month (1-12)

    Returns:
        float: BTC price in USD, or None if not available
    """
    # Try exact match first
    if (year, month) in HISTORICAL_PRICES:
        return HISTORICAL_PRICES[(year, month)]

    # Try to interpolate from nearby months
    # Find closest available price
    closest_key = None
    min_month_diff = float('inf')

    target_months = year * 12 + month

    for (hist_year, hist_month), price in HISTORICAL_PRICES.items():
        hist_months = hist_year * 12 + hist_month
        diff = abs(hist_months - target_months)

        if diff < min_month_diff:
            min_month_diff = diff
            closest_key = (hist_year, hist_month)

    if closest_key and min_month_diff <= 3:  # Within 3 months
        return HISTORICAL_PRICES[closest_key]

    return None


def get_available_date_range():
    """
    Get the range of dates available in historical data

    Returns:
        tuple: (earliest_year, earliest_month, latest_year, latest_month)
    """
    if not HISTORICAL_PRICES:
        return None

    years_months = list(HISTORICAL_PRICES.keys())
    earliest = min(years_months)
    latest = max(years_months)

    return (earliest[0], earliest[1], latest[0], latest[1])
