import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("..", "database", "tca.db")

def compute_arrival_slippage(
    df=None,
    order_ids=None,
    symbol=None,
    side=None,
    date_from=None,
    date_to=None,
    min_qty=None,
    max_qty=None
):
    """
    Compute arrival slippage with clear structured filters.

    Priority:
    1. If df is supplied → use it directly
    2. Else → pull filtered rows from SQLite
    """

    if df is None:
        conn = sqlite3.connect(DB_PATH)

        # --- Build query dynamically --- #
        query = "SELECT * FROM trades"
        conditions = []
        params = []

        if order_ids:
            placeholders = ",".join(["?"] * len(order_ids))
            conditions.append(f"order_id IN ({placeholders})")
            params.extend(order_ids)

        if symbol:
            conditions.append("symbol = ?")
            params.append(symbol)

        if side:
            conditions.append("side = ?")
            params.append(side.upper())

        if date_from:
            conditions.append("start_time >= ?")
            params.append(date_from)

        if date_to:
            conditions.append("start_time <= ?")
            params.append(date_to)

        if min_qty:
            conditions.append("order_qty >= ?")
            params.append(min_qty)

        if max_qty:
            conditions.append("order_qty <= ?")
            params.append(max_qty)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

    # If still empty
    if df.empty:
        print("No trades found for slippage calculation.")
        return df

    # ---- Compute Arrival Slippage ---- #
    df.loc[df["side"] == "BUY", "arrival_slippage"] = (
    df["execution_price"] - df["arrival_price"])
        
        # SELL: arrival - exec
    df.loc[df["side"] == "SELL", "arrival_slippage"] = (
        df["arrival_price"] - df["execution_price"])
    
    df["arrival_slippage_bps"] = (
        df["arrival_slippage"] / df["arrival_price"]  ) * 10000
   

    df["arrival_slippage_bps"] = (
        df["arrival_slippage"] / df["arrival_price"]
    ) * 10000

    return df
