# Exercise 4: Stock Price Movement
# 练习 4：判断股票涨跌

yesterday_price = 180
today_price = 185

if today_price > yesterday_price:
    print("Stock price increased.")
elif today_price < yesterday_price:
    print("Stock price decreased.")
else:
    print("Stock price stayed the same.")

print()

# Exercise 5: Revenue Growth Classification
# 练习 5：营收增长分类

revenue_growth = 0.12

if revenue_growth > 0.2:
    print("High growth")
elif revenue_growth >= 0.05:
    print("Moderate growth")
else:
    print("Low growth")

print()

# Exercise 6: Simple Risk Classification
# 练习 6：简单风险判断

pe_ratio = 45
debt_ratio = 0.7

if pe_ratio > 40 and debt_ratio > 0.6:
    print("High risk")
elif pe_ratio > 40 or debt_ratio > 0.6:
    print("Medium risk")
else:
    print("Low risk")
