# Bitcoin Investment Calculator

A minimalistic dashboard to calculate historical Bitcoin investment returns and project future values.

### Example Use Cases

**Use Case 1: USD Investment**
- Select "USD Investment" and enter $1,000
- Choose January 2020 as purchase date
- See that you would have bought ~0.1389 BTC at $7,200/BTC
- View current value showing ~$15,600 (assuming ~$112k current price)
- Profit: ~$14,600 (1,460% gain)

**Use Case 2: BTC Amount**
- Select "BTC Amount" and enter 0.5 BTC
- Choose June 2017 as purchase date
- See that it cost $1,250 at $2,500/BTC
- View current value and profit/loss

### View:
<img width="650" height="811" alt="image" src="https://github.com/user-attachments/assets/233e9cea-5fad-4042-8eab-32ae41df2d06" />


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
oses only. Bitcoin price projections are speculative and based on simplified models. This is not financial advice. Always do your own research before making investment decisions.
