from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.contrib.evaluate import risk_analysis
from qlib.contrib.data.handler import Alpha158
from qlib.data import D
from qlib.contrib.report import analysis_position
from qlib.backtest import backtest, executor
from qlib.strategy.base import BaseStrategy

# Buy and Hold Strategy Implementation
class BuyAndHoldStrategy(BaseStrategy):
    """
    简单的买入并持有策略：初始化时买入所有可用资金，并一直持有
    """

    def generate_trade_decision(self, *args, **kwargs):
        if not hasattr(self, "has_bought"):
            self.has_bought = False

        if not self.has_bought:
            trade_account = self.common_infra.get("trade_account")
            cash = trade_account.current_position.position['cash']
            stock = "SZ000585"
            # available_stocks = self.trade_exchange.list_instruments()
            # weights = {stock: 1.0 / len(available_stocks) for stock in available_stocks}
            self.has_bought = True
            return {
                "action": "buy",
                "weights": {stock: 1.0},
                "cash": cash
            }
        else:
            return {
                "action": "hold"
            }

if __name__ == "__main__":
    import qlib
    from qlib.config import REG_CN

    # 初始化qlib（请根据你的环境选择合适的provider_uri）
    qlib.init(provider_uri=r"D:\project\python\tradenote\qlibz\qlib_data\cn_data", region=REG_CN)

    # 数据处理
    handler = Alpha158(instruments="csi300", start_time="2017-01-01", end_time="2020-12-31")

    # 策略实例
    strategy = BuyAndHoldStrategy()

    # 回测参数
    EXECUTOR_CONFIG = {
        "time_per_step": "day",
        "generate_portfolio_metrics": True,
    }

    backtest_config = {
        "start_time": "2018-01-01",
        "end_time": "2020-12-31",
        "account": 100000000,
        "benchmark": "SH000300",
        "exchange_kwargs": {
            "freq": "day",
            "limit_threshold": 0.095,
            "deal_price": "close",
            "open_cost": 0.0003,
            "close_cost": 0.0013,
            "min_cost": 5,
        },
    }

    # 执行器
    exec = executor.SimulatorExecutor(**EXECUTOR_CONFIG)

    # 回测
    report_normal, positions = backtest(
        strategy=strategy,
        executor=exec,
        **backtest_config
    )

    print("回测结果：")
    print(report_normal)
    print("持仓分析：")
    print(analysis_position.report_graph(positions))