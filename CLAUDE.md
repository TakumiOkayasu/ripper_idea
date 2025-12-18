# Ripple Idea - Claude Code用プロンプト

## プロジェクト概要

### Ripple Idea (波紋アイデア)

- お題を入力すると、波紋のように円形にアイデアが広がっていくWebアプリケーション
- 中央のお題から放射状に展開するラジアルツリー構造
- ローカルストレージで永続化
- Vercel + Railway でデプロイ
- デスクトップ・モバイル両対応

**ユーザーエクスペリエンス**:

```text
      ステップ1: お題入力
              ↓
       「プロダクト開発」
              ↓
      ステップ2: アイデア生成
              ↓
         🌊 波紋展開
      ／  │  ｜  ｜  ＼
   マーケ 企画 技術 デザイン 営業
      ↓
  各ノードをクリック → さらに波紋が広がる
  
  UI: ラジアルツリーが波紋のように見える円形配置
```

## 技術スタック

### フロントエンド

- **フレームワーク**: React 19 + TypeScript (Vite)
- **ビジュアライゼーション**: D3.js (ラジアルツリー)
- **スタイリング**: シンプルなCSS (UIライブラリ不使用)
- **ストレージ**: localStorage (JSON形式)
- **パッケージマネージャー**: Bun (npm代わり)
- **デプロイ**: Vercel

### バックエンド

- **フレームワーク**: Python + FastAPI
- **LLM**: Claude API (claude-opus-4-1 推奨)
- **非同期**: asyncio で複数案並列生成
- **デプロイ**: Railway

## アーキテクチャ

```text
┌──────────────────────────┐
│  React Front (Vite)      │
│  - ラジアル波紋表示      │
│  - localStorage          │
└───────────┬──────────────┘
            │ HTTP
            ↓
┌──────────────────────────┐
│  FastAPI Backend         │
│  - Claude API連携        │
│  - アイデア波紋生成      │
└──────────────────────────┘
```

## データモデル

### Node (アイデアノード)

```python
{
  "id": "uuid",
  "content": "アイデアテキスト",
  "parentId": "parent_uuid | null",
  "depth": 0,
  "children": [],
  "createdAt": "ISO8601",
  "confidence": 0.85
}
```

### Session (セッション)

```javascript
{
  "sessionId": "uuid",
  "rootTopic": "お題",
  "rootNode": Node,
  "timestamp": "ISO8601"
}
```

## API仕様

### POST /api/ideas/generate

複数のアイデアを並列生成

**リクエスト**:

```json
{
  "parentContent": "親となるアイデアのテキスト",
  "context": "ユーザーが提供するコンテキスト(オプション)",
  "count": 3
}
```

**レスポンス**:

```json
{
  "ideas": [
    {"content": "アイデア1", "confidence": 0.92},
    {"content": "アイデア2", "confidence": 0.88},
    {"content": "アイデア3", "confidence": 0.85}
  ]
}
```

## 実装ガイドライン

### フロントエンド開発

**ファイル構造**:

```text
src/
├── components/
│   ├── RadialTree.tsx       # D3.jsラジアルツリー
│   └── ControlPanel.tsx     # 入力フォーム + ボタン
├── hooks/
│   ├── useIdeaTree.ts       # ツリー状態管理
│   └── useLocalStorage.ts   # ストレージ操作
├── types/
│   └── index.ts             # 型定義
├── utils/
│   └── api.ts               # API呼び出し
└── App.tsx
```

**重点事項**:

- D3.jsのラジアルツリーレイアウトは軽量に
- ノードクリック → APIでアイデア生成 → ツリー更新
- localStorage には JSON.stringify で保存
- エラーハンドリング(API失敗時の再試行)

### バックエンド開発

**ファイル構造**:

```text
backend/
├── .devcontainer/
│   ├── devcontainer.json      # DevContainer 設定
│   └── Dockerfile             # Python 環境定義
├── main.py                    # FastAPI アプリケーション
├── claude_client.py           # Claude API ラッパー
├── models.py                  # Pydantic モデル定義
├── requirements.txt           # 依存パッケージ
├── Procfile                   # Railway 起動設定
├── railway.toml               # Railway 設定(オプション)
├── .env.example               # 環境変数テンプレート
└── .gitignore                 # .env を除外
```

**重点事項**:

- Claude APIの非同期呼び出し (asyncio)
- プロンプトエンジニアリング: 創発的なアイデア生成に最適化
- CORS対応 (Vercel からのリクエスト許可)
- Rate limiting (Claude API の制限を考慮)
- エラーレスポンス統一
- Railway 環境での Python 3.11+ 対応
- 環境変数: `CLAUDE_API_KEY`, `FRONTEND_URL` (CORS用)

**Claude API呼び出しのプロンプト例**:

```text
与えられたテーマ「{theme}」に関連する、創発的で実用的なアイデアを3つ生成してください。

要件:
- 各アイデアは20文字〜100文字
- 既知の概念の組み合わせではなく、新しい視点を提供するもの
- 実装可能性を考慮
- JSON形式で返却: [{"idea": "...", "reasoning": "..."}, ...]
```

**Procfile**:

```text
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**requirements.txt最小構成**:

```text
fastapi
uvicorn[standard]
anthropic
pydantic
python-dotenv
```

## 開発フロー

1. **バックエンド最小実装** (優先)
   - Claude API ラッパー作成
   - アイデア生成エンドポイント実装
   - ローカルで動作確認

2. **フロントエンド実装**
   - React + Vite プロジェクト初期化
   - D3.js ラジアルツリーコンポーネント
   - API連携
   - ローカルストレージ統合

3. **統合テスト**
   - エンドツーエンド動作確認
   - API レスポンスのハンドリング

## デプロイ

### バックエンド (Railway)

**セットアップ手順**:

1. **Railway アカウント作成済みを前提**
2. **GitHub リポジトリ連携**
   - Railway Dashboard → New Project → GitHub 連携
   - Backend ブランチ選択
3. **環境変数設定**
   - Railway Dashboard → Variables
   - `CLAUDE_API_KEY`: Claude API キー
   - `FRONTEND_URL`: `https://ripple-idea.vercel.app` (本番時)
4. **自動デプロイ有効化**
   - GitHub Push → 自動デプロイ開始
   - デプロイ完了時に Railway URL 取得
5. **ローカル開発**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   export CLAUDE_API_KEY="sk-..."
   uvicorn main:app --reload
   ```

**Railway デプロイ後の確認**:

```bash
curl https://your-app.railway.app/health
# {"status": "ok"} が返される
```

### フロントエンド (Vercel)

1. Vercel Dashboard → New Project → GitHub 連携
2. Frontend ブランチ選択
3. Build Settings で以下を設定:
   - **Build Command**: `bun run build`
   - **Install Command**: `bun install`
   - **Output Directory**: `dist`
4. Environment Variables 設定
   - `VITE_API_URL`: Railway API の URL (例: `https://your-app.railway.app`)
5. Deploy

**本番環境 CORS設定**:

- バックエンド CORS許可オリジン: `https://ripple-idea.vercel.app`
- Railway → Variables → `FRONTEND_URL` = `https://ripple-idea.vercel.app`

## 非機能要件

- **API応答時間**: < 3秒 (複数案並列生成)
- **フロント初期ロード**: < 2秒
- **ツリーノード数**: 100以下を推奨
- **ブラウザ対応**: モダンブラウザ (Chrome, Firefox, Safari)

## セキュリティ

- Claude API Key は **環境変数** で管理 (GitHub コミットしない)
- `.env` ファイルは `.gitignore` に含める
- フロント ↔ バック通信は **HTTPS** (本番)
- CORS設定を厳密に (Vercelドメインのみ許可)
- `FRONTEND_URL` 環境変数で許可オリジンを制御

**ローカル開発時の CORS設定**:

```python
# main.py
allow_origins = [
    "http://localhost:5173",  # Vite dev server
    os.getenv("FRONTEND_URL", "http://localhost:5173")
]
```

## ローカル開発環境構築

### バックエンド (DevContainer推奨)

**DevContainer を使う場合 (推奨)**:

1. **前提条件**:
   - Docker Desktop インストール済み
   - VS Code + Dev Containers 拡張インストール

2. **初期化**:

   ```bash
   cd backend
   # .devcontainer ディレクトリが自動生成される
   # VS Code で "Reopen in Container" を選択
   ```

3. **コンテナ内で開発**:

   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # .env に CLAUDE_API_KEY を設定
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   # http://localhost:8000 でアクセス可能
   ```

**DevContainer ファイル構造**:

```text
backend/
├── .devcontainer/
│   ├── devcontainer.json      # DevContainer 設定
│   └── Dockerfile             # Python 環境定義
├── main.py
├── requirements.txt
└── .env.example
```

**devcontainer.json テンプレート**:

```json
{
  "name": "Idea Expansion Tool Backend",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "remoteUser": "vscode",
  "forwardPorts": [8000],
  "portsAttributes": {
    "8000": {
      "label": "FastAPI",
      "onAutoForward": "notify"
    }
  }
}
```

**ローカル開発時の注意**:

- コンテナ内で動作するため、localhost:8000 でアクセス可能
- `--host 0.0.0.0` 指定で外部からアクセス可能
- 環境変数は `.env` ファイルで管理
- Python パッケージは自動インストール (postCreateCommand)

**DevContainer のメリット**:

- OS/環境依存なし
- Python バージョン統一
- 本番環境 (Railway) と同一環境でテスト可能
- チーム開発で環境ズレがない

---

**DevContainer 未使用の場合 (ローカル venv)**:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env に CLAUDE_API_KEY を設定
uvicorn main:app --reload
# http://localhost:8000 で起動
```

**推奨**: DevContainer を使うことで環境問題がなくなります。

**フロントエンド**:

```bash
cd frontend
bun install
bun run dev
# http://localhost:5173 で起動
# VITE_API_URL=http://localhost:8000 設定済みなら自動連携
```

**ビルド**:

```bash
bun run build
# dist/ ディレクトリに出力
```

## 今後の拡張案

- セッション複数保存 + 切り替え機能
- アイデアのCSV/JSONエクスポート
- ノードの手動編集
- 関連度スコアに基づくフィルター

## 質問・確認事項

実装中に以下が発生したら確認してください:

1. Claude API のプロンプト精度が低い → プロンプト改善検討
2. D3.js のパフォーマンス問題 → キャンバスベースの代替検討

## Railway 連携必須事項

- GitHub リポジトリを public にする(Railway連携用)
- Railway アカウント: アカウント作成済み
- Claude API Key: 環境変数に設定
- デプロイ後の URL を Vercel CORS 設定に反映

## Bun 使用時の注意点と既知の問題

### メリット

- **速度**: npm/yarn より 3-10倍高速
- **一体型**: パッケージマネージャー + ランタイム + テストランナー
- **ディスク使用量**: node_modules サイズが小さい

### 既知の問題と対応

#### 1. Vercel デプロイ時の互換性

**問題**: Vercel が Bun を自動検出しない可能性
**対応**:

- `package.json` に以下を追加:

  ```json
  {
    "packageManager": "bun@latest"
  }
  ```

- または vercel.json で明示指定:

  ```json
  {
    "buildCommand": "bun install && bun run build"
  }
  ```

#### 2. 一部 npm パッケージとの互換性

**問題**: Bun の ESM 実装が npm 標準と若干異なる
**対応**:

- `package.json` に `"type": "module"` を明示
- npm package が問題ある場合は、`bun.lock` を削除して再インストール

#### 3. Vite 連携

**問題**: ほぼなし。Bun + Vite の組み合わせは安定
**推奨**: Vite 7.0+ 使用

#### 4. D3.js 互換性

**問題**: ほぼなし。D3.js は ESM 対応済み
**確認**: `bun run build` で error なく完了すれば問題なし

### 推奨チェックリスト

- [ ] `package.json` に `"packageManager": "bun@latest"` を追加
- [ ] `bun.lock` をコミットに含める (Bun 1.1+ はテキスト形式)
- [ ] ローカルで `bun run build` → `dist/` 生成確認
- [ ] Vercel デプロイ前に build command テスト
- [ ] 本番デプロイ後に API 呼び出し確認

### 互換性確認コマンド

```bash
# lock ファイルリセット(問題発生時)
rm bun.lock
bun install

# ビルド検証
bun run build
```

### 最終判定

**Bun 使用は問題なし。** Vite + React の組み合わせは安定性が高く、Vercel デプロイも対応済み。ただし新興ツールのため、問題発生時は npm への切り替えで対応可能。

## DevContainer 使用時の注意点

### セットアップ

**初回のみ**:

```bash
# VS Code コマンドパレット (Ctrl+Shift+P) で:
# "Dev Containers: Reopen in Container" を実行
# または右下の "Reopen in Container" をクリック
```

### 開発ワークフロー

1. **コンテナ起動後の確認**:

   ```bash
   python --version  # Python 3.11+ 確認
   pip list          # 依存パッケージ確認
   ```

2. **開発中の作業**:

   ```bash
   # ホットリロード有効で起動
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # ローカルの http://localhost:8000 でアクセス
   ```

3. **パッケージ追加時**:

   ```bash
   # コンテナ内で
   pip install <package>
   pip freeze > requirements.txt
   
   # 変更をコミット
   git add requirements.txt
   git commit -m "Add <package>"
   ```

### Docker Desktop との連携

- **メモリ設定**: Docker が充分なメモリを持つことを確認
  - 推奨: 4GB 以上
  - 設定: Docker Desktop → Settings → Resources

- **ボリュームマウント**: ホスト OS のファイルがコンテナ内で同期
  - ホスト: `./backend/main.py`
  - コンテナ: `/workspace/backend/main.py`

### トラブルシューティング

**問題**: コンテナが起動しない
**対応**:

```bash
# DevContainer 削除して再構築
# VS Code コマンドパレット:
# "Dev Containers: Rebuild Container"
```

**問題**: `pip install` が遅い
**対応**:

- Docker Desktop のメモリを増加
- または pip キャッシュをクリア: `pip cache purge`

**問題**: Poetry/Pipenv を使いたい
**対応**:

- requirements.txt を使うことを推奨 (Railway 標準)
- 必要ならば devcontainer.json で `postCreateCommand` 修正

### Railway デプロイ時の互換性

- DevContainer で development した内容は Railway でもそのまま動作
- `requirements.txt` が一致していれば環境完全一致
- 本番前に DevContainer 環境で最終テスト推奨

### 推奨チェックリスト (DevContainer)

- [ ] Docker Desktop インストール済み
- [ ] VS Code Dev Containers 拡張インストール済み
- [ ] `.devcontainer/devcontainer.json` が存在
- [ ] `"Reopen in Container"` で起動確認
- [ ] `uvicorn main:app --reload` で FastAPI 起動確認
- [ ] `http://localhost:8000/health` で API 応答確認
- [ ] パッケージ追加時に `requirements.txt` 更新
