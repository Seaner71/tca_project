# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 13:20:01 2025

@author: ssmyt
"""

from dataclasses import dataclass

## TODO  add this class to remove the repitition in the function definitions

@dataclass
class TradeFilters:
    order_ids: list = None
    symbol: str = None
    side: str = None
    date_from: str = None
    date_to: str = None
    min_qty: int = None
    max_qty: int = None

