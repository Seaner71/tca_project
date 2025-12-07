# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 11:48:56 2025

@author: ssmyt
"""

import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("..", "database", "tca.db")

def compute_broker_rank(
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
    Compute broker ranking based on arrival slippage and implementation shortfall.

    Returns
    -------
    pandas.DataFrame with per-trade metrics and summary grouped by broker.
    """

    # Load trades from DB if df not provided
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

    # Compute Arrival Slippage
    df["arrival_slippage"] = df.apply(
        lambda row: (
            row["execution_price"] - row["arrival_price"]
            if row["side"] == "BUY"
            else row["arrival_price"] - row["execution_price"]
        ),
        axis=1
    )
    df["arrival_slippage_bps"] = (df["arrival_slippage"] / df["arrival_price"]) * 10000

    # Compute Implementation Shortfall
    df["IS"] = df.apply(
        lambda row: (
            row["execution_price"] - row["decision_price"]
            if row["side"] == "BUY"
            else row["decision_price"] - row["execution_price"]
        ),
        axis=1
    )
    df["IS_bps"] = (df["IS"] / df["decision_price"]) * 10000

    # Summary grouped by broker
    summary = df.groupby("broker").agg(
        trades_count=("order_id", "count"),
        avg_arrival_slippage_bps=("arrival_slippage_bps", "mean"),
        avg_IS_bps=("IS_bps", "mean")
    ).reset_index().sort_values(by="avg_arrival_slippage_bps")

    return df, summary

# Optional wrapper
def compute_broker(**kwargs):
    return compute_broker_rank(**kwargs)
