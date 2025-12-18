# Ripple Idea

お題を入れると、関連するアイデアが波紋みたいに広がっていくやつ。

```text
       「新規事業」
           │
     ┌─────┼─────┐
     ↓     ↓     ↓
  サブスク  B2B  コミュニティ
     │
     └→ クリックするとさらに広がる
```

## 動かし方

### バックエンド

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # OPENROUTER_API_KEY を設定
uvicorn main:app --reload
```

<http://localhost:8000/docs> で API ドキュメントが見れる。

### フロントエンド

```bash
cd frontend
bun install
bun run dev
```

<http://localhost:5173> で開く。

## 友達と共有

```bash
# Cloudflare Tunnel で一時的に公開 (login不要)
cloudflared tunnel --url http://localhost:5173
# 表示されたURLを共有
```

※ `cloudflared tunnel login` は不要。毎回ランダムURLが発行される。

## API

### POST /api/ideas/generate

```bash
curl -X POST http://localhost:8000/api/ideas/generate \
  -H "Content-Type: application/json" \
  -d '{"parentContent": "プロダクト開発", "count": 3}'
```

```json
{
  "ideas": [
    {"content": "ユーザーインタビュー自動化", "confidence": 0.92},
    {"content": "プロトタイプ共有基盤", "confidence": 0.88}
  ]
}
```

## 構成

- Frontend: React 19 + Vite + D3.js
- Backend: Python + FastAPI + OpenRouter
- Package: Bun (frontend) / pip (backend)

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| OPENROUTER_API_KEY | OpenRouter の API キー | (必須) |
| FRONTEND_URL | CORS 許可するオリジン | `http://localhost:5173` |
| VITE_API_URL | バックエンドURL | `http://localhost:8000` |
