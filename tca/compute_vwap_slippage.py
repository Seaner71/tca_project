# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 13:53:06 2025

@author: ssmyt
"""

import os
import sqlite3
import pandas as pd
from compute_slippage import DB_PATH  # reuse your existing DB_PATH

def compute_vwap_slippage(df=None,
                          order_ids=None,
                          symbol=None,
                          side=None,
                          date_from=None,
                          date_to=None,
                          min_qty=None,
                          max_qty=None):
    """
    Compute VWAP slippage for trades.
    Priority:
    1. If df is supplied → use it directly
    2. Else → pull filtered rows from SQLite
    """
    # --- Load data if df not provided --- #
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
            conditions.append("order_qty >= ?")
            params.append(min_qty)

        if max_qty:
            conditions.append("order_qty <= ?")
            params.append(max_qty)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

    if df.empty:
        print("No trades found for VWAP slippage calculation.")
        return df

    # --- Compute VWAP slippage --- #
    df["vwap_slippage"] = df.apply(
        lambda row: (row["execution_price"] - row["vwap"])
        if row["side"] == "BUY"
        else (row["vwap"] - row["execution_price"]),
        axis=1
    )

    df["vwap_slippage_bps"] = (df["vwap_slippage"] / df["vwap"]) * 10000

    return df
