# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 18:42:51 2025

@author: ssmyt
"""

import os
import sqlite3
import pandas as pd

def load_csv(file_name="sample_trades.csv"):
    csv_path = os.path.join("..", "data", file_name)
    
    if not os.path.exists(os.path.dirname(csv_path)):
        raise FileNotFoundError(f"Database folder does not exist: {os.path.dirname(csv_path)}")
    df = pd.read_csv(csv_path)
    
    return df



def load_sqlite(db_file="trades.db", table="trades"):
    """
    Load a table from SQLite database into a Pandas DataFrame.
    
    db_file : str
        SQLite database file name (should be in database/ folder)
    table : str
        Table name in the database
    """
    
    db_path = os.path.join("..", "database", db_file)
    
   
    if not os.path.exists(os.path.dirname(db_path)):
        raise FileNotFoundError(f"Database folder does not exist: {os.path.dirname(db_path)}")
    
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    except Exception as e:
        print(f"Error reading table '{table}' from database '{db_file}': {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    
    return df
