# AI Gateway

一個 FastAPI 微服務，為 AI 供應商（Ollama、OpenAI）提供統一的 HTTP API。

## 快速開始

### 本地開發

```powershell
# 安裝依賴
uv sync

# 啟動服務
uv run uvicorn app.main:app --reload
```

### Docker

```powershell
docker-compose up -d
```

## API 端點

### 健康檢查

```http
GET /health
```

### 聊天補全

```http
POST /v1/chat
Content-Type: application/json

{
  "messages": [
    {"role": "system", "content": "你是一個有幫助的助手。"},
    {"role": "user", "content": "你好"}
  ],
  "temperature": 0.2,
  "max_tokens": 256
}
```

### 文字分析

```http
POST /v1/analyze
Content-Type: application/json

{
  "text": "這是一個很棒的產品！",
  "options": {
    "need_summary": true,
    "need_label": true,
    "need_score": true,
    "extra_fields": ["keywords"]
  }
}
```

## 環境變數設定

| 環境變數                   | 預設值                    | 說明                        |
| ------------------------- | ------------------------ | --------------------------- |
| `AI_PROVIDER`             | `ollama`                 | AI 供應商（ollama/openai）    |
| `AI_MODEL`                | `gemma3:1b`              | 模型名稱                     |
| `OLLAMA_BASE_URL`         | `http://localhost:11434` | Ollama API 網址             |
| `REQUEST_TIMEOUT_SECONDS` | `30`                     | HTTP 請求逾時（秒）           |
| `LOG_LEVEL`               | `INFO`                   | 日誌等級                     |
| `SERVICE_VERSION`         | `0.1.0`                  | 服務版本                     |

## 測試

```powershell
uv run pytest tests/ -v
```

## 授權

MIT
