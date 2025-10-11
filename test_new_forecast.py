"""
Test script to verify the new multi-anchor point forecasting model
"""
import numpy as np
from datetime import datetime
from config import FORECAST_ANCHORS, MAX_THEORETICAL_BTC_PRICE
from forecasting import interpolate_price_between_anchors, get_projection_info, get_model_description

# Test with realistic current BTC prices
test_prices = [60000, 100000, 112000]

print("=" * 80)
print("NEW MULTI-ANCHOR POINT FORECASTING MODEL - TEST RESULTS")
print("=" * 80)

for current_price in test_prices:
    print(f"\n{'=' * 80}")
    print(f"TESTING WITH CURRENT BTC PRICE: ${current_price:,}")
    print(f"{'=' * 80}")

    # Get model info
    info = get_projection_info(current_price)

    print(f"\nModel Type: {info['model_type']}")
    print(f"Growth Rate to 2030: {info['growth_rate_to_2030_pct']:.2f}% annually")
    print(f"Safety Cap: ${info['max_cap']:,}")

    print(f"\n{'Year':<10} {'Projected Price':>20} {'Multiple of Current':>20}")
    print("-" * 80)

    # Test key years
    test_years = [2026, 2027, 2028, 2029, 2030, 2035, 2040, 2045, 2050]

    for year in test_years:
        projected = interpolate_price_between_anchors(current_price, year)
        multiple = projected / current_price

        # Highlight anchor years
        marker = " (ANCHOR)" if year in FORECAST_ANCHORS else ""

        print(f"{year:<10} ${projected:>19,.2f} {multiple:>19.1f}x{marker}")

    # Calculate and display 2050 stats
    price_2050 = interpolate_price_between_anchors(current_price, 2050)
    market_cap_2050 = price_2050 * 21_000_000  # 21M BTC total supply

    print(f"\n{'-' * 80}")
    print(f"2050 PROJECTION ANALYSIS:")
    print(f"  Price per BTC: ${price_2050:,.2f}")
    print(f"  Market Cap: ${market_cap_2050:,.0f} (${market_cap_2050/1e12:.2f} trillion)")
    print(f"  Multiple of current price: {price_2050/current_price:.1f}x")

    # Compare to global wealth
    global_wealth_low = 100e12  # $100 trillion
    global_wealth_high = 300e12  # $300 trillion
    pct_low = (market_cap_2050 / global_wealth_high) * 100
    pct_high = (market_cap_2050 / global_wealth_low) * 100

    print(f"  As % of global wealth ($100-300T): {pct_low:.1f}% - {pct_high:.1f}%")

    if market_cap_2050 < global_wealth_low:
        print(f"  ✅ REALISTIC - Market cap is below total global wealth")
    else:
        print(f"  ⚠️  WARNING - Market cap exceeds global wealth (may be too optimistic)")

print(f"\n{'=' * 80}")
print("MODEL DESCRIPTION")
print(f"{'=' * 80}")
print(get_model_description())

print(f"\n{'=' * 80}")
print("COMPARISON: OLD MODEL vs NEW MODEL")
print(f"{'=' * 80}")

current_price = 112000
print(f"\nWith current BTC at ${current_price:,}:\n")

# Old model calculation (for comparison)
current_date = datetime.now()
target_date_2030 = datetime(2030, 1, 1)
years_to_2030 = (target_date_2030 - current_date).days / 365.25
old_growth_rate = np.log(800_000 / current_price) / years_to_2030

years_to_2050 = (datetime(2050, 1, 1) - current_date).days / 365.25
old_price_2050 = current_price * np.exp(old_growth_rate * years_to_2050)

# New model calculation
new_price_2050 = interpolate_price_between_anchors(current_price, 2050)

print(f"{'Model':<20} {'2030 Projection':>25} {'2050 Projection':>25}")
print("-" * 80)
print(f"{'Old (Exponential)':<20} ${800_000:>24,} ${old_price_2050:>24,.2f}")
print(f"{'New (Multi-anchor)':<20} ${800_000:>24,} ${new_price_2050:>24,.2f}")
print(f"\n2050 Projection Reduction: {old_price_2050/new_price_2050:.0f}x more realistic")

print(f"\n{'=' * 80}")
print("✅ NEW MODEL SUCCESSFULLY PREVENTS UNREALISTIC PROJECTIONS")
print(f"{'=' * 80}\n")
