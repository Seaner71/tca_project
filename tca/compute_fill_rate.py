import os
import sqlite3
import pandas as pd
from compute_slippage import DB_PATH  

def compute_fill_rate(df=None,
        order_ids=None,
        symbol=None,
        side=None,
        date_from=None,
        date_to=None,
        min_qty=None,
        max_qty=None):
    """
    Compute fill rate for trades. Returns df with fill_rate column.
    """
    if df is None:
        conn = sqlite3.connect(DB_PATH)
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
            conditions.append("executed_qty >= ?")
            params.append(min_qty)

        if max_qty:
            conditions.append("executed_qty <= ?")
            params.append(max_qty)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

    if df.empty:
        print("No trades found for broker ranking.")
        return pd.DataFrame()

    df["fill_rate"] = df["executed_qty"] / df["order_qty"]

    return df
