# Bitcoin Investment Calculator

A minimalistic dashboard to calculate historical Bitcoin investment returns and project future values.

## Features

- **Historical Analysis**: Select any past date from 2010-present and see what your Bitcoin investment would be worth today
- **Future Projections**: Forecast potential Bitcoin values up to 2050 using exponential growth models
- **Interactive Charts**: Visualize Bitcoin price history and portfolio value over time
- **Real-time Data**: Uses CoinGecko API for current Bitcoin prices
- **Fallback Data**: Comprehensive historical price database for periods when API is unavailable
- **Minimalistic Design**: Clean Bitcoin orange theme with excellent readability

## Setup

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2. Install Dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Usage

1. **Enter BTC Amount**: Input the amount of Bitcoin you want to analyze (minimum 0.0001 BTC)

2. **Select Purchase Date**: Choose the year and month when you hypothetically purchased the Bitcoin

3. **Choose Comparison Type**:
   - **Today's Value**: See what your investment is worth right now
   - **Future Projection**: Project the value at a future date (up to 2050)

4. **Calculate**: Click the button to see results including:
   - Purchase value
   - Current/Projected value
   - Profit/Loss amount and percentage
   - Interactive price history chart

## Configuration

All settings can be adjusted in `config.py`:

- `MAX_YEAR`: Maximum year for projections (default: 2050)
- `TARGET_PRICE_2030`: Price target used to calibrate forecasting model (default: $800,000)
- `BITCOIN_ORANGE`: Primary theme color
- Date ranges, BTC amount limits, and more

## Data Sources

- **Current Prices**: CoinGecko API (free tier, no key required)
- **Historical Prices**: Fallback database with monthly price points from 2010-2024
- **Future Projections**: Exponential growth model calibrated to reach ~$800k by 2030

## Project Structure

```
btc-dashboard/
├── app.py                    # Main application entry point
├── config.py                 # Configuration settings
├── api_handler.py            # API calls and price fetching
├── historical_prices.py      # Fallback historical price data
├── forecasting.py            # Future price projection models
├── visualization.py          # Chart generation
├── ui_components.py          # UI styling and components
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Known Limitations

- CoinGecko free API has rate limits and restricted historical data access
- Historical price data is approximate monthly averages
- Future projections are educational estimates only and should not be used for investment decisions
- This is NOT financial advice

## Troubleshooting

**Issue**: Text not visible on white background
**Solution**: Fixed with updated CSS using `!important` flags for text colors

**Issue**: API authorization errors
**Solution**: Implemented fallback historical price database for dates when API is unavailable

**Issue**: App won't start
**Solution**: Make sure virtual environment is activated and all dependencies are installed

## Disclaimer

This tool is for educational purposes only. Bitcoin price projections are speculative and based on simplified models. This is not financial advice. Always do your own research before making investment decisions.
