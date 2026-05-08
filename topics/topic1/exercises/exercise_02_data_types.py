# Exercise 2: Stock Price List
# 练习 2：股票价格列表

prices = [180.5, 181.2, 183.0, 179.8, 185.6]

highest_price = max(prices)
lowest_price = min(prices)
average_price = sum(prices) / len(prices)
last_price = prices[-1]

print("Highest price:", highest_price)
print("Lowest price:", lowest_price)
print("Average price:", average_price)
print("Last price:", last_price)

print()

# Exercise 3: Company Dictionary
# 练习 3：公司信息字典

company = {
    "name": "NVIDIA",
    "ticker": "NVDA",
    "sector": "Semiconductor",
    "price": 900.5,
    "is_ai_company": True,
}

print(f"{company['name']} belongs to {company['sector']} sector.")
