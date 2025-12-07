import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("..", "database", "tca.db")

def compute_implementation_shortfall(
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
    Compute Implementation Shortfall (IS) for trades with optional filters.

    Parameters mirror compute_arrival_slippage.

    Returns
    -------
    pandas.DataFrame with IS and IS_bps columns added.
    """

    # Load filtered trades from database if df not provided
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
        print("No trades found for IS calculation.")
        return df

    # Compute Implementation Shortfall
    df["IS"] = df.apply(
        lambda row: (
            row["execution_price"] - row["decision_price"]
            if row["side"] == "BUY"
            else row["decision_price"] - row["execution_price"]
        ),
        axis=1,
    )

    df["IS_bps"] = (df["IS"] / df["decision_price"]) * 10000

    return df
