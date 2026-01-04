# cospec

**Collaborative Specification CLI** - 人間とAIエージェントが協働して高品質なソフトウェアを構築するためのプラットフォーム。

`cospec` は **"Doc-as-Context"（ドキュメントこそがコンテキスト）** と **"Consistency-First"（整合性第一）** という哲学に基づいています。コードが仕様を正しく反映していることを保証し、明確なトレードオフ分析を通じて人間の意思決定を支援します。

## コアコンセプト

- **Codebase as Context**: ドキュメントをAIにとっての正解データ（Ground Truth）とします。
- **Consistency First**: 実装前にドキュメントとコードの不整合を排除します。
- **Decision Support**: 選択肢とメリット・デメリット（Pros/Cons）を提示し、人間の意思決定を支えます。

## 主な機能

### 実装済み
- **`cospec init`**: 推奨されるディレクトリ構造（`docs/`, `Taskfile.yml`）とガイドラインファイルを展開し、プロジェクトを初期化します。
- **`cospec review`**: 外部AIツール（`qwen`, `opencode` 等）を使用して、コードベースとドキュメントの整合性を分析します。

### 計画中
- **`cospec hear`**: 対話形式で `SPEC.md` の曖昧さを解消するためのヒアリングを行います。
- **`cospec test-gen`**: 仕様書からテストケースを生成します（Test-Driven Generation）。

## アーキテクチャ

`cospec` はAIコーディングエージェントのオーケストレーターとして機能します。重厚なLLMランタイムを内包する代わりに、インストール済みのCLIツール（Agentic Coding Tools）に処理を委譲します。

- **現在の連携先**: `qwen` (Qwen Code), `opencode`.
- **コンテキスト認識**: `cospec` は関連するコンテキスト（ドキュメント + コード）を自動的に収集し、これらのツールに対して効果的なプロンプトを構築します。

## はじめに

### 前提条件

- Python 3.10以上
- [go-task](https://taskfile.dev/) (任意ですが推奨)
- 外部ツール: `qwen` または `opencode` がインストールされ、パスが通っていること。

### インストールとセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/your-org/cospec.git
cd cospec

# 環境セットアップ (venv作成と依存関係インストール)
task setup
```

### 使い方

#### 1. プロジェクトの初期化
```bash
cospec init
```
これにより、仕様書やガイドライン（`OverviewCodingTestingThinking.md`）のテンプレートを含む `docs/` ディレクトリが作成されます。

#### 2. 整合性レビューの実行
```bash
# Qwen Codeを使用 (デフォルト)
cospec review --tool qwen

# OpenCodeを使用
cospec review --tool opencode
```
エージェントは `docs/` と `src/` ファイルを分析し、Markdown形式のレポートを `docs/review_YYYYMMDD_...` に生成します。

## 設定

環境変数（`.env` ファイル等）を通じて `cospec` を設定できます。

| 変数名 | デフォルト | 説明 |
|----------|---------|-------------|
| `COSPEC_LANGUAGE` | `ja` | AI応答の言語設定 (`ja`, `en`)。デフォルトは日本語です。 |
| `COSPEC_DEFAULT_TOOL` | `qwen` | レビューに使用するデフォルトツール。 |

## 開発について

エージェント向けの指示については [GEMINI.md](./GEMINI.md) を、詳細な仕様については [docs/](./docs/) を参照してください。

- `task test`: テストの実行
- `task lint`: リインターの実行
- `task check`: 全チェックの実行

## ライセンス

MIT
