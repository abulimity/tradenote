import pandas as pd
from qlib.contrib.data.handler import Alpha158
from qlib.utils.time import Freq
from qlib.data import D
from qlib.contrib.report import analysis_position
from qlib.backtest import backtest, executor
from qlib.strategy.base import BaseStrategy
from qlib.backtest.decision import TradeDecisionWO,OrderHelper,OrderDir

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
            order = OrderHelper.create(
                code=stock,
                amount=cash,
                direction=OrderDir.BUY
            )
            return TradeDecisionWO([order], self)

        else:
            return TradeDecisionWO([],self)

if __name__ == "__main__":
    import qlib
    from qlib.config import REG_CN

    # 初始化qlib（请根据你的环境选择合适的provider_uri）
    qlib.init(provider_uri=r"D:\project\python\tradenote\qlib_data\cn_data", region=REG_CN)

    start_date = "2017-01-01"
    end_date = "2018-01-01"

    # 数据处理
    handler = Alpha158(instruments="csi300", start_time=start_date, end_time=end_date)

    # 策略实例
    strategy = BuyAndHoldStrategy()

    # 回测参数
    EXECUTOR_CONFIG = {
        "time_per_step": "day",
        "generate_portfolio_metrics": True,
    }

    backtest_config = {
        "start_time": start_date,
        "end_time": end_date,
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
    portfolio_metric_dict, indicator_dict = backtest(
        strategy=strategy,
        executor=exec,
        **backtest_config
    )
    analysis_freq = "{0}{1}".format(*Freq.parse("day"))
    report_normal_df, positions_normal = portfolio_metric_dict.get(analysis_freq)
    analysis_position.report_graph(report_normal_df)
