"""
Visualization Module
Handles chart generation for Bitcoin price and portfolio value over time

Functions:
- generate_price_history_chart(): Create interactive chart showing BTC price and portfolio value
- create_chart_figure(): Build Plotly figure with custom styling
"""

import plotly.graph_objects as go
from datetime import datetime
from api_handler import get_price_for_date
from config import (
    MAX_MONTHLY_POINTS,
    QUARTERLY_SAMPLE_MONTHS,
    BITCOIN_ORANGE,
    SECONDARY_COLOR,
    CHART_BG_COLOR,
    CHART_GRID_COLOR
)


# ============================================================================
# DATA PREPARATION
# ============================================================================

def prepare_chart_data(start_year, start_month, end_year, end_month, btc_amount):
    """
    Prepare data points for the price history chart

    Generates monthly or quarterly data points depending on the total time range.
    For ranges > 120 months, switches to quarterly sampling to improve performance.

    Args:
        start_year (int): Starting year
        start_month (int): Starting month (1-12)
        end_year (int): Ending year
        end_month (int): Ending month (1-12)
        btc_amount (float): Amount of BTC to track

    Returns:
        tuple: (dates, prices, portfolio_values, has_projections)
            - dates (list): List of datetime objects
            - prices (list): List of BTC prices in USD
            - portfolio_values (list): List of portfolio values (price * btc_amount)
            - has_projections (bool): True if any data points are projections
    """
    # Calculate total months in range
    total_months = (end_year - start_year) * 12 + (end_month - start_month) + 1

    # Determine sampling frequency (monthly vs quarterly)
    # If range is too large, sample quarterly to keep chart readable
    step_months = 1 if total_months <= MAX_MONTHLY_POINTS else QUARTERLY_SAMPLE_MONTHS

    # Initialize data lists
    dates = []
    prices = []
    portfolio_values = []
    has_projections = False

    # Generate data points
    current_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)

    while current_date <= end_date:
        # Fetch price for this date (historical or projected)
        price, is_projected = get_price_for_date(current_date.year, current_date.month)

        if is_projected:
            has_projections = True

        # Add data point
        dates.append(current_date)
        prices.append(price if price else 0)
        portfolio_values.append((price * btc_amount) if price else 0)

        # Move to next sampling point (month or quarter)
        month = current_date.month + step_months
        year = current_date.year

        # Handle month overflow (e.g., month 15 becomes January of next year)
        while month > 12:
            month -= 12
            year += 1

        current_date = datetime(year, month, 1)

    return dates, prices, portfolio_values, has_projections


# ============================================================================
# CHART CREATION
# ============================================================================

def create_chart_figure(dates, prices, portfolio_values, btc_amount, has_projections):
    """
    Create a Plotly figure with BTC price and portfolio value traces

    Args:
        dates (list): List of datetime objects
        prices (list): List of BTC prices
        portfolio_values (list): List of portfolio values
        btc_amount (float): Amount of BTC
        has_projections (bool): Whether chart includes projected values

    Returns:
        plotly.graph_objects.Figure: Configured chart figure
    """
    # Create new figure
    fig = go.Figure()

    # Add BTC price trace (main line in Bitcoin orange)
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        name='BTC Price (USD)',
        line=dict(color=BITCOIN_ORANGE, width=2),
        hovertemplate='<b>Date:</b> %{x|%b %Y}<br><b>BTC Price:</b> $%{y:,.2f}<extra></extra>'
    ))

    # Add portfolio value trace (secondary line in dark gray, dotted)
    fig.add_trace(go.Scatter(
        x=dates,
        y=portfolio_values,
        name=f'Portfolio Value ({btc_amount} BTC)',
        line=dict(color=SECONDARY_COLOR, width=2, dash='dot'),
        hovertemplate='<b>Date:</b> %{x|%b %Y}<br><b>Portfolio Value:</b> $%{y:,.2f}<extra></extra>'
    ))

    # Configure chart title
    title = 'Bitcoin Price & Portfolio Value Over Time'
    if has_projections:
        title += ' (includes projections)'

    # Update layout with Bitcoin theme
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Value (USD)',
        hovermode='x unified',  # Show both traces when hovering
        plot_bgcolor=CHART_BG_COLOR,
        paper_bgcolor=CHART_BG_COLOR,
        font=dict(color=SECONDARY_COLOR),
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Style axes with grid lines
    fig.update_xaxes(
        showgrid=True,
        gridcolor=CHART_GRID_COLOR
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=CHART_GRID_COLOR,
        tickformat='$,.0f'  # Format y-axis as currency
    )

    return fig


# ============================================================================
# MAIN CHART GENERATION FUNCTION
# ============================================================================

def generate_price_history_chart(start_year, start_month, end_year, end_month, btc_amount):
    """
    Generate a complete price history chart showing BTC price and portfolio value

    This is the main function called by the UI to create charts.
    It handles data preparation and chart creation.

    Args:
        start_year (int): Starting year
        start_month (int): Starting month (1-12)
        end_year (int): Ending year
        end_month (int): Ending month (1-12)
        btc_amount (float): Amount of BTC to track

    Returns:
        plotly.graph_objects.Figure: Interactive chart figure ready for display

    Example:
        >>> fig = generate_price_history_chart(2020, 1, 2024, 12, 0.5)
        >>> # Display in Streamlit: st.plotly_chart(fig, use_container_width=True)
    """
    # Prepare data points
    dates, prices, portfolio_values, has_projections = prepare_chart_data(
        start_year, start_month, end_year, end_month, btc_amount
    )

    # Create and return chart figure
    fig = create_chart_figure(dates, prices, portfolio_values, btc_amount, has_projections)

    return fig


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_chart_stats(dates, prices, portfolio_values):
    """
    Calculate statistics about the chart data (optional utility function)

    Args:
        dates (list): List of dates
        prices (list): List of prices
        portfolio_values (list): List of portfolio values

    Returns:
        dict: Statistics including min, max, and average values
    """
    return {
        'min_price': min(prices),
        'max_price': max(prices),
        'avg_price': sum(prices) / len(prices) if prices else 0,
        'min_portfolio': min(portfolio_values),
        'max_portfolio': max(portfolio_values),
        'avg_portfolio': sum(portfolio_values) / len(portfolio_values) if portfolio_values else 0,
        'num_data_points': len(dates)
    }
