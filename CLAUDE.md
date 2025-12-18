<!-- このファイルを編集した後は、必ず `bunx markdownlint-cli CLAUDE.md` し、警告が無い状態にすること -->

# Ripple Idea

お題を入力すると、波紋のようにアイデアが広がるWebアプリ。

```text
     「プロダクト開発」
      ／  │  ｜  ＼
   マーケ 企画 技術 デザイン
      ↓
  クリック → さらに波紋が広がる
```

## 技術スタック

| 層 | 技術 |
|----|------|
| Frontend | React 19 + TypeScript + Vite + D3.js |
| Backend | Python + FastAPI |
| LLM | OpenRouter (Gemini Flash / Claude Haiku) |
| Package | Bun (frontend) / pip (backend) |

## クイックスタート

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # OPENROUTER_API_KEY を設定
uvicorn main:app --reload

# Frontend
cd frontend
bun install
bun run dev
```

## ディレクトリ構造

```text
frontend/
├── src/
│   ├── components/
│   │   ├── RadialTree.tsx      # D3.js ラジアルツリー
│   │   └── ControlPanel.tsx    # 入力フォーム
│   ├── hooks/
│   │   ├── useIdeaTree.ts      # ツリー状態管理
│   │   └── useLocalStorage.ts  # ストレージ
│   ├── types/index.ts
│   ├── utils/api.ts
│   └── App.tsx
└── package.json

backend/
├── main.py              # FastAPI アプリ
├── llm_client.py        # OpenRouter クライアント
├── models.py            # Pydantic モデル
├── requirements.txt
├── .env.example
└── .devcontainer/       # DevContainer 設定
```

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

## データモデル

```typescript
interface Node {
  id: string
  content: string
  parentId: string | null
  depth: number
  children: Node[]
  confidence: number
  createdAt: string
}

interface Session {
  sessionId: string
  rootTopic: string
  rootNode: Node
  timestamp: string
}
```

## 環境変数

### backend/.env

```bash
OPENROUTER_API_KEY=your_key    # 必須
FRONTEND_URL=http://localhost:5173
```

### frontend/.env

```bash
VITE_API_URL=http://localhost:8000
```

## OpenRouter 設定

**推奨モデル**:

| 用途 | モデル | コスト |
|------|--------|--------|
| 開発 | `deepseek/deepseek-r1:free` | 無料 |
| 本番 | `google/gemini-2.0-flash-001` | ~30円/3h |
| 高品質 | `anthropic/claude-haiku-4.5` | ~50円/3h |

**セットアップ**:

1. <https://openrouter.ai> でアカウント作成
2. $10 チャージ → API KEY 取得
3. `backend/.env` に設定

## 共有 (Cloudflare Tunnel)

```bash
# ターミナル1: Frontend
bun run dev

# ターミナル2: Backend
uvicorn main:app --reload

# ターミナル3: Tunnel (共有時のみ)
cloudflared tunnel --url http://localhost:5173
# → 表示されたURLを共有
```

**cloudflared インストール**:

```bash
# macOS
brew install cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64 && sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

## デプロイ (オプション)

ローカル実行推奨。本番デプロイが必要な場合:

| 層 | サービス | 設定 |
|----|----------|------|
| Backend | Railway | `OPENROUTER_API_KEY`, `FRONTEND_URL` |
| Frontend | Vercel | `VITE_API_URL` |

## 開発ガイドライン

- D3.js のラジアルツリーは軽量に (100ノード以下推奨)
- localStorage に JSON.stringify で保存
- API失敗時は再試行 UI を表示
- CORS: `FRONTEND_URL` 環境変数で制御

## トラブルシューティング

| 問題 | 対応 |
|------|------|
| API エラー | `echo $OPENROUTER_API_KEY` で確認、クレジット残高チェック |
| CORS エラー | `FRONTEND_URL` が正しいか確認 |
| Tunnel 接続不可 | localhost:5173 が起動しているか確認 |
| bun install 失敗 | `rm bun.lock && bun install` |
