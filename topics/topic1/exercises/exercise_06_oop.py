# Exercise 13: Create a Company Class
# 练习 13：创建 Company 类


class Company:
    def __init__(self, name, ticker, sector, price):
        self.name = name
        self.ticker = ticker
        self.sector = sector
        self.price = price


nvidia = Company("NVIDIA", "NVDA", "Semiconductor", 900.5)

print(nvidia.name)
print(nvidia.ticker)
print(nvidia.sector)
print(nvidia.price)

print()

# Exercise 14: Add a Method to Company Class
# 练习 14：给 Company 类添加方法


class Company:
    def __init__(self, name, ticker, sector, price):
        self.name = name
        self.ticker = ticker
        self.sector = sector
        self.price = price

    def show_summary(self):
        return f"{self.name} ({self.ticker}) belongs to {self.sector} sector."


nvidia = Company("NVIDIA", "NVDA", "Semiconductor", 900.5)
print(nvidia.show_summary())

print()

# Exercise 15: FinancialAnalyzer Class
# 练习 15：FinancialAnalyzer 分析类


class FinancialAnalyzer:
    def calculate_return(self, old_price, new_price):
        return (new_price - old_price) / old_price


analyzer = FinancialAnalyzer()
ret = analyzer.calculate_return(100, 105)

print(f"Return: {ret:.2%}")
