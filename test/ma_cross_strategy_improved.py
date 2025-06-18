"""
改进的均线交叉策略：金叉买入，死叉卖出
使用qlib框架实现，包含完整的数据获取和信号计算
"""

import qlib
from qlib.constant import REG_CN
from qlib.utils import init_instance_by_config
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord
from qlib.contrib.evaluate import backtest_daily
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.data import D
from qlib.data.dataset import DatasetH
from qlib.data.dataset.handler import DataHandlerLP
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class MACrossStrategyImproved(TopkDropoutStrategy):
    """
    改进的均线交叉策略
    金叉（短期均线上穿长期均线）买入
    死叉（短期均线下穿长期均线）卖出
    """
    
    def __init__(self, 
                 short_window: int = 5,
                 long_window: int = 20,
                 topk: int = 50,
                 n_drop: int = 5,
                 universe: str = "csi300",
                 **kwargs):
        """
        初始化策略参数
        
        Args:
            short_window: 短期均线周期
            long_window: 长期均线周期
            topk: 选择前k只股票
            n_drop: 剔除前n只股票
            universe: 股票池
        """
        super().__init__(topk=topk, n_drop=n_drop, **kwargs)
        self.short_window = short_window
        self.long_window = long_window
        self.universe = universe
        self.instruments = None
        self.price_cache = {}
        
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
        signals = pd.Series(0, index=instruments)
        
        # 获取当前日期
        current_date = self._get_current_date(trade_step)
        
        for instrument in instruments:
            try:
                # 获取历史价格数据
                price_data = self._get_price_data(instrument, current_date)
                
                if price_data is not None and len(price_data) >= self.long_window:
                    # 计算短期和长期均线
                    short_ma = price_data['close'].rolling(window=self.short_window).mean()
                    long_ma = price_data['close'].rolling(window=self.long_window).mean()
                    
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
                            
            except Exception as e:
                print(f"计算{instrument}均线信号时出错: {e}")
                continue
        
        return signals
    
    def _get_price_data(self, instrument: str, current_date: str) -> pd.DataFrame:
        """
        获取股票价格数据
        
        Args:
            instrument: 股票代码
            current_date: 当前日期
            
        Returns:
            价格数据DataFrame
        """
        try:
            # 计算开始日期（获取足够的历史数据来计算均线）
            start_date = pd.Timestamp(current_date) - pd.Timedelta(days=self.long_window * 2)
            
            # 从qlib获取数据
            data = D.features(
                instruments=[instrument],
                start_time=start_date.strftime('%Y-%m-%d'),
                end_time=current_date,
                freq='day',
                fields=['$close', '$open', '$high', '$low', '$volume']
            )
            
            if data is not None and not data.empty:
                # 重命名列
                data.columns = ['close', 'open', 'high', 'low', 'volume']
                return data
            else:
                return None
                
        except Exception as e:
            print(f"获取{instrument}价格数据失败: {e}")
            return None
    
    def _get_current_date(self, trade_step: int) -> str:
        """
        根据交易步骤获取当前日期
        
        Args:
            trade_step: 交易步骤
            
        Returns:
            当前日期字符串
        """
        # 这里简化处理，实际应该从qlib的日历获取
        # 假设从2020-01-01开始，每个trade_step代表一天
        start_date = pd.Timestamp('2020-01-01')
        current_date = start_date + pd.Timedelta(days=trade_step)
        return current_date.strftime('%Y-%m-%d')


def create_dataset_config():
    """
    创建数据集配置
    """
    dataset_config = {
        "class": "DatasetH",
        "module_path": "qlib.data.dataset",
        "kwargs": {
            "handler": {
                "class": "DataHandlerLP",
                "module_path": "qlib.data.dataset.handler",
                "kwargs": {
                    "start_time": "2020-01-01",
                    "end_time": "2023-12-31",
                    "fit_start_time": "2020-01-01",
                    "fit_end_time": "2023-12-31",
                    "instruments": "csi300",
                    "infer_processors": [
                        {
                            "class": "RobustZScoreNorm",
                            "module_path": "qlib.data.dataset.processor",
                            "kwargs": {
                                "fields_group": "feature",
                                "clip_outlier": True,
                            },
                        },
                        {
                            "class": "Fillna",
                            "module_path": "qlib.data.dataset.processor",
                            "kwargs": {
                                "fields_group": "feature",
                            },
                        },
                    ],
                    "learn_processors": [
                        {
                            "class": "DropnaLabel",
                            "module_path": "qlib.data.dataset.processor",
                        },
                        {
                            "class": "CSRankNorm",
                            "module_path": "qlib.data.dataset.processor",
                            "kwargs": {
                                "fields_group": "label",
                            },
                        },
                    ],
                    "instruments": "csi300",
                },
            },
            "segments": {
                "train": ("2020-01-01", "2022-12-31"),
                "valid": ("2023-01-01", "2023-06-30"),
                "test": ("2023-07-01", "2023-12-31"),
            },
        },
    }
    
    return dataset_config


def create_ma_cross_strategy_config():
    """
    创建均线交叉策略配置
    """
    strategy_config = {
        "class": "MACrossStrategyImproved",
        "module_path": "test.ma_cross_strategy_improved",
        "kwargs": {
            "short_window": 5,
            "long_window": 20,
            "topk": 50,
            "n_drop": 5,
            "universe": "csi300",
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
    with R.start(experiment_name="ma_cross_strategy_improved"):
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
    
    if 'sharpe' in report.columns:
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


def create_simple_backtest():
    """
    创建简化版回测，用于演示
    """
    print("创建简化版均线交叉策略回测...")
    
    # 初始化qlib
    qlib.init(provider_uri='~/.qlib/qlib_data/cn_data', region=REG_CN)
    
    # 获取股票列表
    instruments = D.list_instruments(instruments="csi300", start_time="2020-01-01", end_time="2023-12-31")
    
    print(f"获取到 {len(instruments)} 只股票")
    
    # 选择前10只股票进行演示
    demo_instruments = instruments[:10]
    
    # 获取价格数据
    data = D.features(
        instruments=demo_instruments,
        start_time="2020-01-01",
        end_time="2023-12-31",
        freq='day',
        fields=['$close']
    )
    
    print(f"获取到价格数据，形状: {data.shape}")
    
    # 计算均线
    short_ma = data.rolling(window=5).mean()
    long_ma = data.rolling(window=20).mean()
    
    # 计算交叉信号
    signals = pd.DataFrame(0, index=data.index, columns=data.columns)
    
    for col in data.columns:
        # 计算均线差值
        diff = short_ma[col] - long_ma[col]
        
        # 计算交叉信号
        for i in range(1, len(diff)):
            if diff.iloc[i-1] < 0 and diff.iloc[i] > 0:
                signals.iloc[i, signals.columns.get_loc(col)] = 1  # 金叉买入
            elif diff.iloc[i-1] > 0 and diff.iloc[i] < 0:
                signals.iloc[i, signals.columns.get_loc(col)] = -1  # 死叉卖出
    
    # 统计信号
    buy_signals = (signals == 1).sum().sum()
    sell_signals = (signals == -1).sum().sum()
    
    print(f"\n信号统计:")
    print(f"买入信号数量: {buy_signals}")
    print(f"卖出信号数量: {sell_signals}")
    
    # 计算简单收益（假设每次信号都产生1%的收益）
    returns = signals * 0.01
    cumulative_returns = returns.sum(axis=1).cumsum()
    
    print(f"\n累计收益: {cumulative_returns.iloc[-1]:.2%}")
    
    return signals, cumulative_returns


def main():
    """
    主函数
    """
    print("开始运行均线交叉策略回测...")
    
    try:
        # 运行简化版回测
        signals, cumulative_returns = create_simple_backtest()
        
        # 保存简化版结果
        signals.to_csv("ma_cross_signals.csv")
        cumulative_returns.to_csv("ma_cross_cumulative_returns.csv")
        
        print("\n简化版回测完成！")
        print("信号数据已保存到 ma_cross_signals.csv")
        print("累计收益已保存到 ma_cross_cumulative_returns.csv")
        
    except Exception as e:
        print(f"回测过程中出现错误: {e}")
        print("请确保已正确安装qlib并下载了相应的数据。")


if __name__ == "__main__":
    main() 