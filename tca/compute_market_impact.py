# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 15:09:54 2025

@author: ssmyt
"""

# tca/compute_market_impact.py

import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("..", "database", "tca.db")

def compute_market_impact(
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
    Compute Market Impact for trades:
    Market Impact = (Execution Price - Decision Price) - Market Move
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

    if df.empty:
        print("No trades found for Market Impact calculation.")
        return df

    # --- Compute Market Impact --- #
    def _impact(row):
        raw_impact = (row["execution_price"] - row["decision_price"])
        if row["side"] == "BUY":
            return raw_impact - (row["market_move_pct"] * row["decision_price"])
        else:  # SELL
            return -raw_impact - (row["market_move_pct"] * row["decision_price"])

    df["market_impact"] = df.apply(_impact, axis=1)
    df["market_impact_bps"] = (df["market_impact"] / df["decision_price"]) * 10000

    return df
