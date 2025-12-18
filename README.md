# Ripple Idea

お題を入れると、関連するアイデアが波紋みたいに広がっていくやつ。

```
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

# venv 作る
python -m venv venv
source venv/bin/activate

# 依存入れる
pip install -r requirements.txt

# 環境変数
cp .env.example .env
# .env を開いて CLAUDE_API_KEY を設定

# 起動
uvicorn main:app --reload
```

http://localhost:8000/docs で API ドキュメントが見れる。

DevContainer 使うなら VS Code で「Reopen in Container」するだけ。

### フロントエンド

まだ。

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
    {"content": "ユーザーインタビュー自動化ツール", "confidence": 0.92},
    {"content": "プロトタイプ共有プラットフォーム", "confidence": 0.88},
    {"content": "開発者向けフィードバック収集", "confidence": 0.85}
  ]
}
```

### GET /health

生きてるか確認用。

## 構成

- バックエンド: Python + FastAPI + Claude API
- フロントエンド: React + Vite + D3.js (予定)
- デプロイ: Railway (API) + Vercel (フロント)

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| CLAUDE_API_KEY | Claude の API キー | (必須) |
| FRONTEND_URL | CORS 許可するオリジン | http://localhost:5173 |
| PORT | サーバーのポート | 8000 |
