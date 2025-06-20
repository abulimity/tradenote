import qlib
from qlib.data import D

# 初始化 Qlib
qlib.init(provider_uri="D:/project/python/tradenote/qlibz/qlib_data/cn_data", region="cn")

# 检查目标股票和基准
stock_code = "SZ000858"  # 你的BuyHold策略用的股票代码
benchmark = "SH000300"

print("--- 检查可用股票列表（前10只） ---")
print("全部股票：", list(D.instruments(market="all")))

print("--- 检查交易日（2017-01-01 ~ 2020-08-01，前10天） ---")
print(D.calendar(start_time="2017-01-01", end_time="2020-08-01")[:10])

print(f"--- 检查目标股票 {stock_code} 是否在股票池 ---")
print(stock_code in D.instruments(market="all"))

print(f"--- 检查基准 {benchmark} 是否在股票池 ---")
print(benchmark in D.instruments(market="all"))

print(f"--- 检查目标股票 {stock_code} 的行情数据（前5行） ---")
try:
    df = D.features([stock_code], ["$close", "$open", "$high", "$low", "$volume"], start_time="2017-01-01", end_time="2020-08-01")
    print(df.head())
except Exception as e:
    print(f"获取行情数据失败: {e}")

print(f"--- 检查基准 {benchmark} 的行情数据（前5行） ---")
try:
    df_bench = D.features([benchmark], ["$close"], start_time="2017-01-01", end_time="2020-08-01")
    print(df_bench.head())
except Exception as e:
    print(f"获取基准行情数据失败: {e}")
# python github/scripts/get_data.py qlib_data --target_dir D:/project/python/tradenote/qlib_data/cn_data --region cn