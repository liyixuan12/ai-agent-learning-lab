# Exercise 10: Return Calculation Function
# 练习 10：收益率计算函数


def calculate_return(old_price, new_price):
    return_rate = (new_price - old_price) / old_price
    return return_rate


result = calculate_return(100, 105)
print(f"Return: {result:.2%}")

print()

# Exercise 11: Risk Classification Function
# 练习 11：风险分类函数


def classify_risk(pe_ratio, debt_ratio):
    if pe_ratio > 40 and debt_ratio > 0.6:
        return "High risk"
    if pe_ratio > 40 or debt_ratio > 0.6:
        return "Medium risk"
    return "Low risk"


risk = classify_risk(45, 0.7)
print(risk)

print()

# Exercise 12: Company Summary Function
# 练习 12：公司摘要生成函数


def generate_summary(company_name, revenue_growth, risk_level):
    summary = (
        f"{company_name} has a revenue growth of {revenue_growth:.2%}. "
        f"Risk level: {risk_level}."
    )
    return summary


text = generate_summary("NVIDIA", 0.35, "Medium risk")
print(text)
