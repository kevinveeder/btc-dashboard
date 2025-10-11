"""
Configuration file for Bitcoin Investment Dashboard
Contains all constants and configuration parameters

Modify values here to change dashboard behavior without touching other files
"""

from datetime import datetime

# ============================================================================
# API CONFIGURATION
# ============================================================================

# CoinGecko API base URL (free, no API key required)
COINGECKO_API_BASE_URL = "https://api.coingecko.com/api/v3"

# API timeout in seconds
API_TIMEOUT = 10

# Cache duration for API calls (in seconds)
# Set to 3600 (1 hour) to reduce API calls and improve performance
CACHE_TTL = 3600


# ============================================================================
# DATE RANGE CONFIGURATION
# ============================================================================

# Minimum year for historical data (Bitcoin data available from ~2010)
MIN_YEAR = 2010

# Maximum year for future projections
MAX_YEAR = 2050

# Current year (auto-calculated)
CURRENT_YEAR = datetime.now().year


# ============================================================================
# BTC AMOUNT CONFIGURATION
# ============================================================================

# Minimum BTC amount users can input (supports 4 decimal places)
MIN_BTC_AMOUNT = 0.0001

# Maximum BTC amount users can input
MAX_BTC_AMOUNT = 1000000.0

# Default BTC amount shown in input field
DEFAULT_BTC_AMOUNT = 1.0

# Number of decimal places for BTC input
BTC_DECIMAL_PLACES = 4


# ============================================================================
# FORECASTING MODEL CONFIGURATION
# ============================================================================

# ANCHOR POINTS for multi-year forecasting (based on expert consensus)
# These represent realistic price targets at specific years
# Model interpolates between these points to avoid unrealistic exponential growth
FORECAST_ANCHORS = {
    2030: 800_000,       # Conservative-to-moderate expert consensus
    2040: 2_500_000,     # Median expert forecast (range: $1M-$6M)
    2050: 6_000_000,     # Conservative expert forecast (range: $2M-$7.5M)
}

# Legacy target for backward compatibility
TARGET_PRICE_2030 = FORECAST_ANCHORS[2030]

# Maximum theoretical Bitcoin price (safety cap)
# Based on Hal Finney's calculation: if BTC = all global wealth ($100-300T / 21M BTC)
# This prevents physically impossible projections
MAX_THEORETICAL_BTC_PRICE = 22_000_000

# Base year for price projections
FORECAST_BASE_YEAR = 2024


# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

# Maximum number of months to show in chart before switching to quarterly view
MAX_MONTHLY_POINTS = 120

# Chart sampling: if total months > MAX_MONTHLY_POINTS, sample every N months
QUARTERLY_SAMPLE_MONTHS = 3

# Bitcoin orange color (official brand color)
BITCOIN_ORANGE = "#F7931A"

# Secondary color for portfolio value line
SECONDARY_COLOR = "#4A4A4A"

# Chart background color
CHART_BG_COLOR = "white"

# Grid color for chart
CHART_GRID_COLOR = "#E0E0E0"


# ============================================================================
# UI THEME CONFIGURATION
# ============================================================================

# Main background color
MAIN_BG_COLOR = "#FFFFFF"

# Text colors
PRIMARY_TEXT_COLOR = "#F7931A"  # Bitcoin orange for headers
SECONDARY_TEXT_COLOR = "#4A4A4A"  # Dark gray for body text

# Button hover color
BUTTON_HOVER_COLOR = "#E17F0A"

# Warning/info box background
INFO_BOX_BG_COLOR = "#FFF5E6"


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

# Streamlit page title (shown in browser tab)
PAGE_TITLE = "Bitcoin Investment Calculator"

# Page icon (shown in browser tab)
PAGE_ICON = "₿"

# Layout mode: "centered" or "wide"
PAGE_LAYOUT = "centered"


# ============================================================================
# DISCLAIMER TEXT
# ============================================================================

# Disclaimer shown for future projections
PROJECTION_DISCLAIMER = (
    "⚠️ **Disclaimer:** Future projections are estimates based on historical trends "
    "and are for educational purposes only. This is not financial advice."
)

# Footer text
FOOTER_TEXT = """
<div style='text-align: center; color: #888; font-size: 0.8em;'>
<p>Data provided by CoinGecko API | Historical data from 2010 onwards</p>
<p>This tool is for educational purposes only and does not constitute financial advice.</p>
</div>
"""
