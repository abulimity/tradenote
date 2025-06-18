# 均线交叉策略 (Moving Average Crossover Strategy)

## 策略概述

这是一个基于qlib框架实现的均线交叉策略，核心逻辑是：
- **金叉买入**：短期均线上穿长期均线时买入
- **死叉卖出**：短期均线下穿长期均线时卖出

## 文件说明

### 1. `ma_cross_strategy.py`
完整的策略实现，包含：
- `MACrossStrategy` 类：继承自qlib的TopkDropoutStrategy
- 完整的回测框架
- 结果分析和保存

### 2. `ma_cross_strategy_improved.py`
改进版本，包含：
- 更完善的数据获取逻辑
- 错误处理机制
- 简化版回测功能

### 3. `simple_ma_strategy.py` ⭐ **推荐使用**
简单实用的版本，包含：
- 清晰的数据获取和处理
- 均线信号计算
- 收益计算和分析
- 可视化图表生成
- 结果保存功能

## 使用方法

### 环境准备

1. 确保已安装qlib：
```bash
pip install pyqlib
```

2. 下载qlib数据（如果还没有）：
```bash
# 下载中国股票数据
python -m qlib.data.dump_bin --csv_path ~/.qlib/qlib_data/cn_data --include_fields close,open,high,low,volume
```

### 运行策略

#### 方法1：运行简单版本（推荐）
```bash
cd test
python simple_ma_strategy.py
```

#### 方法2：运行完整版本
```bash
cd test
python ma_cross_strategy.py
```

#### 方法3：运行改进版本
```bash
cd test
python ma_cross_strategy_improved.py
```

## 策略参数

可以在代码中修改以下参数：

```python
# 均线周期
short_window = 5    # 短期均线周期
long_window = 20    # 长期均线周期

# 回测时间
start_date = "2020-01-01"
end_date = "2023-12-31"

# 初始资金
initial_capital = 100000

# 股票池
instruments = "csi300"  # 沪深300成分股
```

## 输出结果

运行策略后会生成以下文件：

1. **CSV文件**：
   - `ma_cross_signals.csv`：买卖信号数据
   - `ma_cross_cumulative_returns.csv`：累计收益数据
   - `ma_cross_capital_curve.csv`：资金曲线数据

2. **图表文件**：
   - `ma_cross_strategy_results.png`：策略结果可视化图表

3. **控制台输出**：
   - 策略分析结果
   - 收益统计
   - 风险指标

## 策略分析指标

### 收益指标
- 总收益率
- 年化收益率
- 最终资金

### 风险指标
- 年化波动率
- 夏普比率
- 胜率
- 最大回撤

### 交易统计
- 买入信号数量
- 卖出信号数量
- 总交易次数

## 策略逻辑详解

### 1. 均线计算
```python
# 计算短期和长期均线
short_ma = price_data.rolling(window=short_window).mean()
long_ma = price_data.rolling(window=long_window).mean()
```

### 2. 交叉信号判断
```python
# 计算均线差值
diff = short_ma - long_ma

# 金叉：短期均线从下方穿越长期均线
if diff.iloc[i-1] < 0 and diff.iloc[i] > 0:
    signal = 1  # 买入信号

# 死叉：短期均线从上方穿越长期均线
elif diff.iloc[i-1] > 0 and diff.iloc[i] < 0:
    signal = -1  # 卖出信号
```

### 3. 收益计算
```python
# 策略收益（简化处理）
strategy_returns = signals * 0.01

# 累计收益
cumulative_returns = strategy_returns.sum(axis=1).cumsum()
```

## 注意事项

1. **数据依赖**：确保qlib数据已正确下载和配置
2. **参数调优**：可以根据不同市场环境调整均线周期
3. **风险控制**：实际交易中需要加入止损和仓位管理
4. **交易成本**：当前版本未考虑交易费用，实际应用需要考虑

## 扩展功能

可以基于此策略进行以下扩展：

1. **多均线策略**：使用多条均线进行更复杂的信号判断
2. **量价配合**：结合成交量指标优化信号
3. **止损机制**：添加动态止损策略
4. **仓位管理**：根据信号强度调整仓位大小
5. **多股票组合**：构建股票组合分散风险

## 常见问题

### Q: 如何修改股票池？
A: 在代码中修改 `instruments` 参数，例如：
```python
instruments = "csi500"  # 中证500
instruments = ["000001.SZ", "000002.SZ"]  # 指定股票列表
```

### Q: 如何调整均线周期？
A: 修改 `short_window` 和 `long_window` 参数：
```python
short_window = 10  # 10日均线
long_window = 30   # 30日均线
```

### Q: 如何查看详细的交易记录？
A: 查看生成的 `ma_cross_signals.csv` 文件，其中包含每日的买卖信号。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue到项目仓库
- 发送邮件到项目维护者

---

**免责声明**：本策略仅供学习和研究使用，不构成投资建议。实际投资请谨慎决策，并承担相应风险。 