# TCA_Project

This repository contains a Python-based **Transaction Cost Analysis (TCA)** workflow for equity trades. It includes scripts to compute key trading metrics such as **Arrival Slippage**, **Implementation Shortfall (IS)**, and **Broker Ranking**, along with a Jupyter notebook to orchestrate the analysis.

---

## 👂 Folder Structure

```
TCA_Project/
│
├─ database/          # SQLite database (tca.db) with trade data
├─ notebooks/         # Jupyter notebook: tca_metrics.ipynb
├─ tca/               # Python scripts for metrics
│   ├─ compute_slippage.py
│   ├─ compute_IS.py
│   └─ compute_broker.py
└─ README.md
```

---

## 🛠 Dependencies

- Python 3.11+
- pandas
- sqlite3 (built-in with Python)
- Jupyter Notebook
- Optional: Anaconda for environment management

Install dependencies:

```bash
pip install pandas jupyter
```

---

## 🗓 Usage

1. **Set up the database**  
   Place your SQLite database (`tca.db`) in the `database/` folder. Ensure the `trades` table exists with proper columns.

2. **Run the notebook**  
   Launch the Jupyter notebook in `notebooks/tca_metrics.ipynb`.  
   Example:

```python
from tca.compute_slippage import compute_arrival_slippage
from tca.compute_IS import compute_IS
from tca.compute_broker import compute_broker

# Compute arrival slippage for all trades
slippage_df = compute_arrival_slippage()

# Compute Implementation Shortfall
is_df = compute_arrival_slippage()

# Compute Broker Ranking
trades_df, broker_summary = compute_broker_rank()
```

3. **Filter and analyze**  
   You can filter the DataFrames in the notebook for specific symbols, sides, or date ranges.

---

## 🎈 Metrics Included

- **Arrival Slippage** – measures execution price vs. arrival price  
- **Implementation Shortfall (IS)** – measures execution price vs. decision price  
- **Broker Ranking** – evaluates brokers based on slippage and IS

---

## ⚡ Notes

- Functions are designed to **load from database if no DataFrame is provided**.  
- All functions return **pandas DataFrames** for flexible analysis in notebooks.  
- You can expand with additional TCA metrics (VWAP slippage, market impact, venue analysis).

---

## 🔗 License

MIT License (or your preferred license)

