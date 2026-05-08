# Exercise 7: Analyze Multiple Stocks
# 练习 7：批量输出股票代码

stocks = ["AAPL", "MSFT", "NVDA", "TSLA"]

for stock in stocks:
    print(f"Analyzing {stock}")

print()

# Exercise 8: Calculate Daily Returns
# 练习 8：计算每日收益率

prices = [100, 105, 103, 108]

for i in range(1, len(prices)):
    daily_return = (prices[i] - prices[i - 1]) / prices[i - 1]
    print(f"Day {i} return: {daily_return:.2%}")

print()

# Exercise 9: Filter High-Growth Companies
# 练习 9：筛选高增长公司

companies = [
    {"name": "Apple", "growth": 0.08},
    {"name": "NVIDIA", "growth": 0.35},
    {"name": "Tesla", "growth": 0.18},
    {"name": "Intel", "growth": -0.02},
]

for company in companies:
    if company["growth"] > 0.15:
        print(company["name"])
