# Topic 7 — 微服务与容器化实战 [可选 / 加分项]

> 范围：本目录是 Topic 7 的实操区。目标是让你的金融 AI Demo「**在我电脑上能跑**」变成「**在任何人电脑上都能跑、在云上也能跑**」。
>
> 这是 Roadmap 里标注为「可选」的主题——但**对求职作品集是非常加分的一条**：能在 README 里贴一行 `docker compose up`，作品集的可信度立刻上一个台阶。
>
> 本文件聚焦两件事：**1) 如何把当前 FastAPI 应用容器化；2) 如何用 GitHub Actions 做最小 CI。** 微服务（多服务拆分）只讲思想不强求落地。

---

## 1. 学完这一节你应具备的能力

- 解释「镜像（image）」「容器（container）」「卷（volume）」「网络（network）」分别是什么。
- 写一份**多阶段构建 + 非 root 用户**的 Dockerfile，把 `api/main.py` 容器化。
- 用 `docker compose` 把 API + 向量库（如 Chroma）/ 前端（Streamlit）拼成一个 stack，一条命令启动。
- 知道**镜像里绝对不能放什么**（`.env`、`.git`、虚拟环境、模型权重、训练数据）。
- 写一份最小 GitHub Actions workflow：lint + 测试 + 镜像构建（不发布）。
- 解释「单体 vs 微服务」在你这个 Demo 体量下的取舍，以及未来真要拆分该按什么边界拆。

---

## 2. 本目录结构

```text
topics/topic7/
├── README.md                       # 本文件，完整教学
├── Dockerfile.example              # 多阶段构建 + 非 root 的范例（带详细注释）
├── docker-compose.example.yml      # API + Streamlit + Chroma 的最小 stack
└── .dockerignore.example           # 推荐忽略清单（带注释）

# 仓库根目录已有
Dockerfile
docker-compose.yml
.github/workflows/basic-check.yml
```

> 仓库根目录已有的 `Dockerfile` / `docker-compose.yml` 是「能跑的最小版」；本目录下的 `*.example` 文件是**带注释、生产更友好的进阶版**，建议读完后逐步替换根目录文件。

---

## 3. 容器化的最小心智模型

```text
你的代码 + 系统依赖 + Python 依赖
            │
            ▼
        Dockerfile  (一份「构建配方」)
            │
        docker build
            ▼
        Image  (只读、可分发的快照)
            │
        docker run
            ▼
        Container  (Image 的一次运行实例，进程级隔离)
```

记住三件事：

1. **Image 是不可变的**——同一个 image 在你电脑、同事电脑、云上跑出来必须一样。
2. **Container 是可丢弃的**——任何状态都不该写进容器内部。要持久化，用 **volume**。
3. **环境变量是配置入口**——`.env` 注入容器，而不是 `COPY .env`。

---

## 4. 第 1 课 — 仓库现有 Dockerfile 在做什么

```dockerfile
# 仓库根目录的 Dockerfile（能跑的最小版本）
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

逐行读一遍：

| 指令 | 作用 | 关键点 |
|---|---|---|
| `FROM python:3.12-slim` | 选基础镜像 | `slim` 比默认小 5–10 倍；生产可以再考虑 `distroless` |
| `WORKDIR /app` | 后续命令的工作目录 | 不要再用 `cd`，会丢失 |
| `COPY requirements.txt .` | **先**复制依赖清单 | 配合下一行做层缓存：requirements 不变就不重装 |
| `RUN pip install --no-cache-dir ...` | 装依赖 | `--no-cache-dir` 让镜像更小 |
| `COPY . .` | 复制全部源码 | **危险**：会顺手把 `.env`、`.venv` 也带进去——必须配 `.dockerignore` |
| `EXPOSE 8000` | 声明端口 | 仅文档作用，真正暴露看 `docker run -p` |
| `CMD [...]` | 默认启动命令 | 用 exec form（数组），不用 shell form（字符串） |

---

## 5. 第 2 课 — 进阶 Dockerfile（多阶段 + 非 root）

详见 `Dockerfile.example`，关键改进：

1. **多阶段构建**：用一个 `builder` 阶段装依赖与编译，最终 image 只复制必要产物 → 镜像更小、攻击面更小。
2. **非 root 用户**：进程不以 `root` 跑，避免容器逃逸时直接拿到 root。
3. **`.dockerignore`**：在 build 阶段就拒绝把 `.env` / `.venv` / `.git` 复制进去。
4. **健康检查**：`HEALTHCHECK` 让编排平台知道容器是否真的健康。

最关键的几条：

```dockerfile
# 第一阶段：装依赖
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 第二阶段：运行镜像
FROM python:3.12-slim
RUN useradd -m -u 1000 appuser
USER appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH
COPY --chown=appuser:appuser . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 6. 第 3 课 — `.dockerignore`（最容易被忽略的安全点）

类比 `.gitignore`，但对「构建上下文」生效。**没写就等于把整个仓库塞进镜像**。

`topics/topic7/.dockerignore.example` 推荐内容：

```text
# 密钥与本地配置（绝对不能进镜像）
.env
.env.*
*.pem
*.key

# Python 运行产物
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/

# 虚拟环境（极大且无意义）
.venv/
venv/

# Git 元数据（暴露提交历史）
.git/
.gitignore

# 编辑器 / 系统
.idea/
.vscode/
.DS_Store

# 大文件（除非真的需要）
data/raw/
*.faiss
*.bin
*.pt
chroma/
notebooks/

# 文档（可选；保留 README 即可）
docs/
screenshots/
```

> 验证：把它加好后跑 `docker build` 应该能感觉到**明显变快**（构建上下文体积小很多）。

---

## 7. 第 4 课 — `docker compose` 把多服务串起来

仓库根的 `docker-compose.yml` 是单服务版。Demo 真正的形态通常是 **API + UI + Vector DB**，用 compose 一条命令拉起来。

`docker-compose.example.yml`（详见同目录文件）核心结构：

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      chroma:
        condition: service_healthy

  ui:
    build:
      context: .
      dockerfile: Dockerfile           # 同一个镜像，不同 CMD
    command: ["streamlit", "run", "app/streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
    ports:
      - "8501:8501"
    env_file:
      - .env
    depends_on:
      - api

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma-data:/chroma/.chroma
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  chroma-data:
```

学习要点：

- **`env_file`**：把 `.env` 注入容器环境变量。注意：`.env` 仍然在本地，不进镜像。
- **`volumes`**：让 Chroma 的向量数据**离开容器活着**——容器删了下次还能用。
- **`depends_on` + `healthcheck`**：API 必须等 Chroma 真的健康再启动。
- **同一个镜像跑两种角色**：API 与 UI 共用同一个 `Dockerfile`，只是 `command` 不同——**这是单体应用走向「逻辑分服务」的最低成本方式**。

启动：

```bash
docker compose -f topics/topic7/docker-compose.example.yml up --build
```

---

## 8. 第 5 课 — 单体 vs 微服务：你这个 Demo 选哪个？

| 维度 | 单体（当前 Demo 推荐） | 微服务 |
|---|---|---|
| 部署 | 1 个进程，1 条命令 | N 个服务，需要编排 |
| 调试 | 单进程 stack trace | 跨服务 trace（需要 OpenTelemetry） |
| 复杂度 | ★ | ★★★★ |
| 适合 | **作品集 / MVP / 团队 < 5 人** | 大团队 / 不同语言栈 / 独立伸缩需求 |

> 我的建议：**当前阶段保持单体**，但**逻辑上**按未来拆分思路来组织代码：
>
> ```text
> src/
> ├── llm_client.py          # 未来 → llm-service
> ├── rag_pipeline.py        # 未来 → retrieval-service
> ├── financial_analyzer.py  # 未来 → analyzer-service
> └── ...
> api/
> └── main.py                # 未来 → api-gateway
> ```
>
> 面试时讲：「我现在是单体，但模块边界已按未来微服务拆分思路设计——`llm_client` 可以独立成服务，`rag_pipeline` 可以独立成服务。这是有意识的架构取舍。」**这种回答比硬上微服务漂亮得多。**

如果未来真要拆，按下面的边界拆通常不会错：

```text
[ Streamlit UI ]  ──►  [ API Gateway (FastAPI) ]
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       [ LLM Service ]  [ Retrieval ]   [ Analyzer ]
                              │
                              ▼
                      [ Vector DB (Chroma) ]
```

---

## 9. 第 6 课 — 最小 CI（GitHub Actions）

仓库根已有 `.github/workflows/basic-check.yml`，做的是「装依赖 + 跑 pytest」。Topic 7 阶段建议**再加一步「能不能成功 build 镜像」**：

```yaml
name: ci
on:
  push:
    branches: [main, master]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -q

  docker-build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Build image (no push)
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: financial-ai-demo:ci
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

要点：

- `needs: test` 让构建只在测试通过后跑，节省 CI 配额。
- `push: false`：CI 阶段**只验证能不能构建**，不发布镜像（发布到 registry 是后续课题）。
- `cache-from/cache-to: type=gha`：用 GitHub Actions cache 复用层，第二次跑会快很多。

> 进阶（不强制）：再加一步用 `aquasecurity/trivy-action` 扫镜像漏洞，写在简历上是「我懂 supply-chain security」。

---

## 10. 注意事项 / 常见坑

### 10.1 镜像与构建
- `COPY .` 没配 `.dockerignore` = 几乎肯定会泄漏 `.env`、`.venv`、`.git`。
- 把 `.env` 写进 Dockerfile 的 `ENV` = 等同于公开密钥（任何人 `docker history` 都看得见）。
- 大文件（模型权重、向量索引）放进镜像 → 镜像几个 GB → CI 很慢且每次部署都搬。**用 volume 或对象存储**。
- 不固定基础镜像版本（`FROM python` 而不是 `python:3.12-slim`）= 哪天 CI 突然挂掉很难复现。

### 10.2 运行时
- 容器以 root 跑 = 安全审查必挂。**始终建专用用户**（见 Dockerfile.example）。
- `localhost` 在容器里指容器自己。**容器之间互相调用**走 compose 的服务名（如 `http://chroma:8000`）。
- 容器里 `print` 出来的东西去了哪？ → 默认到 stdout，被 `docker logs` 抓到。**不要写本地文件**，不会跨容器持久化。

### 10.3 LLM / Demo 特有
- 镜像里**不要**预下载模型权重——首次运行从 Hugging Face 拉，配 volume 缓存。
- Streamlit 容器化要加 `--server.address 0.0.0.0`，否则只监听 `127.0.0.1` 容器外访问不到。
- 有状态依赖（向量库）一定要 volume；删容器 = 删数据，会让 Demo 偶发地「重新初始化」。

### 10.4 CI / 部署
- CI 上的 `pytest` **不要**依赖真实 LLM API（费钱、不稳定）。给 `llm_client` 写 mock 或用 `--dry-run`。
- 真要往 registry 推镜像 → 用 `secrets.GHCR_TOKEN`，不要把 token 硬编码到 workflow。
- 部署到 Hugging Face Spaces / Render / Railway 时，**密钥走平台的 secrets 配置**，不要进镜像。

---

## 11. 推荐练习（按顺序做）

1. **加 `.dockerignore`**

   把本目录的 `.dockerignore.example` 复制到仓库根目录改名为 `.dockerignore`，重新 `docker build`，对比构建上下文大小。

2. **替换为多阶段 Dockerfile**

   把根目录 `Dockerfile` 替换为本目录 `Dockerfile.example` 的内容，跑：

   ```bash
   docker build -t financial-ai-demo .
   docker run --rm -p 8000:8000 --env-file .env financial-ai-demo
   curl http://localhost:8000/health
   ```

3. **跑通三服务 compose**

   ```bash
   docker compose -f topics/topic7/docker-compose.example.yml up --build
   ```

   分别访问：
   - API：`http://localhost:8000/health`
   - UI：`http://localhost:8501`
   - Chroma：`http://localhost:8001/api/v1/heartbeat`

4. **给 CI 加一步 docker build**

   把第 9 节的 `docker-build` job 合并到 `.github/workflows/basic-check.yml`，push 到 GitHub 看 Actions 页面。

5. **写一份「单体 → 微服务的迁移路线」**（选做，1 页）

   分析当前 `src/` 模块，列出未来要拆几个服务、每个服务的接口契约（输入/输出 JSON）、共享什么（鉴权 / 日志 / 向量库）。**这是 AI 应用工程师面试里很常见的开放题。**

---

## 12. 升级路线（Topic 7 → Topic 7+）

- 镜像扫描：`trivy` 接入 CI，把 CVE 当 PR check。
- 镜像签名：`cosign`，让用户能验证镜像来自你。
- 部署：从 `docker run` → **Hugging Face Spaces / Render / Fly.io / Railway**（免费层就够 Demo）。
- 编排：从 `docker compose` → **Kubernetes**（先用 minikube 本地玩，再上 EKS/GKE）。
- 可观测性：接入 **OpenTelemetry**，日志 / 指标 / trace 一起做。
- Service Mesh / API Gateway：等真的拆成多服务再考虑。

---

## 13. 自测检查表

- [ ] 我能说出 Image / Container / Volume / Network 各是什么。
- [ ] 我的 Dockerfile 用了多阶段构建并且**不以 root 运行**。
- [ ] 我有 `.dockerignore`，且 `.env`、`.venv`、`.git` 都不会进镜像。
- [ ] 我能用 `docker compose up` 一条命令拉起整个 stack（API + UI + 向量库）。
- [ ] 我的 CI 至少能验证「测试通过」+「镜像能构建」。
- [ ] 我能解释当前为什么用单体，以及未来怎么按服务边界拆。
- [ ] 我的 README 里写明了 `docker compose up` 的运行方式（求职 Demo 的关键）。

---

## 14. 反思模板

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this improves my project:
这如何提升我的项目：

Next improvement:
下一步改进：
```
