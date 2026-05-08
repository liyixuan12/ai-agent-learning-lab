"""
Topic 1 exercises 1–15 (rollup). Split versions live under exercises/.
主题 1 练习 1–15 汇总，分文件版本见 exercises/ 目录。
"""

# --- Exercise 1: Company Basic Information ---
company_name = "Apple"
stock_price = 185.6
market_cap = 2900000000000
is_tech_company = True
revenue_growth = 0.08
print(f"{company_name} is a technology company. Current stock price is {stock_price}.")

print()

# --- Exercise 2: Stock Price List ---
prices = [180.5, 181.2, 183.0, 179.8, 185.6]
print("Highest price:", max(prices))
print("Lowest price:", min(prices))
print("Average price:", sum(prices) / len(prices))
print("Last price:", prices[-1])

print()

# --- Exercise 3: Company Dictionary ---
company = {
    "name": "NVIDIA",
    "ticker": "NVDA",
    "sector": "Semiconductor",
    "price": 900.5,
    "is_ai_company": True,
}
print(f"{company['name']} belongs to {company['sector']} sector.")

print()

# --- Exercise 4: Stock Price Movement ---
yesterday_price = 180
today_price = 185
if today_price > yesterday_price:
    print("Stock price increased.")
elif today_price < yesterday_price:
    print("Stock price decreased.")
else:
    print("Stock price stayed the same.")

print()

# --- Exercise 5: Revenue Growth Classification ---
rg = 0.12
if rg > 0.2:
    print("High growth")
elif rg >= 0.05:
    print("Moderate growth")
else:
    print("Low growth")

print()

# --- Exercise 6: Simple Risk Classification ---
pe_ratio = 45
debt_ratio = 0.7
if pe_ratio > 40 and debt_ratio > 0.6:
    print("High risk")
elif pe_ratio > 40 or debt_ratio > 0.6:
    print("Medium risk")
else:
    print("Low risk")

print()

# --- Exercise 7: Analyze Multiple Stocks ---
for stock in ["AAPL", "MSFT", "NVDA", "TSLA"]:
    print(f"Analyzing {stock}")

print()

# --- Exercise 8: Calculate Daily Returns ---
price_series = [100, 105, 103, 108]
for i in range(1, len(price_series)):
    dr = (price_series[i] - price_series[i - 1]) / price_series[i - 1]
    print(f"Day {i} return: {dr:.2%}")

print()

# --- Exercise 9: Filter High-Growth Companies ---
companies_growth = [
    {"name": "Apple", "growth": 0.08},
    {"name": "NVIDIA", "growth": 0.35},
    {"name": "Tesla", "growth": 0.18},
    {"name": "Intel", "growth": -0.02},
]
for c in companies_growth:
    if c["growth"] > 0.15:
        print(c["name"])

print()


def calculate_return(old_price, new_price):
    return (new_price - old_price) / old_price


# --- Exercise 10 ---
print(f"Return: {calculate_return(100, 105):.2%}")

print()


def classify_risk(pe, debt):
    if pe > 40 and debt > 0.6:
        return "High risk"
    if pe > 40 or debt > 0.6:
        return "Medium risk"
    return "Low risk"


# --- Exercise 11 ---
print(classify_risk(45, 0.7))

print()


def generate_summary(name, revenue_growth_pct, risk_level):
    return (
        f"{name} has a revenue growth of {revenue_growth_pct:.2%}. "
        f"Risk level: {risk_level}."
    )


# --- Exercise 12 ---
print(generate_summary("NVIDIA", 0.35, "Medium risk"))

print()


class Company:
    def __init__(self, name, ticker, sector, price):
        self.name = name
        self.ticker = ticker
        self.sector = sector
        self.price = price

    def show_summary(self):
        return f"{self.name} ({self.ticker}) belongs to {self.sector} sector."


# --- Exercise 13–14 (combined Company with method) ---
sample = Company("NVIDIA", "NVDA", "Semiconductor", 900.5)
print(sample.name, sample.ticker, sample.sector, sample.price, sep="\n")
print(sample.show_summary())

print()


class FinancialAnalyzer:
    def calculate_return(self, old_price, new_price):
        return (new_price - old_price) / old_price


# --- Exercise 15 ---
analyzer = FinancialAnalyzer()
print(f"Return: {analyzer.calculate_return(100, 105):.2%}")
