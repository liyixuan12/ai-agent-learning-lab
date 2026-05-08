# Topic 1: Coding Basics

# 主题 1：编程基础

## Goal

## 学习目标

My goal is to learn Python coding basics for building a Financial AI Demo.  
我的目标是学习 Python 编程基础，为后续搭建金融 AI Demo 做准备。

By the end of this topic, I should be able to:  
完成本主题后，我应该能够：

- Use variables and basic data types  
使用变量和基础数据类型
- Work with lists and dictionaries  
使用列表和字典
- Write if statements for simple decision-making  
使用 if 条件判断进行简单决策
- Use loops to process multiple companies or stock prices  
使用循环批量处理多家公司或股票价格
- Write functions to reuse analysis logic  
编写函数复用分析逻辑
- Understand basic object-oriented programming concepts  
理解基础面向对象编程概念

---

## Why this topic matters for my Financial AI Demo

## 为什么这个主题对我的金融 AI Demo 很重要

Coding basics are the foundation of every AI application.  
编程基础是所有 AI 应用的基础。

In a Financial AI Demo, I need Python basics to:  
在金融 AI Demo 中，我需要用 Python 基础能力来：

- Store company information  
存储公司信息
- Process stock prices and financial indicators  
处理股票价格和财务指标
- Classify company growth and risk levels  
判断公司的增长水平和风险等级
- Generate structured analysis outputs  
生成结构化分析结果
- Prepare data for API, RAG, and LLM-based applications  
为 API、RAG 和基于 LLM 的应用准备数据

This topic is not about writing complex algorithms.  
这个主题的重点不是写复杂算法。

The main purpose is to build the ability to write clear, reusable, and understandable Python code for a real AI product demo.  
主要目的是培养为真实 AI 产品 Demo 编写清晰、可复用、易理解 Python 代码的能力。

---

# 1. Variables

# 1. 变量

## What I learned

## 我学到了什么

Variables are used to store data.  
变量用于存储数据。

In Python, I can create variables without declaring their types in advance.  
在 Python 中，我可以不提前声明数据类型，直接创建变量。

Example:  
示例：

```python
company_name = "Apple"
stock_price = 185.6
market_cap = 2900000000000
is_tech_company = True
```

In this example:  
在这个例子中：

- `company_name` stores a company name  
`company_name` 存储公司名称
- `stock_price` stores the current stock price  
`stock_price` 存储当前股票价格
- `market_cap` stores the market capitalization  
`market_cap` 存储市值
- `is_tech_company` stores a boolean value  
`is_tech_company` 存储布尔值

## My understanding

## 我的理解

Variables are like containers for information.  
变量就像存放信息的容器。

In a financial AI application, variables can store company names, stock prices, financial ratios, user questions, and AI-generated answers.  
在金融 AI 应用中，变量可以用来存储公司名称、股票价格、财务比率、用户问题和 AI 生成的答案。

Good variable names are important because they make the code easier to read.  
好的变量命名很重要，因为它可以让代码更容易阅读。

For example:  
例如：

```python
revenue_growth = 0.12
```

is better than:  
比下面这种写法更好：

```python
x = 0.12
```

because `revenue_growth` clearly shows what the variable means.  
因为 `revenue_growth` 能清楚表达变量的含义。

---

## Exercise 1: Company Basic Information

## 练习 1：公司基础信息

### Task

### 任务

Create variables for a company and print a simple sentence.  
为一家公司创建变量，并输出一句简单介绍。

Company information:  
公司信息：

- Company name: Apple  
公司名称：Apple
- Stock price: 185.6  
股票价格：185.6
- Market cap: 2900000000000  
市值：2900000000000
- Technology company: True  
是否科技公司：True
- Revenue growth: 0.08  
年收入增长率：0.08

### My Code

### 我的代码

```python
company_name = "Apple"
stock_price = 185.6
market_cap = 2900000000000
is_tech_company = True
revenue_growth = 0.08

print(f"{company_name} is a technology company. Current stock price is {stock_price}.")
```

### Output

### 输出结果

```text
Apple is a technology company. Current stock price is 185.6.
```

### What I learned

### 我学到了什么

- How to create variables  
如何创建变量
- How to store different types of information  
如何存储不同类型的信息
- How to use f-string formatting  
如何使用 f-string 格式化输出

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to store and display basic company profile information.  
这可以用于存储和展示公司的基础信息。

---

# 2. Data Types

# 2. 数据类型

## What I learned

## 我学到了什么

Python has several common data types.  
Python 有几种常见的数据类型。


| English    | 中文  | Python Type | Example             | Financial Use Case              |
| ---------- | --- | ----------- | ------------------- | ------------------------------- |
| Integer    | 整数  | `int`       | `2026`              | Year, number of shares          |
| Float      | 小数  | `float`     | `185.6`             | Stock price, revenue growth     |
| String     | 字符串 | `str`       | `"Apple"`           | Company name, sector            |
| Boolean    | 布尔值 | `bool`      | `True`              | Whether a company is profitable |
| List       | 列表  | `list`      | `[180, 182, 185]`   | Stock price history             |
| Dictionary | 字典  | `dict`      | `{"name": "Apple"}` | Company profile                 |


For my current goal, the most important data types are:  
对于我当前的目标，最重要的数据类型是：

- `str`  
字符串
- `int` and `float`  
整数和小数
- `list`  
列表
- `dict`  
字典

---

## 2.1 List

## 2.1 列表

A list is used to store multiple values.  
列表用于存储多个值。

Example:  
示例：

```python
stock_prices = [180.5, 181.2, 183.0, 179.8, 185.6]
```

Common operations:  
常见操作：

```python
print(stock_prices[0])       # first value / 第一个值
print(stock_prices[-1])      # last value / 最后一个值
print(len(stock_prices))     # length / 长度
print(max(stock_prices))     # maximum value / 最大值
print(min(stock_prices))     # minimum value / 最小值
```

## My understanding

## 我的理解

Lists are useful when I need to store a sequence of values.  
当我需要存储一组连续数据时，列表非常有用。

In finance, lists can be used to store stock prices, daily returns, or multiple company names.  
在金融场景中，列表可以用来存储股票价格、每日收益率或多个公司名称。

---

## Exercise 2: Stock Price List

## 练习 2：股票价格列表

### Task

### 任务

Given a list of stock prices, calculate:  
给定一个股票价格列表，计算：

1. Highest price
  最高价格
2. Lowest price
  最低价格
3. Average price
  平均价格
4. Last price
  最后一天价格

### My Code

### 我的代码

```python
prices = [180.5, 181.2, 183.0, 179.8, 185.6]

highest_price = max(prices)
lowest_price = min(prices)
average_price = sum(prices) / len(prices)
last_price = prices[-1]

print("Highest price:", highest_price)
print("Lowest price:", lowest_price)
print("Average price:", average_price)
print("Last price:", last_price)
```

### Output

### 输出结果

```text
Highest price: 185.6
Lowest price: 179.8
Average price: 182.02
Last price: 185.6
```

### What I learned

### 我学到了什么

- How to access values in a list  
如何访问列表中的值
- How to calculate maximum, minimum, and average values  
如何计算最大值、最小值和平均值
- How to use negative indexing  
如何使用负数索引

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to analyze stock price history and generate basic financial indicators.  
这可以用于分析股票价格历史，并生成基础金融指标。

---

## 2.2 Dictionary

## 2.2 字典

A dictionary stores data as key-value pairs.  
字典以键值对的形式存储数据。

Example:  
示例：

```python
company = {
    "name": "NVIDIA",
    "ticker": "NVDA",
    "sector": "Semiconductor",
    "price": 900.5,
    "is_ai_company": True
}
```

Access values:  
访问数据：

```python
print(company["name"])
print(company["sector"])
```

Update values:  
更新数据：

```python
company["price"] = 920.0
```

Add new values:  
添加新数据：

```python
company["country"] = "USA"
```

## My understanding

## 我的理解

Dictionaries are very useful for storing structured information.  
字典非常适合存储结构化信息。

In a financial AI application, one company can be represented as one dictionary.  
在金融 AI 应用中，一家公司可以用一个字典表示。

---

## Exercise 3: Company Dictionary

## 练习 3：公司信息字典

### Task

### 任务

Create a dictionary for NVIDIA and print a summary sentence.  
为 NVIDIA 创建一个字典，并输出一句总结。

### My Code

### 我的代码

```python
company = {
    "name": "NVIDIA",
    "ticker": "NVDA",
    "sector": "Semiconductor",
    "price": 900.5,
    "is_ai_company": True
}

print(f"{company['name']} belongs to {company['sector']} sector.")
```

### Output

### 输出结果

```text
NVIDIA belongs to Semiconductor sector.
```

### What I learned

### 我学到了什么

- How to create a dictionary  
如何创建字典
- How to access dictionary values using keys  
如何通过 key 访问字典中的值
- How to store structured company information  
如何存储结构化公司信息

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to store company profiles before sending them to an AI analysis module.  
这可以用于在发送给 AI 分析模块之前存储公司资料。

---

# 3. If Statements

# 3. 条件判断

## What I learned

## 我学到了什么

If statements allow the program to make decisions.  
if 条件判断可以让程序做决策。

Example:  
示例：

```python
daily_return = 0.03

if daily_return > 0:
    print("Stock price increased.")
else:
    print("Stock price decreased.")
```

In finance, if statements can be used to judge:  
在金融场景中，if 判断可以用于判断：

- Whether a stock price increased or decreased  
股票价格是上涨还是下跌
- Whether a company has high growth  
公司是否高增长
- Whether a company has high risk  
公司是否高风险
- Whether a financial ratio is healthy  
某个财务比率是否健康

Common comparison operators:  
常见比较运算符：


| Operator | Meaning                  | 中文   |
| -------- | ------------------------ | ---- |
| `>`      | greater than             | 大于   |
| `<`      | less than                | 小于   |
| `>=`     | greater than or equal to | 大于等于 |
| `<=`     | less than or equal to    | 小于等于 |
| `==`     | equal to                 | 等于   |
| `!=`     | not equal to             | 不等于  |


Logical operators:  
逻辑运算符：


| Operator | Meaning                        | 中文       |
| -------- | ------------------------------ | -------- |
| `and`    | both conditions are true       | 两个条件都满足  |
| `or`     | at least one condition is true | 至少满足一个条件 |
| `not`    | reverse the condition          | 取反       |


---

## Exercise 4: Stock Price Movement

## 练习 4：判断股票涨跌

### Task

### 任务

Given yesterday's price and today's price, decide whether the stock increased, decreased, or stayed the same.  
给定昨日价格和今日价格，判断股票上涨、下跌还是持平。

### My Code

### 我的代码

```python
yesterday_price = 180
today_price = 185

if today_price > yesterday_price:
    print("Stock price increased.")
elif today_price < yesterday_price:
    print("Stock price decreased.")
else:
    print("Stock price stayed the same.")
```

### Output

### 输出结果

```text
Stock price increased.
```

### What I learned

### 我学到了什么

- How to use `if`, `elif`, and `else`  
如何使用 `if`、`elif` 和 `else`
- How to compare two numbers  
如何比较两个数字
- How to write basic decision logic  
如何编写基础判断逻辑

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to generate simple market movement descriptions.  
这可以用于生成简单的市场涨跌描述。

---

## Exercise 5: Revenue Growth Classification

## 练习 5：营收增长分类

### Task

### 任务

Classify company growth based on revenue growth.  
根据营收增长率判断公司的增长水平。

Rules:  
规则：

- `> 0.2`: High growth  
高增长
- `>= 0.05`: Moderate growth  
中等增长
- Otherwise: Low growth  
其他情况：低增长

### My Code

### 我的代码

```python
revenue_growth = 0.12

if revenue_growth > 0.2:
    print("High growth")
elif revenue_growth >= 0.05:
    print("Moderate growth")
else:
    print("Low growth")
```

### Output

### 输出结果

```text
Moderate growth
```

### What I learned

### 我学到了什么

- How to classify numerical values  
如何对数值进行分类
- How to write multiple conditions  
如何编写多条件判断
- How business rules can be translated into code  
如何把业务规则转换成代码

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to classify companies into different growth categories.  
这可以用于将公司划分为不同的增长类型。

---

## Exercise 6: Simple Risk Classification

## 练习 6：简单风险判断

### Task

### 任务

Classify company risk using PE ratio and debt ratio.  
使用市盈率和负债率判断公司风险。

Rules:  
规则：

- If `PE > 40` and `debt_ratio > 0.6`: High risk  
如果 `PE > 40` 且 `debt_ratio > 0.6`：高风险
- If `PE > 40` or `debt_ratio > 0.6`: Medium risk  
如果 `PE > 40` 或 `debt_ratio > 0.6`：中等风险
- Otherwise: Low risk  
否则：低风险

### My Code

### 我的代码

```python
pe_ratio = 45
debt_ratio = 0.7

if pe_ratio > 40 and debt_ratio > 0.6:
    print("High risk")
elif pe_ratio > 40 or debt_ratio > 0.6:
    print("Medium risk")
else:
    print("Low risk")
```

### Output

### 输出结果

```text
High risk
```

### What I learned

### 我学到了什么

- How to combine multiple conditions  
如何组合多个条件
- How to use `and` and `or`  
如何使用 `and` 和 `or`
- How to convert financial logic into Python code  
如何把金融判断逻辑转换成 Python 代码

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used as a simple rule-based risk analysis module.  
这可以作为一个简单的规则型风险分析模块。

---

# 4. Loops

# 4. 循环

## What I learned

## 我学到了什么

Loops are used to repeat actions.  
循环用于重复执行操作。

In a financial AI application, loops can be used to process:  
在金融 AI 应用中，循环可以用于处理：

- Multiple companies  
多家公司
- Multiple stock prices  
多个股票价格
- Multiple financial indicators  
多个财务指标
- Multiple documents or news articles  
多篇文档或新闻

Example:  
示例：

```python
stocks = ["AAPL", "MSFT", "NVDA"]

for stock in stocks:
    print(stock)
```

## My understanding

## 我的理解

A loop helps me avoid writing repeated code manually.  
循环可以帮助我避免手动重复写代码。

If I have 100 companies, I can use a loop to analyze all of them automatically.  
如果我有 100 家公司，我可以用循环自动分析它们。

---

## Exercise 7: Analyze Multiple Stocks

## 练习 7：批量输出股票代码

### Task

### 任务

Print an analysis message for each stock.  
为每只股票输出一条分析信息。

### My Code

### 我的代码

```python
stocks = ["AAPL", "MSFT", "NVDA", "TSLA"]

for stock in stocks:
    print(f"Analyzing {stock}")
```

### Output

### 输出结果

```text
Analyzing AAPL
Analyzing MSFT
Analyzing NVDA
Analyzing TSLA
```

### What I learned

### 我学到了什么

- How to loop through a list  
如何遍历列表
- How to repeat the same action for multiple items  
如何对多个对象重复执行同一个操作

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to analyze multiple companies automatically.  
这可以用于自动分析多家公司。

---

## Exercise 8: Calculate Daily Returns

## 练习 8：计算每日收益率

### Task

### 任务

Given stock prices, calculate the return from one day to the next.  
给定股票价格，计算相邻两天之间的收益率。

### My Code

### 我的代码

```python
prices = [100, 105, 103, 108]

for i in range(1, len(prices)):
    daily_return = (prices[i] - prices[i - 1]) / prices[i - 1]
    print(f"Day {i} return: {daily_return:.2%}")
```

### Output

### 输出结果

```text
Day 1 return: 5.00%
Day 2 return: -1.90%
Day 3 return: 4.85%
```

### What I learned

### 我学到了什么

- How to use `range()`  
如何使用 `range()`
- How to access current and previous values in a list  
如何访问列表中的当前值和前一个值
- How to calculate daily return  
如何计算每日收益率
- How to format numbers as percentages  
如何将数字格式化为百分比

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to calculate stock return indicators from historical price data.  
这可以用于根据历史价格数据计算股票收益指标。

---

## Exercise 9: Filter High-Growth Companies

## 练习 9：筛选高增长公司

### Task

### 任务

Given a list of companies, print companies with revenue growth greater than 15%.  
给定一个公司列表，输出营收增长率大于 15% 的公司。

### My Code

### 我的代码

```python
companies = [
    {"name": "Apple", "growth": 0.08},
    {"name": "NVIDIA", "growth": 0.35},
    {"name": "Tesla", "growth": 0.18},
    {"name": "Intel", "growth": -0.02}
]

for company in companies:
    if company["growth"] > 0.15:
        print(company["name"])
```

### Output

### 输出结果

```text
NVIDIA
Tesla
```

### What I learned

### 我学到了什么

- How to loop through a list of dictionaries  
如何遍历字典列表
- How to combine loops and if statements  
如何结合循环和条件判断
- How to filter data based on rules  
如何根据规则筛选数据

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to filter companies that meet certain financial criteria.  
这可以用于筛选符合特定财务条件的公司。

---

# 5. Functions

# 5. 函数

## What I learned

## 我学到了什么

Functions are used to organize and reuse code.  
函数用于组织和复用代码。

Example:  
示例：

```python
def calculate_return(old_price, new_price):
    return (new_price - old_price) / old_price
```

Call the function:  
调用函数：

```python
result = calculate_return(100, 105)
print(result)
```

## My understanding

## 我的理解

Functions help make code cleaner and easier to maintain.  
函数可以让代码更清晰，也更容易维护。

In a Financial AI Demo, many steps should be written as functions, such as:  
在金融 AI Demo 中，很多步骤都应该写成函数，例如：

```python
load_data()
clean_data()
calculate_metrics()
classify_risk()
generate_summary()
```

---

## Exercise 10: Return Calculation Function

## 练习 10：收益率计算函数

### Task

### 任务

Write a function to calculate return based on old price and new price.  
写一个函数，根据旧价格和新价格计算收益率。

### My Code

### 我的代码

```python
def calculate_return(old_price, new_price):
    return_rate = (new_price - old_price) / old_price
    return return_rate


result = calculate_return(100, 105)
print(f"Return: {result:.2%}")
```

### Output

### 输出结果

```text
Return: 5.00%
```

### What I learned

### 我学到了什么

- How to define a function  
如何定义函数
- How to pass parameters into a function  
如何向函数传入参数
- How to return a result  
如何返回结果

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used as a reusable function for stock return analysis.  
这可以作为股票收益分析中的可复用函数。

---

## Exercise 11: Risk Classification Function

## 练习 11：风险分类函数

### Task

### 任务

Write a function to classify risk based on PE ratio and debt ratio.  
写一个函数，根据市盈率和负债率判断风险等级。

### My Code

### 我的代码

```python
def classify_risk(pe_ratio, debt_ratio):
    if pe_ratio > 40 and debt_ratio > 0.6:
        return "High risk"
    elif pe_ratio > 40 or debt_ratio > 0.6:
        return "Medium risk"
    else:
        return "Low risk"


risk = classify_risk(45, 0.7)
print(risk)
```

### Output

### 输出结果

```text
High risk
```

### What I learned

### 我学到了什么

- How to put business rules into a function  
如何把业务规则写进函数
- How to return different results based on conditions  
如何根据不同条件返回不同结果
- How to make risk analysis logic reusable  
如何让风险分析逻辑可复用

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used as a basic rule-based financial risk module.  
这可以作为一个基础的规则型金融风险模块。

---

## Exercise 12: Company Summary Function

## 练习 12：公司摘要生成函数

### Task

### 任务

Write a function to generate a company analysis summary.  
写一个函数，生成公司分析摘要。

### My Code

### 我的代码

```python
def generate_summary(company_name, revenue_growth, risk_level):
    summary = f"{company_name} has a revenue growth of {revenue_growth:.2%}. Risk level: {risk_level}."
    return summary


text = generate_summary("NVIDIA", 0.35, "Medium risk")
print(text)
```

### Output

### 输出结果

```text
NVIDIA has a revenue growth of 35.00%. Risk level: Medium risk.
```

### What I learned

### 我学到了什么

- How to generate structured text with Python  
如何用 Python 生成结构化文本
- How to combine variables into a readable summary  
如何把变量组合成可读的摘要
- How coding connects to AI-generated reporting  
编程如何和 AI 报告生成场景连接起来

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to generate a simple company analysis report before adding LLM capabilities.  
这可以在接入 LLM 之前，用于生成简单的公司分析报告。

---

# 6. Object-Oriented Programming

# 6. 面向对象编程

## What I learned

## 我学到了什么

Object-oriented programming means organizing data and functions into classes and objects.  
面向对象编程是指把数据和功能组织到类和对象中。

Example:  
示例：

```python
class Company:
    def __init__(self, name, ticker, sector, price):
        self.name = name
        self.ticker = ticker
        self.sector = sector
        self.price = price
```

Create an object:  
创建对象：

```python
apple = Company("Apple", "AAPL", "Technology", 185.6)
print(apple.name)
```

Important concepts:  
重要概念：


| English    | 中文    | Meaning                                  |
| ---------- | ----- | ---------------------------------------- |
| Class      | 类     | A template                               |
| Object     | 对象    | A specific instance created from a class |
| Attribute  | 属性    | Data stored inside an object             |
| Method     | 方法    | A function inside a class                |
| `__init__` | 初始化方法 | Runs when an object is created           |
| `self`     | 当前对象  | Refers to the current object             |


## My understanding

## 我的理解

OOP is useful when a project becomes larger.  
当项目变大时，面向对象编程会很有用。

For my current stage, I do not need to master advanced OOP.  
在我当前阶段，我不需要掌握非常高级的 OOP。

I only need to understand how classes can organize financial data and analysis functions.  
我只需要理解类如何组织金融数据和分析功能。

---

## Exercise 13: Create a Company Class

## 练习 13：创建 Company 类

### Task

### 任务

Create a `Company` class with name, ticker, sector, and price.  
创建一个 `Company` 类，包含公司名称、股票代码、行业和价格。

### My Code

### 我的代码

```python
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
```

### Output

### 输出结果

```text
NVIDIA
NVDA
Semiconductor
900.5
```

### What I learned

### 我学到了什么

- How to create a class  
如何创建类
- How to create an object  
如何创建对象
- How to store company information as object attributes  
如何把公司信息存储为对象属性

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to represent each company as a structured object.  
这可以用于把每家公司表示成结构化对象。

---

## Exercise 14: Add a Method to Company Class

## 练习 14：给 Company 类添加方法

### Task

### 任务

Add a method called `show_summary()` to the `Company` class.  
给 `Company` 类添加一个叫 `show_summary()` 的方法。

### My Code

### 我的代码

```python
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
```

### Output

### 输出结果

```text
NVIDIA (NVDA) belongs to Semiconductor sector.
```

### What I learned

### 我学到了什么

- How to define a method inside a class  
如何在类中定义方法
- How to use object attributes inside a method  
如何在方法中使用对象属性
- How to generate a summary from object data  
如何根据对象数据生成摘要

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can be used to create company-level summary outputs.  
这可以用于生成公司层面的摘要输出。

---

## Exercise 15: FinancialAnalyzer Class

## 练习 15：FinancialAnalyzer 分析类

### Task

### 任务

Create a `FinancialAnalyzer` class with a method to calculate stock return.  
创建一个 `FinancialAnalyzer` 类，并添加一个计算股票收益率的方法。

### My Code

### 我的代码

```python
class FinancialAnalyzer:
    def calculate_return(self, old_price, new_price):
        return (new_price - old_price) / old_price


analyzer = FinancialAnalyzer()
result = analyzer.calculate_return(100, 105)

print(f"Return: {result:.2%}")
```

### Output

### 输出结果

```text
Return: 5.00%
```

### What I learned

### 我学到了什么

- How to create an analyzer class  
如何创建一个分析类
- How to put analysis logic into a method  
如何把分析逻辑放进方法中
- How OOP can be used to organize financial analysis functions  
面向对象编程如何用于组织金融分析功能

### Possible use in my Financial AI Demo

### 在我的金融 AI Demo 中的应用

This can become the starting point of a financial analysis module.  
这可以作为金融分析模块的起点。

---

# Final Mini Project: Company Growth and Risk Analyzer

# 最终小项目：公司增长与风险分析器

## Project Goal

## 项目目标

Build a small Python program that analyzes multiple companies based on simple financial indicators.  
构建一个小型 Python 程序，根据简单财务指标分析多家公司。

The program should:  
这个程序应该能够：

1. Store company information
  存储公司信息
2. Classify company growth level
  判断公司增长水平
3. Classify company risk level
  判断公司风险等级
4. Generate a structured company summary
  生成结构化公司分析摘要

---

## Given Data

## 给定数据

```python
companies = [
    {
        "name": "Apple",
        "ticker": "AAPL",
        "sector": "Technology",
        "revenue_growth": 0.08,
        "pe_ratio": 28,
        "debt_ratio": 0.35
    },
    {
        "name": "NVIDIA",
        "ticker": "NVDA",
        "sector": "Semiconductor",
        "revenue_growth": 0.35,
        "pe_ratio": 55,
        "debt_ratio": 0.25
    },
    {
        "name": "Tesla",
        "ticker": "TSLA",
        "sector": "Automotive",
        "revenue_growth": 0.18,
        "pe_ratio": 45,
        "debt_ratio": 0.65
    }
]
```

---

## My Code

## 我的代码

```python
companies = [
    {
        "name": "Apple",
        "ticker": "AAPL",
        "sector": "Technology",
        "revenue_growth": 0.08,
        "pe_ratio": 28,
        "debt_ratio": 0.35
    },
    {
        "name": "NVIDIA",
        "ticker": "NVDA",
        "sector": "Semiconductor",
        "revenue_growth": 0.35,
        "pe_ratio": 55,
        "debt_ratio": 0.25
    },
    {
        "name": "Tesla",
        "ticker": "TSLA",
        "sector": "Automotive",
        "revenue_growth": 0.18,
        "pe_ratio": 45,
        "debt_ratio": 0.65
    }
]


def classify_growth(revenue_growth):
    if revenue_growth > 0.2:
        return "High growth"
    elif revenue_growth >= 0.05:
        return "Moderate growth"
    else:
        return "Low growth"


def classify_risk(pe_ratio, debt_ratio):
    if pe_ratio > 40 and debt_ratio > 0.6:
        return "High risk"
    elif pe_ratio > 40 or debt_ratio > 0.6:
        return "Medium risk"
    else:
        return "Low risk"


def generate_company_summary(company):
    growth_level = classify_growth(company["revenue_growth"])
    risk_level = classify_risk(company["pe_ratio"], company["debt_ratio"])

    summary = (
        f"{company['name']} ({company['ticker']}) is in {company['sector']} sector. "
        f"Growth: {growth_level}. Risk: {risk_level}."
    )

    return summary


for company in companies:
    print(generate_company_summary(company))
```

---

## Output

## 输出结果

```text
Apple (AAPL) is in Technology sector. Growth: Moderate growth. Risk: Low risk.
NVIDIA (NVDA) is in Semiconductor sector. Growth: High growth. Risk: Medium risk.
Tesla (TSLA) is in Automotive sector. Growth: Moderate growth. Risk: High risk.
```

---

## What I learned from this mini project

## 我从这个小项目中学到了什么

Through this mini project, I learned how to combine variables, dictionaries, if statements, loops, and functions into a small financial analysis program.  
通过这个小项目，我学会了如何把变量、字典、条件判断、循环和函数组合成一个小型金融分析程序。

I also learned that a simple rule-based program can already produce structured financial summaries.  
我也理解到，即使是简单的规则型程序，也可以生成结构化的金融分析摘要。

This is a useful foundation before adding more advanced AI features such as RAG, LLM APIs, and automatic report generation.  
这为后续加入 RAG、LLM API 和自动报告生成等更高级的 AI 功能打下了基础。

---

## Product Thinking

## 产品思考

This mini project can be seen as the first version of a financial analysis engine.  
这个小项目可以被看作金融分析引擎的第一版。

In a real Financial AI Demo, this logic could be expanded in the following ways:  
在真实的金融 AI Demo 中，这套逻辑可以进一步扩展为：

- Replace manually written company data with real financial data  
用真实金融数据替代手动填写的公司数据
- Add more indicators such as profit margin, cash flow, and volatility  
加入更多指标，例如利润率、现金流和波动率
- Store company data in a database  
将公司数据存入数据库
- Use RAG to retrieve related financial documents  
使用 RAG 检索相关金融文档
- Use an LLM to generate more detailed company analysis reports  
使用 LLM 生成更详细的公司分析报告
- Build an API with FastAPI  
使用 FastAPI 构建接口
- Build a simple web interface with Streamlit  
使用 Streamlit 构建简单网页界面

---

## Reflection

## 学习反思

At this stage, I do not need to master advanced algorithms.  
在这个阶段，我不需要掌握高级算法。

The most important thing is to become comfortable with basic Python syntax and learn how to use code to solve small business problems.  
最重要的是熟悉 Python 基础语法，并学会用代码解决小型业务问题。

For my Financial AI Demo, the most important coding basics are:  
对于我的金融 AI Demo 来说，最重要的编程基础是：

- Lists and dictionaries  
列表和字典
- If statements  
条件判断
- Loops  
循环
- Functions  
函数
- Basic project organization  
基础项目组织能力

After completing this topic, I am ready to move on to Topic 2: Software Architecture.  
完成这个主题后，我可以进入主题 2：软件架构。

---

# Next Step

# 下一步

The next topic is:  
下一个主题是：

## Topic 2: Software Architecture

## 主题 2：软件架构

In Topic 2, I will learn how to structure a real AI application, including APIs, data flow, databases, testing, and deployment.  
在主题 2 中，我将学习如何组织一个真实 AI 应用，包括 API、数据流、数据库、测试和部署。