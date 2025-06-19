from qlib.strategy.base import BaseStrategy

class BuyAndHoldStrategy(BaseStrategy):
    """
    简单的买入并持有策略：初始化时买入所有可用资金，并一直持有
    """

    def generate_trade_decision(self, *args, **kwargs):
        """
        在第一次调用时买入全部资产，之后不再交易
        """
        if not hasattr(self, "has_bought"):
            self.has_bought = False

        if not self.has_bought:
            # 这里的 pseudo_code 仅做示例，具体接口参数和格式请根据 Qlib 版本调整
            trade_account = self.common_infra.get("trade_account")
            cash = trade_account.cash
            available_stocks = self.trade_exchange.list_instruments()
            weights = {stock: 1.0 / len(available_stocks) for stock in available_stocks}
            self.has_bought = True
            return {
                "action": "buy",
                "weights": weights,
                "cash": cash
            }
        else:
            return {
                "action": "hold"
            }