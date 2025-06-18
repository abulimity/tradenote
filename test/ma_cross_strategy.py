"""
均线交叉策略：金叉买入，死叉卖出
使用qlib框架实现
"""

import qlib
from qlib.constant import REG_CN
from qlib.utils import init_instance_by_config
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord
from qlib.contrib.evaluate import backtest_daily
from qlib.contrib.strategy import TopkDropoutStrategy
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class MACrossStrategy(TopkDropoutStrategy):
    """
    均线交叉策略
    金叉（短期均线上穿长期均线）买入
    死叉（短期均线下穿长期均线）卖出
    """
    
    def __init__(self, 
                 short_window: int = 5,
                 long_window: int = 20,
                 topk: int = 50,
                 n_drop: int = 5,
                 **kwargs):
        """
        初始化策略参数
        
        Args:
            short_window: 短期均线周期
            long_window: 长期均线周期
            topk: 选择前k只股票
            n_drop: 剔除前n只股票
        """
        super().__init__(topk=topk, n_drop=n_drop, **kwargs)
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_trade_decision(self, score: pd.Series, trade_step: int) -> pd.Series:
        """
        生成交易决策
        
        Args:
            score: 股票评分
            trade_step: 交易步骤
            
        Returns:
            交易决策，1表示买入，-1表示卖出，0表示持有
        """
        # 获取当前持仓
        current_pos = self.get_current_position()
        
        # 计算均线信号
        signal = self._calculate_ma_signal(score.index.tolist(), trade_step)
        
        # 生成交易决策
        decision = pd.Series(0, index=score.index)
        
        # 金叉买入信号
        buy_signal = signal == 1
        decision[buy_signal] = 1
        
        # 死叉卖出信号
        sell_signal = signal == -1
        decision[sell_signal] = -1
        
        return decision
    
    def _calculate_ma_signal(self, instruments: List[str], trade_step: int) -> pd.Series:
        """
        计算均线交叉信号
        
        Args:
            instruments: 股票代码列表
            trade_step: 交易步骤
            
        Returns:
            信号序列：1表示金叉买入，-1表示死叉卖出，0表示无信号
        """
        # 获取历史数据
        data = self._get_historical_data(instruments, trade_step)
        
        signals = pd.Series(0, index=instruments)
        
        for instrument in instruments:
            if instrument in data.index:
                # 计算短期和长期均线
                short_ma = data.loc[instrument].rolling(window=self.short_window).mean()
                long_ma = data.loc[instrument].rolling(window=self.long_window).mean()
                
                # 计算交叉信号
                if len(short_ma) >= 2 and len(long_ma) >= 2:
                    # 当前和前一个时间点的均线差值
                    current_diff = short_ma.iloc[-1] - long_ma.iloc[-1]
                    prev_diff = short_ma.iloc[-2] - long_ma.iloc[-2]
                    
                    # 金叉：短期均线从下方穿越长期均线
                    if prev_diff < 0 and current_diff > 0:
                        signals[instrument] = 1
                    # 死叉：短期均线从上方穿越长期均线
                    elif prev_diff > 0 and current_diff < 0:
                        signals[instrument] = -1
        
        return signals
    
    def _get_historical_data(self, instruments: List[str], trade_step: int) -> pd.DataFrame:
        """
        获取历史价格数据
        
        Args:
            instruments: 股票代码列表
            trade_step: 交易步骤
            
        Returns:
            历史价格数据
        """
        # 这里简化处理，实际应该从qlib数据源获取
        # 在实际应用中，您需要使用qlib的数据接口
        try:
            # 获取最近的数据用于计算均线
            # 这里使用模拟数据，实际应该从qlib获取
            dates = pd.date_range(end=pd.Timestamp.now(), periods=50, freq='D')
            data = pd.DataFrame(
                np.random.randn(len(dates), len(instruments)) * 0.02 + 1.0,
                index=dates,
                columns=instruments
            )
            return data
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return pd.DataFrame()


def create_ma_cross_strategy_config():
    """
    创建均线交叉策略配置
    """
    strategy_config = {
        "class": "MACrossStrategy",
        "module_path": "test.ma_cross_strategy",
        "kwargs": {
            "short_window": 5,
            "long_window": 20,
            "topk": 50,
            "n_drop": 5,
        }
    }
    
    return strategy_config


def run_backtest():
    """
    运行回测
    """
    # 初始化qlib
    qlib.init(provider_uri='~/.qlib/qlib_data/cn_data', region=REG_CN)
    
    # 策略配置
    strategy_config = create_ma_cross_strategy_config()
    
    # 回测配置
    backtest_config = {
        "start_time": "2020-01-01",
        "end_time": "2023-12-31",
        "benchmark": "SH000300",  # 沪深300作为基准
        "account": 100000000,     # 初始资金1亿
        "exchange_kwargs": {
            "freq": "day",
            "limit_threshold": 0.095,
            "deal_price": "close",
            "open_cost": 0.0005,
            "close_cost": 0.0015,
            "min_cost": 5,
        }
    }
    
    # 创建策略实例
    strategy = init_instance_by_config(strategy_config)
    
    # 运行回测
    with R.start(experiment_name="ma_cross_strategy"):
        # 记录信号
        sr = SignalRecord(model=strategy, dataset=None, recorder=R.get_recorder())
        sr.generate()
        
        # 记录投资组合分析
        par = PortAnaRecord(recorder=R.get_recorder(), config=backtest_config, strategy=strategy)
        par.generate()
        
        # 获取回测结果
        report_normal, positions_normal = backtest_daily(
            account=backtest_config["account"],
            benchmark=backtest_config["benchmark"],
            start_time=backtest_config["start_time"],
            end_time=backtest_config["end_time"],
            strategy=strategy,
            exchange_kwargs=backtest_config["exchange_kwargs"]
        )
        
        return report_normal, positions_normal


def analyze_results(report: pd.DataFrame, positions: pd.DataFrame):
    """
    分析回测结果
    
    Args:
        report: 回测报告
        positions: 持仓信息
    """
    print("=" * 50)
    print("均线交叉策略回测结果")
    print("=" * 50)
    
    # 基本统计信息
    print(f"总收益率: {report['return'].sum():.2%}")
    print(f"年化收益率: {report['return'].mean() * 252:.2%}")
    print(f"最大回撤: {report['drawdown'].min():.2%}")
    print(f"夏普比率: {report['sharpe'].iloc[-1]:.2f}")
    print(f"胜率: {(report['return'] > 0).mean():.2%}")
    
    # 风险指标
    volatility = report['return'].std() * np.sqrt(252)
    print(f"年化波动率: {volatility:.2%}")
    
    # 最大回撤期间
    max_drawdown_idx = report['drawdown'].idxmin()
    print(f"最大回撤发生时间: {max_drawdown_idx}")
    
    # 收益分布
    print("\n收益分布统计:")
    print(f"平均日收益: {report['return'].mean():.2%}")
    print(f"收益标准差: {report['return'].std():.2%}")
    print(f"最小日收益: {report['return'].min():.2%}")
    print(f"最大日收益: {report['return'].max():.2%}")
    
    # 交易统计
    if 'trade_count' in report.columns:
        print(f"\n总交易次数: {report['trade_count'].sum()}")
        print(f"平均每日交易次数: {report['trade_count'].mean():.1f}")


def main():
    """
    主函数
    """
    print("开始运行均线交叉策略回测...")
    
    try:
        # 运行回测
        report, positions = run_backtest()
        
        # 分析结果
        analyze_results(report, positions)
        
        # 保存结果
        report.to_csv("ma_cross_strategy_report.csv")
        positions.to_csv("ma_cross_strategy_positions.csv")
        
        print("\n回测完成！结果已保存到CSV文件。")
        
    except Exception as e:
        print(f"回测过程中出现错误: {e}")
        print("请确保已正确安装qlib并下载了相应的数据。")


if __name__ == "__main__":
    main() 