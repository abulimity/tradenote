"""
简单实用的均线交叉策略
金叉买入，死叉卖出
"""

import qlib
from qlib.constant import REG_CN
from qlib.data import D
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def init_qlib():
    """初始化qlib"""
    try:
        qlib.init(provider_uri='~/.qlib/qlib_data/cn_data', region=REG_CN)
        print("qlib初始化成功")
        return True
    except Exception as e:
        print(f"qlib初始化失败: {e}")
        print("请确保已安装qlib并下载了数据")
        return False


def get_stock_data(instruments, start_date, end_date):
    """
    获取股票数据
    
    Args:
        instruments: 股票代码列表
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        股票价格数据
    """
    try:
        data = D.features(
            instruments=instruments,
            start_time=start_date,
            end_time=end_date,
            freq='day',
            fields=['$close', '$open', '$high', '$low', '$volume']
        )
        
        if data is not None and not data.empty:
            # 重命名列
            data.columns = ['close', 'open', 'high', 'low', 'volume']
            return data
        else:
            print("未获取到数据")
            return None
            
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None


def calculate_ma_signals(data, short_window=5, long_window=20):
    """
    计算均线交叉信号
    
    Args:
        data: 价格数据
        short_window: 短期均线周期
        long_window: 长期均线周期
    
    Returns:
        信号DataFrame，1表示买入，-1表示卖出，0表示无信号
    """
    signals = pd.DataFrame(0, index=data.index, columns=data.columns)
    
    for col in data.columns:
        if col == 'close':
            continue
            
        # 计算均线
        short_ma = data[col].rolling(window=short_window).mean()
        long_ma = data[col].rolling(window=long_window).mean()
        
        # 计算均线差值
        diff = short_ma - long_ma
        
        # 计算交叉信号
        for i in range(1, len(diff)):
            if pd.notna(diff.iloc[i-1]) and pd.notna(diff.iloc[i]):
                # 金叉：短期均线从下方穿越长期均线
                if diff.iloc[i-1] < 0 and diff.iloc[i] > 0:
                    signals.iloc[i, signals.columns.get_loc(col)] = 1
                # 死叉：短期均线从上方穿越长期均线
                elif diff.iloc[i-1] > 0 and diff.iloc[i] < 0:
                    signals.iloc[i, signals.columns.get_loc(col)] = -1
    
    return signals


def calculate_returns(data, signals, initial_capital=100000):
    """
    计算策略收益
    
    Args:
        data: 价格数据
        signals: 信号数据
        initial_capital: 初始资金
    
    Returns:
        收益数据
    """
    # 计算日收益率
    returns = data.pct_change()
    
    # 策略收益（假设每次信号产生1%的收益）
    strategy_returns = signals * 0.01
    
    # 累计收益
    cumulative_returns = strategy_returns.sum(axis=1).cumsum()
    
    # 资金曲线
    capital_curve = initial_capital * (1 + cumulative_returns)
    
    return {
        'strategy_returns': strategy_returns,
        'cumulative_returns': cumulative_returns,
        'capital_curve': capital_curve
    }


def analyze_strategy(signals, returns_data):
    """
    分析策略表现
    
    Args:
        signals: 信号数据
        returns_data: 收益数据
    """
    print("=" * 50)
    print("均线交叉策略分析结果")
    print("=" * 50)
    
    # 信号统计
    buy_signals = (signals == 1).sum().sum()
    sell_signals = (signals == -1).sum().sum()
    
    print(f"买入信号数量: {buy_signals}")
    print(f"卖出信号数量: {sell_signals}")
    print(f"总信号数量: {buy_signals + sell_signals}")
    
    # 收益统计
    cumulative_returns = returns_data['cumulative_returns']
    capital_curve = returns_data['capital_curve']
    
    total_return = cumulative_returns.iloc[-1]
    annual_return = total_return / (len(cumulative_returns) / 252)
    
    print(f"\n收益统计:")
    print(f"总收益率: {total_return:.2%}")
    print(f"年化收益率: {annual_return:.2%}")
    print(f"最终资金: {capital_curve.iloc[-1]:,.0f}")
    
    # 风险统计
    daily_returns = returns_data['strategy_returns'].sum(axis=1)
    volatility = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility > 0 else 0
    
    print(f"\n风险统计:")
    print(f"年化波动率: {volatility:.2%}")
    print(f"夏普比率: {sharpe_ratio:.2f}")
    print(f"胜率: {(daily_returns > 0).mean():.2%}")


def plot_results(data, signals, returns_data, stock_code):
    """
    绘制结果图表
    
    Args:
        data: 价格数据
        signals: 信号数据
        returns_data: 收益数据
        stock_code: 股票代码
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # 绘制价格和均线
    axes[0].plot(data.index, data[stock_code], label='收盘价', alpha=0.7)
    short_ma = data[stock_code].rolling(window=5).mean()
    long_ma = data[stock_code].rolling(window=20).mean()
    axes[0].plot(data.index, short_ma, label='5日均线', alpha=0.8)
    axes[0].plot(data.index, long_ma, label='20日均线', alpha=0.8)
    
    # 标记买卖信号
    buy_signals = signals[stock_code] == 1
    sell_signals = signals[stock_code] == -1
    
    axes[0].scatter(data.index[buy_signals], data.loc[buy_signals, stock_code], 
                   color='red', marker='^', s=100, label='买入信号', alpha=0.8)
    axes[0].scatter(data.index[sell_signals], data.loc[sell_signals, stock_code], 
                   color='green', marker='v', s=100, label='卖出信号', alpha=0.8)
    
    axes[0].set_title(f'{stock_code} 价格走势与均线交叉信号')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 绘制累计收益
    axes[1].plot(returns_data['cumulative_returns'].index, 
                returns_data['cumulative_returns'].values, 
                label='累计收益', color='blue')
    axes[1].set_title('策略累计收益')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # 绘制资金曲线
    axes[2].plot(returns_data['capital_curve'].index, 
                returns_data['capital_curve'].values, 
                label='资金曲线', color='green')
    axes[2].set_title('资金曲线')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ma_cross_strategy_results.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """
    主函数
    """
    print("开始运行均线交叉策略...")
    
    # 初始化qlib
    if not init_qlib():
        return
    
    # 策略参数
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    short_window = 5
    long_window = 20
    initial_capital = 100000
    
    # 获取股票列表
    try:
        instruments = D.list_instruments(instruments="csi300", start_time=start_date, end_time=end_date)
        print(f"获取到 {len(instruments)} 只股票")
        
        # 选择前5只股票进行演示
        demo_instruments = instruments[:5]
        print(f"选择演示股票: {demo_instruments}")
        
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        # 使用默认股票列表
        demo_instruments = ['000001.SZ', '000002.SZ', '000858.SZ', '002415.SZ', '600036.SH']
        print(f"使用默认股票列表: {demo_instruments}")
    
    # 获取价格数据
    data = get_stock_data(demo_instruments, start_date, end_date)
    
    if data is None:
        print("无法获取数据，程序退出")
        return
    
    print(f"获取到价格数据，形状: {data.shape}")
    
    # 计算均线信号
    signals = calculate_ma_signals(data, short_window, long_window)
    
    # 计算收益
    returns_data = calculate_returns(data, signals, initial_capital)
    
    # 分析策略
    analyze_strategy(signals, returns_data)
    
    # 保存结果
    signals.to_csv("ma_cross_signals.csv")
    returns_data['cumulative_returns'].to_csv("ma_cross_cumulative_returns.csv")
    returns_data['capital_curve'].to_csv("ma_cross_capital_curve.csv")
    
    print("\n结果已保存到CSV文件:")
    print("- ma_cross_signals.csv: 买卖信号")
    print("- ma_cross_cumulative_returns.csv: 累计收益")
    print("- ma_cross_capital_curve.csv: 资金曲线")
    
    # 绘制图表（选择第一只股票）
    if len(demo_instruments) > 0:
        try:
            plot_results(data, signals, returns_data, demo_instruments[0])
            print("图表已保存为 ma_cross_strategy_results.png")
        except Exception as e:
            print(f"绘制图表失败: {e}")
    
    print("\n策略回测完成！")


if __name__ == "__main__":
    main() 