# FastAPI Todo API

一个基于 FastAPI + SQLite 的待办事项 REST API，采用三层架构设计，作为后端分层与工程规范的练手项目。

## 技术栈

- **Python 3.14**
- **FastAPI** —— Web 框架
- **Pydantic** —— 数据校验与序列化
- **SQLite** —— 数据库

## 项目结构

```
.
├── main.py            # 应用装配：创建 app、挂载路由、注册异常处理器
├── api/
│   ├── __init__.py
│   └── todos.py       # 接口层：接收请求、返回响应、决定状态码
├── service.py         # 服务层：业务校验、业务规则
├── repository.py      # 数据层：SQL 语句与数据库连接管理
└── schemas.py         # 数据模型：Pydantic 请求 / 响应模型
```

分层依赖是**单向**的：`api → service → repository → SQLite`，下层不感知上层。
接口层只依赖服务层，因此更换数据库实现时上层无需改动。

各层职责边界：

| 层 | 文件 | 职责 | 不做什么 |
| --- | --- | --- | --- |
| 接口层 | `api/todos.py` | 接请求、调服务、返回响应 | 不写业务规则和 SQL |
| 服务层 | `service.py` | 业务校验、编排数据层调用 | 不 import FastAPI、不写 SQL |
| 数据层 | `repository.py` | SQL、连接管理 | 不做业务判断、不碰 HTTP |

## 快速开始

```bash
# 1. 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 2. 安装依赖
pip install fastapi uvicorn

# 3. 启动服务
uvicorn main:app --reload
```

启动后访问 <http://127.0.0.1:8000/docs> 查看交互式接口文档。

## 接口列表

| 方法 | 路径 | 说明 | 成功 | 失败 |
| --- | --- | --- | --- | --- |
| POST | `/todos` | 新增待办 | 200 | 400 |
| GET | `/todos` | 查询全部待办 | 200 | — |
| GET | `/todos/{todo_id}` | 查询单条待办 | 200 | 404 |
| PUT | `/todos/{todo_id}` | 更新待办 | 200 | 400 / 404 |
| DELETE | `/todos/{todo_id}` | 删除待办 | 200 | 404 |

请求体示例：

```json
{
  "title": "买牛奶",
  "done": false
}
```

## 错误处理

业务异常统一由 FastAPI 的异常处理器转换为 HTTP 状态码：

- `TodoValidationError` → **400**（标题为空，或超过 100 个字符）
- `TodoNotFoundError` → **404**（待办不存在）

数据层用 `False` 表示"未命中"，由服务层翻译成业务异常；真正的故障（如数据库不可用）
则向上抛出异常，最终返回 500 —— 避免把服务器故障误报成"资源不存在"。

## 后续计划


- [ ] 在此基础上开发 RAG 知识库问答项目
