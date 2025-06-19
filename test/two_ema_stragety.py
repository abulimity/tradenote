import pandas as pd

from abc import ABC
from typing import Dict, List, Text, Tuple, Union
from qlib.data.dataset import Dataset
from qlib.model.base import BaseModel
from qlib.backtest.signal import Signal, create_signal_from
from qlib.strategy.base import BaseStrategy
from qlib.backtest.decision import Order, OrderDir, OrderHelper, TradeDecisionWO
# from qlib.strategy import 
# from qlib.backtest import backtest

class InnerStrategy(BaseStrategy):
    """
    Inner strategy for order execution:
    - Buy: if price < 200, buy all cash; else buy 200,000 worth.
    - Sell: if price > 200, sell all; else sell half.
    """
    STOCK_CODE = "000858.SZ"

    def generate_trade_decision(self, execute_result: list = None, action: str = None, amount: float = None):
        # action: 'buy' or 'sell', amount: suggested amount (shares) from outer
        position = self.trade_position
        trade_step = self.trade_calendar.get_trade_step()
        trade_start_time, trade_end_time = self.trade_calendar.get_step_time(trade_step)
        order_helper = self.trade_exchange.get_order_helper()
        orders = []
        price = self.trade_exchange.get_deal_price(self.STOCK_CODE, trade_start_time, trade_end_time)
        if action == 'buy':
            cash = position.get_cash()
            if price <= 0:
                return TradeDecisionWO([], self)
            if price < 200:
                buy_amount = cash // price
            else:
                buy_amount = min(cash // price, 200000 // price)
            buy_amount = int(buy_amount)
            if buy_amount > 0:
                order = order_helper.create(
                    code=self.STOCK_CODE,
                    amount=buy_amount,
                    direction=OrderDir.BUY,
                    start_time=trade_start_time,
                    end_time=trade_end_time,
                )
                orders.append(order)
        elif action == 'sell':
            held_amount = position.get_stock_amount(self.STOCK_CODE)
            if held_amount <= 0 or price <= 0:
                return TradeDecisionWO([], self)
            if price > 200:
                sell_amount = held_amount
            else:
                sell_amount = held_amount // 2
            sell_amount = int(sell_amount)
            if sell_amount > 0:
                order = order_helper.create(
                    code=self.STOCK_CODE,
                    amount=sell_amount,
                    direction=OrderDir.SELL,
                    start_time=trade_start_time,
                    end_time=trade_end_time,
                )
                orders.append(order)
        return TradeDecisionWO(orders, self)

class OuterStrategy(BaseStrategy):
    """
    Outer strategy:
    - If not holding Wuliangye, issues a buy order via inner strategy.
    - If holding, checks if held for 25 days, if so, issues a sell order via inner strategy.
    - Otherwise, holds.
    """
    STOCK_CODE = "000858.SZ"
    HOLD_DAYS = 25
    BAR = "day"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inner_strategy = InnerStrategy()

    def generate_trade_decision(self, execute_result: list = None):
        position = self.trade_position
        stock_list = position.get_stock_list()
        trade_step = self.trade_calendar.get_trade_step()
        trade_start_time, trade_end_time = self.trade_calendar.get_step_time(trade_step)
        # Pass infra to inner strategy
        self.inner_strategy.reset(level_infra=self.level_infra, common_infra=self.common_infra)
        if self.STOCK_CODE in stock_list:
            hold_days = position.get_stock_count(self.STOCK_CODE, self.BAR)
            if hold_days >= self.HOLD_DAYS:
                # Sell via inner strategy
                return self.inner_strategy.generate_trade_decision(action='sell')
        else:
            # Buy via inner strategy
            return self.inner_strategy.generate_trade_decision(action='buy')
        # Otherwise, hold
        return TradeDecisionWO([], self)