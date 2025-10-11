"""
Quick test script to analyze the forecasting model projections
"""
import numpy as np
from datetime import datetime
from config import TARGET_PRICE_2030

# Simulate the forecasting model with different current prices
def analyze_forecast(current_price):
    """Analyze what the model projects for various years"""

    current_date = datetime.now()
    target_date_2030 = datetime(2030, 1, 1)
    years_to_2030 = (target_date_2030 - current_date).days / 365.25

    # Calculate growth rate
    growth_rate = np.log(TARGET_PRICE_2030 / current_price) / years_to_2030

    print(f"\n{'='*70}")
    print(f"FORECAST ANALYSIS")
    print(f"{'='*70}")
    print(f"Current BTC Price: ${current_price:,.2f}")
    print(f"Target Price 2030: ${TARGET_PRICE_2030:,.2f}")
    print(f"Years to 2030: {years_to_2030:.2f}")
    print(f"Annual Growth Rate: {growth_rate*100:.2f}%")
    print(f"\n{'Year':<10} {'Projected Price':>20} {'Years from Now':>15}")
    print(f"{'-'*70}")

    # Project prices for key years
    years_to_project = [2025, 2026, 2027, 2028, 2029, 2030, 2035, 2040, 2045, 2050]

    for year in years_to_project:
        target_date = datetime(year, 1, 1)
        years_diff = (target_date - current_date).days / 365.25

        if years_diff >= 0:
            projected_price = current_price * np.exp(growth_rate * years_diff)
            print(f"{year:<10} ${projected_price:>19,.2f} {years_diff:>15.2f}")

    # Calculate 2050 specifically
    target_2050 = datetime(2050, 1, 1)
    years_to_2050 = (target_2050 - current_date).days / 365.25
    price_2050 = current_price * np.exp(growth_rate * years_to_2050)

    print(f"\n{'='*70}")
    print(f"2050 PROJECTION: ${price_2050:,.2f}")
    print(f"That's {price_2050/current_price:.1f}x the current price")
    print(f"{'='*70}\n")

    return price_2050

# Test with different current price scenarios
print("\n" + "="*70)
print("TESTING FORECAST MODEL WITH DIFFERENT CURRENT PRICES")
print("="*70)

# Test scenario 1: Current BTC at $60,000
analyze_forecast(60000)

# Test scenario 2: Current BTC at $100,000
analyze_forecast(100000)

# Test scenario 3: Current BTC at $112,000 (approximate current price in late 2024/early 2025)
analyze_forecast(112000)
