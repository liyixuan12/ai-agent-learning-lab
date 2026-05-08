# Topic 2：HTTP、JSON、状态码、接口设计与 AI 产品 API 思维练习

## 1. 本 Topic 学习目标

完成本 Topic 后，你需要掌握：

1. HTTP 的基本含义
2. API 的基本含义
3. GET / POST 的区别
4. JSON 的基本结构
5. 常见 HTTP 状态码
6. FastAPI 接口的基本写法
7. API 请求字段和返回字段的设计
8. 金融 AI Demo 的接口清单
9. 薄 API / 厚业务的分工
10. API 在 AI 产品中的角色
11. 如何从产品需求拆解出接口设计
12. 如何用面试语言解释 API 对 AI 产品落地的作用

---

# Part 1：HTTP 基础理解

## 练习 1：HTTP 是什么？

### 题目

用你自己的话解释：HTTP 是什么？它在一个 AI 产品中起什么作用？

### 参考答案

HTTP 可以理解为前端页面、浏览器、App 和后端服务器之间通信的规则。

在 AI 产品中，用户在页面输入问题后，前端会通过 HTTP 把用户输入发送给后端。后端再调用数据库、大模型、RAG 系统或其他服务，最后把结果通过 HTTP 返回给前端。

例如：

```text
用户输入问题
↓
前端通过 HTTP 发送请求
↓
后端接收请求
↓
调用 AI 模型或数据库
↓
后端通过 HTTP 返回结果
↓
前端展示给用户
```

### 解析

HTTP 本身不是 AI，也不是模型，而是系统之间“传话”的通道。

AI 产品不是只有模型，还需要前端、后端、数据库、模型服务之间互相通信。HTTP 就是其中最常见的通信方式。

---

## 练习 2：判断下面哪些场景需要 HTTP？

### 题目

判断以下场景是否涉及 HTTP 请求：

1. 用户打开一个网页
2. 用户点击“AI 分析股票”按钮
3. 用户在 Python 里写一个普通的 `for` 循环
4. 前端向后端提交用户问题
5. 后端返回 AI 生成的回答

### 参考答案

| 场景 | 是否涉及 HTTP | 原因 |
|---|---|---|
| 用户打开一个网页 | 是 | 浏览器向服务器请求网页内容 |
| 用户点击“AI 分析股票”按钮 | 是 | 前端通常会向后端发送请求 |
| 用户在 Python 里写普通 `for` 循环 | 否 | 这是本地代码逻辑，不一定涉及网络请求 |
| 前端向后端提交用户问题 | 是 | 这是典型 HTTP 请求 |
| 后端返回 AI 生成的回答 | 是 | 后端通过 HTTP 响应返回结果 |

### 解析

只要是浏览器、前端、App 和服务器之间交换数据，大多数情况下都会涉及 HTTP。

但普通本地代码逻辑，例如变量、循环、函数，不一定涉及 HTTP。

---

# Part 2：API 基础理解

## 练习 3：API 是什么？

### 题目

用通俗的话解释：API 是什么？

### 参考答案

API 可以理解为后端开放给前端或其他系统使用的“功能入口”。

比如一个金融 AI Demo 里可能有这些 API：

```text
GET  /health
POST /chat
GET  /stock/{symbol}
POST /stock/analyze
```

你可以把 API 想象成餐厅菜单。

菜单上写着：

```text
1. 查询股票信息
2. 分析财报
3. 和 AI 对话
4. 检查系统是否正常
```

用户或前端不能直接进入后端内部操作数据库或模型，只能通过 API 调用对应功能。

### 解析

API 是产品功能和技术实现之间的桥梁。

产品上看是一个按钮，例如：

```text
AI 分析股票
```

技术上可能对应一个接口：

```text
POST /stock/analyze
```

所以 API 可以把一个抽象产品功能变成一个可以被系统调用的功能入口。

---

## 练习 4：API 在 AI 产品中连接了什么？

### 题目

下面哪些内容通常需要通过 API 连接？

1. 前端页面
2. 后端业务逻辑
3. 数据库
4. 大模型服务
5. 用户输入
6. 分析结果展示

### 参考答案

全部都可能需要通过 API 或后端服务链路连接。

典型 AI 产品链路是：

```text
用户输入
↓
前端页面
↓
API 接口
↓
后端业务逻辑
↓
数据库 / 外部数据 / RAG / 大模型
↓
API 返回结果
↓
前端展示
```

### 解析

AI 产品不是用户直接调用模型，而是通过一整套产品系统完成：

```text
用户需求 → 前端交互 → 后端 API → 数据与模型 → 结果展示
```

API 是这个系统里的关键连接点。

---

# Part 3：GET 和 POST

## 练习 5：区分 GET 和 POST

### 题目

判断下面这些功能更适合用 GET 还是 POST：

1. 查询某只股票的基本信息
2. 用户提交一段问题，让 AI 生成分析
3. 查看系统是否正常运行
4. 创建一条用户分析记录
5. 查询历史聊天记录
6. 上传一段长文本让 AI 总结

### 参考答案

| 功能 | 推荐方法 | 原因 |
|---|---|---|
| 查询某只股票的基本信息 | GET | 只是读取数据 |
| 用户提交问题让 AI 分析 | POST | 需要提交用户输入并触发处理 |
| 查看系统是否正常运行 | GET | 只是查询系统状态 |
| 创建一条用户分析记录 | POST | 创建新数据 |
| 查询历史聊天记录 | GET | 读取已有数据 |
| 上传长文本让 AI 总结 | POST | 提交内容给后端处理 |

### 解析

GET 主要用于“拿数据”。

POST 主要用于“提交数据”或“触发处理”。

简单记忆：

```text
GET = 我要看
POST = 我要交给你处理
```

---

## 练习 6：为功能选择 HTTP 方法

### 题目

你要做一个金融 AI Demo，请为下面的功能选择合适的 HTTP 方法和路径。

1. 检查后端服务是否在线
2. 查询股票代码为 AAPL 的股票信息
3. 用户提交问题，让 AI 回答
4. 用户提交股票代码和问题，让 AI 做分析

### 参考答案

```text
GET  /health
GET  /stock/AAPL
POST /chat
POST /stock/analyze
```

### 解析

`/health` 是健康检查，只需要查询状态，所以用 GET。

`/stock/AAPL` 是查询股票信息，也用 GET。

`/chat` 需要提交用户输入，所以用 POST。

`/stock/analyze` 需要提交股票代码、问题、风险偏好等信息，并触发 AI 分析，所以用 POST。

---

# Part 4：JSON 基础

## 练习 7：识别 JSON 字段

### 题目

阅读下面 JSON，并说明每个字段的含义。

```json
{
  "symbol": "AAPL",
  "question": "这只股票适合长期持有吗？",
  "risk_level": "medium"
}
```

### 参考答案

| 字段 | 含义 |
|---|---|
| symbol | 股票代码，例如 AAPL 表示 Apple |
| question | 用户提出的问题 |
| risk_level | 用户风险偏好，这里是中等风险 |

### 解析

JSON 是前后端传递数据的常见格式。

字段名相当于“信息标签”，字段值相当于“具体内容”。

---

## 练习 8：判断 JSON 是否正确

### 题目

下面哪些是合法 JSON？

### A

```json
{
  "message": "Hello"
}
```

### B

```json
{
  message: "Hello"
}
```

### C

```json
{
  "message": "Hello",
  "language": "zh"
}
```

### D

```json
{
  "message": "Hello",
}
```

### 参考答案

合法 JSON：

```text
A、C
```

不合法 JSON：

```text
B、D
```

### 解析

JSON 的基本规则：

1. 字段名必须用双引号
2. 字符串必须用双引号
3. 最后一个字段后面不能有多余逗号

所以：

```json
{
  message: "Hello"
}
```

不合法，因为 `message` 没有双引号。

```json
{
  "message": "Hello",
}
```

不合法，因为最后多了一个逗号。

---

## 练习 9：设计一个请求 JSON

### 题目

为“AI 股票分析”功能设计一个请求 JSON。

要求包含：

1. 股票代码
2. 用户问题
3. 用户风险偏好
4. 用户希望使用的语言

### 参考答案

```json
{
  "symbol": "TSLA",
  "question": "这只股票未来三个月风险大吗？",
  "risk_level": "high",
  "language": "zh"
}
```

### 解析

这个 JSON 表示用户希望 AI 用中文分析 TSLA，并且用户风险偏好较高。

从产品角度看，这些字段可以帮助 AI 生成更贴近用户需求的回答。

---

## 练习 10：设计一个返回 JSON

### 题目

为“AI 股票分析”功能设计一个返回 JSON。

要求包含：

1. 股票代码
2. AI 分析结果
3. 风险提示
4. 数据来源
5. 是否成功

### 参考答案

```json
{
  "success": true,
  "symbol": "TSLA",
  "analysis": "TSLA 具有较高成长性，但波动也较大，需要关注市场情绪、交付数据和估值水平。",
  "risk_warning": "本分析仅用于学习和信息参考，不构成投资建议。",
  "sources": ["stock_price", "company_profile", "news"]
}
```

### 解析

返回 JSON 不只是给用户看的文字，也要方便前端展示。

例如：

| 字段 | 前端用途 |
|---|---|
| success | 判断请求是否成功 |
| symbol | 展示股票代码 |
| analysis | 展示 AI 分析 |
| risk_warning | 展示风险提示 |
| sources | 展示分析依据 |

---

# Part 5：HTTP 状态码

## 练习 11：匹配状态码含义

### 题目

将状态码和含义匹配起来。

| 状态码 | 含义 |
|---|---|
| 200 | ? |
| 400 | ? |
| 401 | ? |
| 403 | ? |
| 404 | ? |
| 500 | ? |

### 参考答案

| 状态码 | 含义 |
|---|---|
| 200 | 请求成功 |
| 400 | 用户请求有问题，例如字段缺失或格式错误 |
| 401 | 未登录或身份认证失败 |
| 403 | 已登录但没有权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 解析

状态码是后端告诉前端“这次请求发生了什么”的方式。

你可以这样记：

```text
2xx = 成功
4xx = 用户侧请求问题
5xx = 服务端问题
```

---

## 练习 12：为错误场景选择状态码

### 题目

给下面场景选择合适的状态码：

1. 用户成功获取 AI 分析结果
2. 用户没有输入股票代码
3. 用户没有登录，却访问个人分析记录
4. 用户访问一个不存在的股票代码
5. 后端调用大模型失败
6. 普通用户访问管理员后台

### 参考答案

| 场景 | 状态码 |
|---|---|
| 成功获取 AI 分析结果 | 200 |
| 没有输入股票代码 | 400 |
| 没有登录却访问个人记录 | 401 |
| 股票代码不存在 | 404 |
| 后端调用大模型失败 | 500 |
| 普通用户访问管理员后台 | 403 |

### 解析

区分 401 和 403 很重要：

```text
401 = 你是谁？请先登录
403 = 我知道你是谁，但你没有权限
```

区分 400 和 500 也很重要：

```text
400 = 用户传错了
500 = 服务端自己出错了
```

---

## 练习 13：设计用户提示文案

### 题目

为下面状态码设计适合用户看到的提示文案。

1. 400
2. 401
3. 403
4. 404
5. 500

### 参考答案

| 状态码 | 用户提示 |
|---|---|
| 400 | 请检查输入内容是否完整 |
| 401 | 请先登录后再使用该功能 |
| 403 | 你暂无权限访问该功能 |
| 404 | 未找到相关内容，请检查输入 |
| 500 | 系统暂时繁忙，请稍后再试 |

### 解析

产品经理不能只知道技术错误，还要知道如何把错误转化为用户能理解的提示。

例如不要直接给普通用户展示：

```text
Internal Server Error
```

而应该展示：

```text
系统暂时繁忙，请稍后再试
```

---

# Part 6：FastAPI 基础接口练习

## 练习 14：理解 FastAPI 启动命令

### 题目

解释下面命令的含义：

```bash
uvicorn app.main:app --reload
```

### 参考答案

这个命令的意思是：启动 FastAPI 服务。

其中：

| 部分 | 含义 |
|---|---|
| uvicorn | 用来运行 FastAPI 的服务器 |
| app.main | 表示 `app/main.py` 文件 |
| app.main:app | 表示 `main.py` 里面名为 `app` 的 FastAPI 对象 |
| --reload | 代码修改后自动重启服务，适合开发阶段使用 |

### 解析

`uvicorn app.main:app --reload` 可以拆成：

```text
运行 app 文件夹下 main.py 文件里的 app 对象
```

如果终端显示：

```text
Application startup complete.
```

说明服务已经启动成功。

---

## 练习 15：编写 health 接口

### 题目

写一个 FastAPI 接口：

路径：

```text
GET /health
```

返回：

```json
{
  "status": "ok",
  "message": "Financial AI API is running"
}
```

### 参考答案

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Financial AI API is running"
    }
```

### 解析

这个接口的作用是检查服务是否正常运行。

在 AI 产品中，`/health` 常用于：

1. 检查后端是否启动成功
2. 检查服务是否在线
3. 方便部署后做健康检查

---

## 练习 16：编写 GET 股票查询接口

### 题目

写一个 FastAPI 接口：

路径：

```text
GET /stock/{symbol}
```

当用户访问：

```text
/stock/AAPL
```

返回：

```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "price": 192.5,
  "currency": "USD"
}
```

### 参考答案

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    return {
        "symbol": symbol.upper(),
        "company_name": "Apple Inc.",
        "price": 192.5,
        "currency": "USD"
    }
```

### 解析

`{symbol}` 是路径参数。

例如：

```text
/stock/AAPL
```

这里的 `AAPL` 会被传给函数里的 `symbol`。

```python
def get_stock(symbol: str):
```

表示 `symbol` 是一个字符串类型参数。

---

## 练习 17：编写 POST chat 接口

### 题目

写一个接口：

路径：

```text
POST /chat
```

请求 JSON：

```json
{
  "message": "市盈率是什么意思？",
  "language": "zh"
}
```

返回 JSON：

```json
{
  "answer": "市盈率可以理解为投资者愿意为公司每赚 1 元支付多少价格。",
  "type": "financial_education"
}
```

### 参考答案

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    language: str = "zh"

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "answer": "市盈率可以理解为投资者愿意为公司每赚 1 元支付多少价格。",
        "type": "financial_education"
    }
```

### 解析

`BaseModel` 用来定义请求体的字段结构。

```python
class ChatRequest(BaseModel):
    message: str
    language: str = "zh"
```

表示请求 JSON 里应该包含：

```json
{
  "message": "...",
  "language": "zh"
}
```

其中 `language` 默认是 `"zh"`。

---

## 练习 18：理解请求体模型

### 题目

阅读下面代码，说明 `StockAnalyzeRequest` 的作用。

```python
class StockAnalyzeRequest(BaseModel):
    symbol: str
    question: str
    risk_level: str = "medium"
```

### 参考答案

`StockAnalyzeRequest` 定义了股票分析接口需要接收的请求字段。

它要求用户传入：

| 字段 | 类型 | 是否必填 | 含义 |
|---|---|---|---|
| symbol | str | 是 | 股票代码 |
| question | str | 是 | 用户问题 |
| risk_level | str | 否 | 风险偏好，默认是 medium |

### 解析

请求体模型相当于 API 的“入参说明书”。

它告诉后端：

```text
这个接口需要哪些字段？
字段是什么类型？
哪些字段有默认值？
```

也告诉前端和产品经理：

```text
用户需要输入哪些信息？
哪些信息可以不填？
```

---

# Part 7：接口清单设计练习

## 练习 19：设计金融 AI Demo 的接口清单

### 题目

为一个基础版金融 AI Demo 设计接口清单。

要求包含：

1. 健康检查
2. AI 聊天
3. 股票信息查询
4. 股票 AI 分析
5. 查询历史分析记录

### 参考答案

| 功能 | 方法 | 路径 | 说明 |
|---|---|---|---|
| 健康检查 | GET | `/health` | 检查后端服务是否运行 |
| AI 聊天 | POST | `/chat` | 用户向 AI 提问 |
| 股票信息查询 | GET | `/stock/{symbol}` | 查询某只股票基础信息 |
| 股票 AI 分析 | POST | `/stock/analyze` | 对股票进行 AI 分析 |
| 历史分析记录 | GET | `/history` | 查询用户过去的分析记录 |

### 解析

接口清单相当于产品功能和技术实现之间的桥梁。

产品需求是：

```text
用户可以用 AI 分析股票
```

接口设计要进一步拆成：

```text
用户如何提交问题？
后端如何获取股票信息？
AI 分析结果如何返回？
历史记录如何查询？
```

---

## 练习 20：补全接口字段

### 题目

为 `POST /stock/analyze` 设计请求字段和返回字段。

### 参考答案

#### 请求字段

| 字段 | 类型 | 是否必填 | 含义 |
|---|---|---|---|
| symbol | string | 是 | 股票代码 |
| question | string | 是 | 用户问题 |
| risk_level | string | 否 | 风险偏好，可选 low / medium / high |
| language | string | 否 | 返回语言，默认 zh |

#### 返回字段

| 字段 | 类型 | 含义 |
|---|---|---|
| success | boolean | 请求是否成功 |
| symbol | string | 股票代码 |
| analysis | string | AI 分析结果 |
| risk_warning | string | 风险提示 |
| sources | list | 使用的数据来源 |
| created_at | string | 分析生成时间 |

#### 示例请求

```json
{
  "symbol": "AAPL",
  "question": "这只股票适合长期持有吗？",
  "risk_level": "medium",
  "language": "zh"
}
```

#### 示例返回

```json
{
  "success": true,
  "symbol": "AAPL",
  "analysis": "Apple 具有较强的品牌、生态和现金流优势，但也需要关注估值水平和市场竞争。",
  "risk_warning": "本分析仅用于学习和信息参考，不构成投资建议。",
  "sources": ["company_profile", "stock_price", "news"],
  "created_at": "2026-05-03T10:30:00"
}
```

### 解析

字段设计要考虑三件事：

1. 用户输入是否足够支持 AI 分析
2. 后端是否能根据字段执行逻辑
3. 前端是否能根据返回字段展示结果

---

## 练习 21：判断字段是否合理

### 题目

下面是一个股票分析接口的请求 JSON：

```json
{
  "name": "Apple",
  "text": "分析一下",
  "level": "1"
}
```

请指出它的问题，并改成更合理的设计。

### 参考答案

问题：

1. `name` 不够清楚，最好使用 `symbol`
2. `text` 不够清楚，最好使用 `question`
3. `level` 不够清楚，最好使用 `risk_level`
4. `"1"` 不如 `"low" / "medium" / "high"` 直观
5. 缺少语言字段 `language`

改进后：

```json
{
  "symbol": "AAPL",
  "question": "请分析一下这只股票是否适合长期持有",
  "risk_level": "medium",
  "language": "zh"
}
```

### 解析

好的字段名应该具备：

```text
清晰
稳定
容易理解
方便前后端沟通
```

不好的字段名会导致前端、后端、产品、测试人员理解不一致。

---

# Part 8：薄 API / 厚业务

## 练习 22：解释薄 API / 厚业务

### 题目

用通俗语言解释什么是“薄 API / 厚业务”。

### 参考答案

薄 API 的意思是：接口层不要写太复杂，只负责接收请求、检查参数、调用业务逻辑、返回结果。

厚业务的意思是：复杂逻辑应该放在 service 层，例如获取数据、调用大模型、处理结果、生成风险提示、保存历史记录等。

可以这样理解：

```text
API 层 = 前台接待员
Service 层 = 后厨 / 专业分析团队
```

前台负责接单，后厨负责真正做菜。

### 解析

如果所有逻辑都写在 API 函数里，代码会越来越乱，后期难维护。

把复杂逻辑放到 service 层，可以让系统更清晰、更容易测试和扩展。

---

## 练习 23：判断哪些逻辑应该放在哪里

### 题目

判断下面逻辑应该放在 API 层还是 Service 层。

1. 接收用户请求
2. 调用大模型
3. 检查股票代码是否为空
4. 获取股票价格数据
5. 返回 JSON 响应
6. 拼接 Prompt
7. 生成风险提示
8. 保存分析记录

### 参考答案

| 逻辑 | 推荐位置 |
|---|---|
| 接收用户请求 | API 层 |
| 调用大模型 | Service 层 |
| 检查股票代码是否为空 | API 层或 Pydantic 校验 |
| 获取股票价格数据 | Service 层 |
| 返回 JSON 响应 | API 层 |
| 拼接 Prompt | Service 层 |
| 生成风险提示 | Service 层 |
| 保存分析记录 | Service 层 |

### 解析

API 层负责“对外沟通”。

Service 层负责“真正干活”。

一个清晰的结构应该是：

```text
用户请求
↓
API 层
↓
Service 层
↓
模型 / 数据库 / 外部 API
↓
Service 层整理结果
↓
API 层返回结果
```

---

## 练习 24：重构厚 API

### 题目

下面代码的问题是什么？应该如何改？

```python
@app.post("/stock/analyze")
def analyze_stock(request: StockAnalyzeRequest):
    symbol = request.symbol.upper()

    stock_price = 192.5

    prompt = f"请分析 {symbol}，用户问题是：{request.question}"

    ai_result = "这是一段 AI 分析结果"

    risk_warning = "本分析仅供学习参考，不构成投资建议。"

    return {
        "symbol": symbol,
        "analysis": ai_result,
        "risk_warning": risk_warning
    }
```

### 参考答案

问题：

这个 API 函数里写了太多业务逻辑，包括：

1. 处理股票代码
2. 获取股票价格
3. 拼接 Prompt
4. 调用或模拟 AI 分析
5. 生成风险提示

更好的方式是把这些逻辑放到 service 层。

改进示例：

```python
@app.post("/stock/analyze")
def analyze_stock(request: StockAnalyzeRequest):
    result = stock_service.analyze_stock(request)
    return result
```

Service 层：

```python
class StockService:
    def analyze_stock(self, request: StockAnalyzeRequest):
        symbol = request.symbol.upper()

        stock_price = 192.5

        prompt = f"请分析 {symbol}，用户问题是：{request.question}"

        ai_result = "这是一段 AI 分析结果"

        risk_warning = "本分析仅供学习参考，不构成投资建议。"

        return {
            "symbol": symbol,
            "analysis": ai_result,
            "risk_warning": risk_warning
        }

stock_service = StockService()
```

### 解析

原来的代码不是不能运行，而是不利于长期维护。

当项目变大后，API 函数会越来越长，最后很难修改、测试和复用。

薄 API / 厚业务的核心思想是：

```text
接口层保持简单
复杂逻辑集中管理
```

---

# Part 9：AI 产品中的 API 角色

## 练习 25：从用户需求拆接口

### 题目

用户需求：

```text
我希望用户输入一只股票代码，AI 可以分析这只股票的优势、风险和长期投资价值。
```

请拆解成接口设计。

### 参考答案

接口：

```text
POST /stock/analyze
```

请求字段：

| 字段 | 类型 | 是否必填 | 含义 |
|---|---|---|---|
| symbol | string | 是 | 股票代码 |
| question | string | 否 | 用户具体问题 |
| risk_level | string | 否 | 用户风险偏好 |
| language | string | 否 | 返回语言 |

返回字段：

| 字段 | 类型 | 含义 |
|---|---|---|
| symbol | string | 股票代码 |
| strengths | list | 股票或公司的优势 |
| risks | list | 风险点 |
| long_term_view | string | 长期投资观点 |
| risk_warning | string | 风险提示 |

示例返回：

```json
{
  "symbol": "AAPL",
  "strengths": ["品牌影响力强", "生态系统成熟", "现金流稳定"],
  "risks": ["估值偏高", "市场竞争加剧", "硬件增长放缓"],
  "long_term_view": "长期来看，公司基本面较强，但需要结合买入价格和个人风险偏好判断。",
  "risk_warning": "本分析仅用于学习和信息参考，不构成投资建议。"
}
```

### 解析

产品经理要做的不是只写一句“做股票分析功能”，而是要把功能拆成工程师可以实现的接口。

---

## 练习 26：分析 AI 产品链路

### 题目

用户在前端输入：

```text
帮我分析一下英伟达是否适合长期持有
```

请写出从用户输入到 AI 返回结果的完整系统链路。

### 参考答案

```text
1. 用户在前端输入问题
2. 前端把问题、股票代码、风险偏好等信息整理成 JSON
3. 前端通过 HTTP 请求发送给后端
4. 后端 API 层接收请求
5. API 层调用 Service 层
6. Service 层检查参数
7. Service 层获取股票数据、公司信息或相关新闻
8. Service 层构造 Prompt
9. Service 层调用大模型
10. 大模型返回分析结果
11. Service 层补充风险提示并整理结构
12. API 层返回 JSON
13. 前端展示 AI 分析结果
```

### 解析

AI 产品的本质不是“用户直接和模型说话”，而是：

```text
用户需求
↓
产品功能
↓
接口设计
↓
业务逻辑
↓
数据
↓
模型
↓
结果展示
```

API 是这个链路中的关键连接点。

---

## 练习 27：识别 AI 产品中的 API 价值

### 题目

为什么一个 AI 产品不能只有大模型，还需要 API？

### 参考答案

因为大模型只是能力的一部分。

一个完整 AI 产品还需要：

1. 接收用户输入
2. 判断用户身份
3. 获取业务数据
4. 调用大模型
5. 保存历史记录
6. 返回结构化结果
7. 处理错误情况
8. 支持前端展示

API 的作用是把这些能力连接起来。

### 解析

大模型像“大脑”，API 像“神经系统”。

没有 API，前端、数据库、模型服务和用户界面就无法形成一个可用产品。

---

# Part 10：综合实战练习

## 练习 28：设计一个完整的金融 AI Demo API 文档

### 题目

请为你的金融 AI Demo 写一份简化版 API 文档，至少包含三个接口：

1. `GET /health`
2. `POST /chat`
3. `POST /stock/analyze`

每个接口需要写：

1. 功能说明
2. 请求方式
3. 请求字段
4. 返回字段
5. 示例请求
6. 示例返回
7. 可能的错误状态码

---

## API 1：GET /health

### 功能说明

检查后端服务是否正常运行。

### 请求方式

```text
GET /health
```

### 请求字段

无。

### 返回字段

| 字段 | 类型 | 含义 |
|---|---|---|
| status | string | 服务状态 |
| message | string | 状态说明 |

### 示例返回

```json
{
  "status": "ok",
  "message": "Financial AI API is running"
}
```

### 可能状态码

| 状态码 | 含义 |
|---|---|
| 200 | 服务正常 |
| 500 | 服务异常 |

---

## API 2：POST /chat

### 功能说明

用户向 AI 提问，系统返回 AI 回答。

### 请求方式

```text
POST /chat
```

### 请求字段

| 字段 | 类型 | 是否必填 | 含义 |
|---|---|---|---|
| message | string | 是 | 用户问题 |
| language | string | 否 | 返回语言，默认 zh |

### 示例请求

```json
{
  "message": "市盈率是什么意思？",
  "language": "zh"
}
```

### 返回字段

| 字段 | 类型 | 含义 |
|---|---|---|
| answer | string | AI 回答 |
| type | string | 回答类型 |
| risk_warning | string | 风险提示 |

### 示例返回

```json
{
  "answer": "市盈率可以理解为投资者愿意为公司每赚 1 元支付多少价格。",
  "type": "financial_education",
  "risk_warning": "本内容仅用于学习参考，不构成投资建议。"
}
```

### 可能状态码

| 状态码 | 含义 |
|---|---|
| 200 | 请求成功 |
| 400 | message 为空 |
| 500 | AI 服务调用失败 |

---

## API 3：POST /stock/analyze

### 功能说明

根据用户输入的股票代码和问题，生成 AI 股票分析。

### 请求方式

```text
POST /stock/analyze
```

### 请求字段

| 字段 | 类型 | 是否必填 | 含义 |
|---|---|---|---|
| symbol | string | 是 | 股票代码 |
| question | string | 是 | 用户问题 |
| risk_level | string | 否 | 风险偏好 |
| language | string | 否 | 返回语言 |

### 示例请求

```json
{
  "symbol": "AAPL",
  "question": "这只股票适合长期持有吗？",
  "risk_level": "medium",
  "language": "zh"
}
```

### 返回字段

| 字段 | 类型 | 含义 |
|---|---|---|
| success | boolean | 请求是否成功 |
| symbol | string | 股票代码 |
| analysis | string | AI 分析 |
| risk_warning | string | 风险提示 |
| sources | list | 数据来源 |

### 示例返回

```json
{
  "success": true,
  "symbol": "AAPL",
  "analysis": "Apple 具有较强的品牌、生态和现金流优势，但需要关注估值水平和市场竞争。",
  "risk_warning": "本分析仅用于学习和信息参考，不构成投资建议。",
  "sources": ["stock_price", "company_profile", "news"]
}
```

### 可能状态码

| 状态码 | 含义 |
|---|---|
| 200 | 分析成功 |
| 400 | 请求字段缺失 |
| 404 | 股票代码不存在 |
| 500 | AI 服务或数据服务异常 |

---

# Part 11：面试表达练习

## 练习 29：用面试语言解释 API 在 AI 产品中的作用

### 题目

请用 1 分钟左右的面试表达回答：

```text
你如何理解 API 在 AI 产品中的作用？
```

### 参考答案

我理解 API 是 AI 产品中连接用户界面、后端业务逻辑、数据源和大模型能力的关键桥梁。

用户在前端输入问题后，前端会通过 API 把结构化请求发送给后端。后端接收到请求后，会根据业务逻辑获取数据、构造 Prompt、调用大模型，并把结果整理成结构化 JSON 返回给前端。

所以 AI 产品并不是简单调用一个大模型，而是要通过 API 把用户输入、业务规则、数据、模型和前端展示串成一个完整的产品闭环。

在设计 API 时，我会重点关注请求字段、返回字段、错误状态码、异常提示和接口职责边界。同时，我也会倾向于保持 API 层简洁，把复杂逻辑放到 service 层，这样系统更容易维护和扩展。

### 解析

这段回答适合 AI 产品经理、AI 应用开发、数据产品相关岗位。

它体现了你理解：

1. AI 产品不是只有模型
2. API 是系统连接层
3. 你知道字段、状态码、业务逻辑分层
4. 你有产品到技术落地的思维

---

## 练习 30：用面试语言解释薄 API / 厚业务

### 题目

请用 1 分钟左右的面试表达回答：

```text
你如何理解薄 API / 厚业务？
```

### 参考答案

我理解薄 API / 厚业务是一种比较清晰的后端设计思路。

薄 API 指的是接口层尽量保持简单，主要负责接收请求、做基础参数校验、调用业务逻辑，并返回结果。厚业务指的是把真正复杂的逻辑放到 service 层，例如数据获取、规则判断、Prompt 构造、大模型调用、结果解析、风险提示和历史记录保存。

这样做的好处是代码结构更清晰，也更容易维护和扩展。比如在金融 AI 分析场景中，`POST /stock/analyze` 这个接口本身不应该写太多复杂逻辑，而应该调用 `stock_service.analyze()`，让 service 层负责完成股票数据获取、AI 分析和风险提示生成。

这种分层方式也方便产品和工程团队沟通，因为每一层的职责都更明确。

### 解析

这段回答可以展示你不仅懂一点代码，还理解工程结构和产品落地。

---

# Part 12：自测题

## 自测 1：基础概念

### 题目

请回答：

1. HTTP 是什么？
2. API 是什么？
3. JSON 是什么？
4. GET 和 POST 的区别是什么？
5. 200、400、401、403、404、500 分别是什么意思？

### 参考答案

1. HTTP 是前端和后端之间通信的规则。
2. API 是后端开放给前端或其他系统调用的功能入口。
3. JSON 是一种结构化数据格式，常用于前后端传递数据。
4. GET 用于查询数据，POST 用于提交数据或触发处理。
5. 状态码含义：
   - 200：成功
   - 400：请求错误
   - 401：未登录或认证失败
   - 403：没有权限
   - 404：资源不存在
   - 500：服务器内部错误

---

## 自测 2：接口设计

### 题目

设计一个 `POST /news/summarize` 接口，用于让 AI 总结金融新闻。

要求写出：

1. 请求字段
2. 返回字段
3. 示例请求
4. 示例返回
5. 可能状态码

### 参考答案

接口：

```text
POST /news/summarize
```

请求字段：

| 字段 | 类型 | 是否必填 | 含义 |
|---|---|---|---|
| title | string | 是 | 新闻标题 |
| content | string | 是 | 新闻正文 |
| language | string | 否 | 返回语言 |
| summary_length | string | 否 | 摘要长度，可选 short / medium / long |

示例请求：

```json
{
  "title": "Apple reports quarterly earnings",
  "content": "Apple reported its quarterly earnings with strong services revenue...",
  "language": "zh",
  "summary_length": "short"
}
```

返回字段：

| 字段 | 类型 | 含义 |
|---|---|---|
| summary | string | AI 生成的摘要 |
| key_points | list | 新闻要点 |
| sentiment | string | 情绪判断 |
| risk_warning | string | 风险提示 |

示例返回：

```json
{
  "summary": "苹果本季度服务收入表现强劲，但硬件增长仍面临压力。",
  "key_points": ["服务收入增长", "硬件业务承压", "市场关注未来指引"],
  "sentiment": "neutral",
  "risk_warning": "本内容仅用于信息参考，不构成投资建议。"
}
```

可能状态码：

| 状态码 | 含义 |
|---|---|
| 200 | 总结成功 |
| 400 | 标题或正文为空 |
| 500 | AI 总结服务失败 |

---

## 自测 3：产品分析

### 题目

为什么“字段设计”对 AI 产品很重要？

### 参考答案

字段设计决定了前端、后端和 AI 模型之间如何传递信息。

如果字段设计不清楚，前端不知道该传什么，后端不知道该处理什么，AI 也可能缺少必要上下文。

例如股票分析功能中，如果只传：

```json
{
  "text": "分析一下"
}
```

后端无法知道用户要分析哪只股票，也不知道用户的风险偏好和语言需求。

更合理的设计是：

```json
{
  "symbol": "AAPL",
  "question": "这只股票适合长期持有吗？",
  "risk_level": "medium",
  "language": "zh"
}
```

这样系统才能生成更准确、更可控、更符合用户需求的回答。

---

# Part 13：本 Topic 最终掌握清单

学完这一节后，你应该能完成下面这些任务：

- [ ] 能解释 HTTP 是什么
- [ ] 能解释 API 是什么
- [ ] 能区分 GET 和 POST
- [ ] 能读懂基础 JSON
- [ ] 能自己设计简单 JSON 请求体
- [ ] 能解释 200、400、401、403、404、500
- [ ] 能写一个 `GET /health` 接口
- [ ] 能写一个 `POST /chat` 接口
- [ ] 能写一个 `POST /stock/analyze` 接口
- [ ] 能设计接口请求字段和返回字段
- [ ] 能写简单 API 文档
- [ ] 能解释薄 API / 厚业务
- [ ] 能说明 API 在 AI 产品中的作用
- [ ] 能从一个模糊产品需求拆成接口设计
- [ ] 能用面试语言讲清楚 API 如何支撑 AI 产品落地

---

# Part 14：建议你提交到 GitHub 的学习成果

建议你在本 Topic 最后形成以下文件：

```text
topics/topic2/fastapi_basics/
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── services.py
├── README.md
└── api_design_notes.md
```

其中：

## main.py

放 API 路由，例如：

```python
@app.get("/health")
@app.post("/chat")
@app.post("/stock/analyze")
```

## schemas.py

放请求和返回字段定义，例如：

```python
class ChatRequest(BaseModel):
    message: str
    language: str = "zh"
```

## services.py

放业务逻辑，例如：

```python
def analyze_stock(request):
    ...
```

## README.md

说明项目如何启动。

## api_design_notes.md

记录你对接口设计、字段含义、状态码和薄 API / 厚业务的理解。

---

# Part 15：本 Topic 的一句话总结

HTTP、JSON、状态码和 API 设计，是 AI 产品从“用户想法”走向“可运行系统”的基础语言。

对 AI 产品经理和 AI 应用开发者来说，掌握这部分不是为了炫技，而是为了能真正理解：

```text
用户输入如何进入系统？
AI 如何被调用？
数据如何被传递？
结果如何返回？
错误如何处理？
产品功能如何落地？
```

---

# Part 16：最小可运行 FastAPI 示例

如果你想把本 Topic 的内容落实到代码里，可以先创建如下文件：

```text
topics/topic2/fastapi_basics/app/main.py
```

内容如下：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Financial AI API")


class ChatRequest(BaseModel):
    message: str
    language: str = "zh"


class StockAnalyzeRequest(BaseModel):
    symbol: str
    question: str
    risk_level: str = "medium"
    language: str = "zh"


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Financial AI API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "answer": f"你问的是：{request.message}",
        "type": "financial_education",
        "risk_warning": "本内容仅用于学习参考，不构成投资建议。"
    }


@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    return {
        "symbol": symbol.upper(),
        "company_name": "Demo Company",
        "price": 100.0,
        "currency": "USD"
    }


@app.post("/stock/analyze")
def analyze_stock(request: StockAnalyzeRequest):
    return {
        "success": True,
        "symbol": request.symbol.upper(),
        "analysis": f"这是针对 {request.symbol.upper()} 的示例 AI 分析。用户问题是：{request.question}",
        "risk_level": request.risk_level,
        "risk_warning": "本分析仅用于学习和信息参考，不构成投资建议。",
        "sources": ["demo_stock_price", "demo_company_profile"]
    }
```

启动命令：

```bash
uvicorn app.main:app --reload
```

浏览器打开：

```text
http://127.0.0.1:8000/docs
```

---

# Part 17：本 Topic 推荐学习顺序

建议按下面顺序学习和练习：

```text
1. 先理解 HTTP / API / JSON / 状态码
2. 再打开 FastAPI 的 /docs 页面
3. 先测试 GET /health
4. 再测试 POST /chat
5. 再测试 GET /stock/{symbol}
6. 最后测试 POST /stock/analyze
7. 把每个接口的请求字段、返回字段和状态码写入 api_design_notes.md
8. 用面试语言总结 API 在 AI 产品中的作用
```

完成后，你就可以说：

```text
我已经理解了 AI 应用中最基础的 API 设计方式，能够用 FastAPI 搭建简单接口，并能从产品需求拆解出请求字段、返回字段、错误状态码和后端业务分层。
```