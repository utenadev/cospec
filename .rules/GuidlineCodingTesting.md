# 概要: LLM協働開発のためのコーディング・テストガイド

このドキュメントは、人間とLLMがソフトウェアを共同開発するためのコーディングおよびテストの標準指針です。
目標は、PythonであれGolangであれ、**「AIエージェントが理解しやすく、かつ自律的に検証可能なコード」**を書くことです。

## 1. コーディング標準: "Guardrails for AI"

LLMは確率的にコードを生成するため、厳格な制約（ガードレール）が必要です。言語機能を用いて、AIの「幻覚」を防ぎます。

### 1.1 強い型付け (Strong Typing)
**言語を問わず、型定義は「LLMへの最強のドキュメント」です。**

- **Pythonの場合**:
    - `Any` は禁止（AIに「何でもいい」と伝えるとバグります）。
    - `Pydantic` モデルを使用して、データ構造を強制する。
- **Golangの場合 (将来)**:
    - `interface` を小さく定義し、構造体の役割を明確にする。
    - `struct` タグを活用し、JSON等の入出力形式を明示する。
- **TypeScriptの場合 (将来)**:
    - `Zod` 等で実行時バリデーションを行う。

### 1.2 自己文書化コード (Self-Documenting Code)
- **ドキュメントコメント**:
    - 関数の中身を書く**前**に、ドキュメントコメント（例: PythonではDocstring、Goではコメントブロック）を書くフローを推奨します。
    - LLMは関数名とドキュメントコメントを見て、実装を補完します。

## 2. テスト戦略: "Test-Driven Generation (TDG) with Interactive Hearing"

人間が全てのテストコードを書く必要はありません。
重要なのは、**「何が正解か（テストケース）」をAIと合意すること**です。

### 2.1 TDGの目的と価値
実装とテストを分離することで、以下のメリットを得られます:
- **期待値の明確化**: テストケースを先に定義することで、実装前に「正解」を共有できる
- **品質保証の自動化**: AIが自律的にテストを生成・実行し、開発の安全網とする
- **リファクタリングの安全性**: テストがガードレールとなり、コード整理を恐れずに行える

詳細な実践フローについては `GuidlineBasicRule.md` を参照してください。

### 2.2 外部依存のモック化
AIエージェントが試行錯誤する際、実際のAPIを叩くとレート制限にかかったり、データが汚染されたりします。
- **原則**: 開発・テスト時の外部I/O（HTTP, DB）はすべてモック可能にする。
- **Dependency Injection**: コンストラクタでAPIクライアント等を注入する設計にする（PythonでもGoでも共通のベストプラクティス）。

## 3. 技術スタック別ガイドライン

プロジェクトのフェーズや要件に応じて、適切なスタックを選択します。

### A. Python CLI (Current Default)
現在の `cospec` などのCLIツール開発標準です。
- **Core**: Typer, Pydantic, HTTPX
- **Testing**: Pytest, Pytest-Asyncio, Pytest-Mock
- **Lint/Format**: Ruff, Mypy

### B. Python Web/Server (Future)
データ処理やAPIサーバー向け。
- **Core**: FastAPI
- **Interface**: OpenAPI (schema-first development)

### C. Golang / High Performance (Future)
バイナリ配布や高並行処理が必要な場合。
- **Project Layout**: `Standard Go Project Layout` (cmd/, internal/, pkg/)
- **Core**: Cobra (CLI), Echo/Gin (Web)
- **Lint**: golangci-lint
