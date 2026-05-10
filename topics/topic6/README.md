# Topic 6 — 隐私与安全实战

> 范围：本目录是 Topic 6 的实操区。目标是把你的金融 AI Demo 从「能跑」升级到「能给别人看」——也就是**面试时不会因为安全问题被一票否决**。
>
> 配套笔记：`docs/security_notes.md`（极简免责声明）。本文件聚焦：**API Key 怎么存、`.env` 怎么用、`.gitignore` 怎么写、最简单的接口鉴权怎么做、金融场景下还要补什么。**

---

## 1. 学完这一节你应具备的能力

- 解释为什么不能把 API Key 写进代码、提交到 GitHub。
- 用 `python-dotenv` + 环境变量的方式安全加载密钥；区分 `.env` 与 `.env.example` 的角色。
- 写出一份覆盖 Python、虚拟环境、IDE、模型缓存、密钥文件的 `.gitignore`。
- 给 FastAPI 加上最小可用的「API Key 鉴权」中间件，理解后续如何升级到 JWT / OAuth2。
- 在金融场景下补齐 4 类必做事项：**免责声明 / 输入校验 / 日志脱敏 / 速率限制（思想）**。
- 万一密钥不小心提交了，知道**「先吊销、再清理」**的正确顺序。

---

## 2. 本目录结构

```text
topics/topic6/
├── README.md             # 本文件，完整教学
├── env_loader_demo.py    # 安全加载 .env 的最小示例（含错误演示）
├── auth_demo.py          # FastAPI + 最简单 API Key 鉴权
└── secret_scan.py        # 扫一扫仓库里有没有疑似 API Key 的字符串

# 配套文件（仓库根目录已有）
.env.example              # 模板：可以提交
.env                      # 真实密钥：永远不提交
.gitignore                # 已忽略 .env
docs/security_notes.md    # 极简免责声明
```

---

## 3. 安全三原则（先记住这张图）

```text
1) Secrets 出仓库  ──►  代码里不写 Key，全部读环境变量
2) 用户输入有边界  ──►  Pydantic / 长度限制 / 白名单
3) 输出可被信任    ──►  免责声明 + 不暴露内部错误堆栈
```

一句话：**不让密钥跑出去，不让用户输入跑进来作恶，不让模型胡说八道当结论。**

---

## 4. 第 1 课 — API Key 与 `.env`：最常见也最致命

### 4.1 为什么不能硬编码

下面这种写法是**面试一票否决级**的反例：

```python
# ❌ 反例：永远不要这么做
client = SomeLLM(api_key="sk-live-abcdef1234567890")
```

风险：

- 一旦推到 GitHub（哪怕是 private 仓库被误改成 public），扫描机器人**几分钟内**就会捡到。
- 多人协作时，Key 跟着代码到处跑，**无法吊销单一来源**。
- 不同环境（dev / staging / prod）需要不同 Key，硬编码意味着每次切环境都要改代码。

### 4.2 正确姿势：环境变量 + `.env`

仓库根目录已经有：

```env
# .env.example  （可以提交）
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

```env
# .env          （绝不提交）
GEMINI_API_KEY=AIza...你的真实 Key
GEMINI_MODEL=gemini-2.5-flash
```

代码里这样读：

```python
import os
from dotenv import load_dotenv

load_dotenv()  # 默认读取当前目录的 .env

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Did you create .env?")
```

### 4.3 `.env` vs `.env.example`

| 文件 | 是否进 Git | 内容 | 作用 |
|---|---|---|---|
| `.env.example` | ✅ 进 Git | **键名 + 占位符**（如 `your_key_here`） | 告诉别人需要哪些环境变量 |
| `.env` | ❌ 不进 Git | 键名 + **真实密钥** | 自己本地跑 |

新人最常犯的错：把 `.env` 提交了，或者把 `.env.example` 写成了真实 Key。

> 实操：跑一下 `topics/topic6/env_loader_demo.py`，先看「不读环境变量」会怎么炸，再看正确加载的样子。

---

## 5. 第 2 课 — `.gitignore` 必须包含什么

仓库当前的 `.gitignore` 已经覆盖核心项，下面是**金融 AI 项目最小推荐版**（含解释）：

```gitignore
# Python 运行产物
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# 虚拟环境
.venv/
venv/

# 测试 / 缓存
.pytest_cache/
.mypy_cache/

# 系统 / 编辑器
.DS_Store
.idea/
.vscode/

# 密钥与本地配置（金融项目重点）
.env
.env.*.local
*.pem
*.key
credentials.json

# 模型 / 向量索引（容易很大且含敏感信息）
*.faiss
*.bin
*.pt
chroma/

# 数据（教学项目常被忽略，但实际上需要看是否含敏感信息）
data/raw/private_*
data/processed/*.parquet
```

> 注意：`.gitignore` 只对**还没被 Git 追踪的文件**生效。如果你已经 `git add` 过 `.env`，再加规则也没用，必须先 `git rm --cached .env`。

---

## 6. 第 3 课 — 万一密钥泄漏了：先吊销，再清理

时间顺序很关键，**绝对不要反过来**：

```text
1. 立刻去服务商控制台「吊销 / Rotate」泄漏的 Key
2. 生成新 Key，更新本地 .env
3. 然后再处理 Git 历史
   - 简单情况：git rm --cached .env && commit && push
   - 严重情况（密钥已在远端历史里）：
       使用 git filter-repo 或 BFG Repo-Cleaner 重写历史
       force-push 后通知所有协作者重新 clone
4. 检查账单与调用日志，确认没有异常用量
```

**重点**：吊销永远是第 1 步。即便你把 Git 历史擦得再干净，扫描机器人可能早就抓到了快照。

---

## 7. 第 4 课 — 给 FastAPI 加最小可用鉴权

学习目标：让 `/analyze-company` 这种接口**不能被随便 curl**。

### 7.1 思路对比

| 方案 | 复杂度 | 适合场景 |
|---|---|---|
| 不加鉴权 | ★ | 完全本地 Demo |
| **静态 API Key（请求头）** | ★★ | **求职 Demo / 内部工具（推荐先做这层）** |
| HTTP Basic | ★★ | 简单内部页面 |
| JWT / OAuth2 | ★★★★ | 真实多用户产品 |
| 第三方 IdP（Auth0 / Cognito） | ★★★ | 不想自己管账号 |

> 当前阶段（Topic 6）：**做到 API Key 那一档就够了**，写在简历里也足够说明「我懂鉴权概念」。Topic 6+ 再升级 JWT。

### 7.2 最小代码（详见 `auth_demo.py`）

核心思路：

1. 把一个独立的「服务端 API Key」存进 `.env`（跟 LLM 的 Key **不要混用**）。
2. 用 FastAPI `Depends` + `Header` 校验请求头里的 `X-API-Key`。
3. 不通过就返回 `401`，**不要**把期望的 Key 放进错误信息里。

```python
import os
from fastapi import FastAPI, Header, HTTPException, Depends
from dotenv import load_dotenv

load_dotenv()
SERVER_API_KEY = os.getenv("SERVER_API_KEY")  # 与 LLM Key 区分

def require_api_key(x_api_key: str = Header(default=None)):
    if not SERVER_API_KEY or x_api_key != SERVER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze-company", dependencies=[Depends(require_api_key)])
def analyze_company(payload: dict):
    return {"company": payload.get("name", "unknown"), "summary": "..."}
```

调用方式：

```bash
# 不带 Key —— 应当 401
curl -X POST http://localhost:8000/analyze-company \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme"}'

# 带 Key —— 200
curl -X POST http://localhost:8000/analyze-company \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVER_API_KEY" \
  -d '{"name":"Acme"}'
```

### 7.3 升级路径（看一下就好，不用现在做）

```text
API Key  ─► JWT (有过期时间 + 用户身份)
         ─► OAuth2 (第三方登录 / 多角色)
         ─► RBAC (谁能调哪个接口)
```

---

## 8. 第 5 课 — 金融场景下还必须做的 4 件事

这是把项目从「**编程练习**」升级到「**金融 AI Demo**」的关键。

### 8.1 免责声明（合规底线）

每一个返回 LLM 结论的接口，**响应体里都应该带**一段免责声明，而不只是 README：

```python
DISCLAIMER = (
    "本回答仅用于学习和研究目的，不构成任何金融投资建议。"
    "信息可能不完整或过时，决策前请咨询持牌专业人士。"
)

return {
    "answer": llm_output,
    "disclaimer": DISCLAIMER,
    "sources": [...],
}
```

### 8.2 输入校验：用 Pydantic，不要用裸 dict

反例：

```python
# ❌ payload: dict 完全无校验，prompt injection 友好
@app.post("/ask")
def ask(payload: dict): ...
```

正例：

```python
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    company_ticker: str = Field(pattern=r"^[A-Z]{1,5}$")

@app.post("/ask")
def ask(req: AskRequest): ...
```

收益：

- 自动拒绝过长 / 格式错误 / 缺字段的请求。
- 缩小**提示词注入（prompt injection）**的攻击面。
- 自动生成 OpenAPI 文档，面试时给人看 Swagger 页面非常加分。

### 8.3 日志脱敏：别把 Key / PII 打到日志里

```python
# ❌ 反例
logger.info(f"Calling LLM with key={api_key} and user={user_email}")

# ✅ 正例
logger.info("Calling LLM", extra={
    "key_id": api_key[:6] + "***",
    "user_id_hash": hash_user(user_email),
})
```

原则：**日志里只放可观察性需要的最少信息**。

### 8.4 速率限制（思想 > 实现）

即使不上生产，也要在 README / 接口注释里写明：

```text
TODO: 接入 rate limiter（每 IP / 每 Key 每分钟 N 次）
原因：防止 LLM API 账单被刷爆 + 防止滥用
```

具体实现可以用 `slowapi`、`fastapi-limiter`，或反向代理（Nginx / Cloudflare）那一层做。**面试时能讲出「为什么需要、放在哪一层」就够了。**

---

## 9. 第 6 课 — 自己扫一遍仓库（防呆检查）

跑下面这条命令做一次「自查」（详细脚本见 `secret_scan.py`）：

```bash
.venv/bin/python topics/topic6/secret_scan.py .
```

它会：

- 扫 `.py` / `.md` / `.yml` / `.json` / `.env*`（默认跳过 `.git/`、`.venv/`、`node_modules/`）。
- 用启发式正则匹配常见 Key 形态：`sk-...`、`AIza...`、`AKIA...`、`ghp_...`、`xox[abp]-...` 等。
- 命中后**只打印行号与片段**，不打印完整 Key。

> 注意：这只是教学级自查，不能替代专业工具（`gitleaks`、`trufflehog`）。但它能在你 push 之前抓到 80% 的低级失误。

---

## 10. 注意事项 / 常见坑

### 10.1 `.env` 相关
- `.env` 已被 `git add` 过：单加 `.gitignore` 不生效，必须 `git rm --cached .env`。
- `.env.example` 写了真实 Key：等同于直接泄漏，立刻吊销。
- 一份 `.env` 里塞了**多个项目**的 Key：泄漏一次=全军覆没，按项目隔离。

### 10.2 鉴权相关
- 静态 API Key 不要写在 URL 里（会进访问日志、Referer），永远走请求头或 body。
- HTTPS 不是可选项；本地开发 OK，**任何对外暴露的 Demo 都必须 HTTPS**。
- 错误信息里**不要**透露「Key 长度对 / 用户存在但密码错」这种细节，统一返回 `401 Unauthorized`。

### 10.3 LLM 特有风险（金融 Demo 很重要）
- **提示词注入**：用户上传文档里可能写「忽略上面所有指令」。最低成本防御 = 在 system prompt 里写死边界 + 限制输出格式。
- **训练数据回流**：用付费 / 商用 API（OpenAI / Gemini）通常默认不会回流，但用 SaaS 平台前请确认条款。
- **PII**：财报 OK，但用户上传的合同 / 客户名单 = PII。Demo 阶段建议**只允许示例数据**。

### 10.4 部署相关（与 Topic 7 衔接）
- 容器里**不要 COPY `.env`**，要在 `docker run -e` 或 `compose.env_file` 注入。
- Docker 镜像里的环境变量，**任何能 `docker inspect` 的人都能看见**——所以生产用 secrets manager（AWS Secrets Manager / Vault）。
- 把 `.env` 写进 `Dockerfile` 用 `ENV` 指令 = 镜像层永远带着这个 Key，**等同于公开**。

---

## 11. 推荐练习（按顺序做）

1. **跑通 env_loader_demo**

   ```bash
   .venv/bin/python topics/topic6/env_loader_demo.py
   ```

   感受「没有 .env 时报错」与「正确加载」两种情况的差别。

2. **给 `/analyze-company` 加 API Key 鉴权**

   - 在 `.env` 里加一行 `SERVER_API_KEY=dev-secret-please-change-me`
   - 把 `auth_demo.py` 的思路搬到 `api/main.py`
   - 用 `curl` 验证带 / 不带 Header 的两种返回。

3. **加金融免责声明到所有返回 LLM 结论的接口**

   每个 LLM 回答都附 `disclaimer` 字段，前端 / Streamlit 上也展示出来。

4. **跑一次 secret_scan**

   ```bash
   .venv/bin/python topics/topic6/secret_scan.py .
   ```

   修复所有命中（如果有）。**注意：不是所有命中都是真泄漏**——示例占位符也会命中，需要人工确认。

5. **写一份 `docs/threat_model.md`**（选做，1 页即可）
   按表格列：威胁 / 影响 / 当前缓解 / 待办。这是非常加分的产出物。

   | 威胁 | 影响 | 当前缓解 | 待办 |
   |---|---|---|---|
   | API Key 泄漏 | 账单被刷 | `.env` + `.gitignore` + secret_scan | 接入 gitleaks pre-commit |
   | 提示词注入 | 模型说错 | system prompt 限制 | 加输出格式校验 |
   | ... | ... | ... | ... |

---

## 12. 升级路线（Topic 6 → Topic 6+）

- 静态 API Key → **JWT**（`python-jose` / `pyjwt`），加过期时间和 user 信息。
- 单租户 → **多租户**：每个用户一份 token，接口里能区分 `current_user`。
- 本地 `.env` → **Secrets Manager**（AWS Secrets Manager / GCP Secret Manager / Vault）。
- 手动扫描 → **`gitleaks` / `trufflehog` pre-commit hook**，提交前自动拦截。
- 加 **`slowapi`** 做接口级速率限制；前面挂 Nginx / Cloudflare 做 IP 级限流。

---

## 13. 自测检查表

- [ ] 我能解释为什么 `.env` 不能进 Git，以及如果不小心提交了应该怎么处理。
- [ ] 我的仓库里**没有任何**真实 API Key（用 `secret_scan.py` 验证过）。
- [ ] 我给 `/analyze-company` 接口加了 API Key 鉴权（或在 README 里说明了为什么暂不加）。
- [ ] 我的 LLM 接口返回里都包含 `disclaimer` 字段。
- [ ] 我能讲出至少 3 个金融 AI 特有的安全 / 合规风险。
- [ ] 我知道下一步要把鉴权升级到 JWT / 把密钥搬到 Secrets Manager。

---

## 14. 反思模板

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my Financial AI Demo:
这对我的金融 AI Demo 的帮助是：

Next improvement:
下一步改进：
```
