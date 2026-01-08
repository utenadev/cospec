# BLUEPRINT: cospec

## 1. 技術スタック (Python CLI)
- **CLI Framework**: `Typer` (直感的なコマンド定義)
- **UI Library**: `Rich` (Markdown表示、テーブル、プログレスバー)
- **LLM Client**: `OpenAI SDK` or `LangChain` (将来的に抽象化)
- **Settings**: `Pydantic Settings` (堅牢な設定管理)
- **Task Runner**: `go-task` (Taskfile.yml)

## 2. アーキテクチャ

### 2.1 ディレクトリ構成
```
cospec/
├── src/
│   └── cospec/
│       ├── main.py            # Entry point
│       ├── core/              # Business Logic
│       │   ├── analyzer.py    # Codebase scanning
│       │   └── config.py      # Configuration & Settings
│       ├── agents/            # Agent Definitions (Wrappers for External Tools)
│       │   ├── base.py        # Base Agent logic
│       │   └── reviewer.py    # Reviewer Agent
│       ├── prompts/           # System Prompts for Agents
│       └── templates/         # Spec/Test templates
├── docs/                  # Project Context
├── tests/
└── Taskfile.yml
```

## 3. エージェント定義 (Agent Definitions)

本システムでは、以下の役割を持つ「専門エージェント」を定義し、タスクに応じて呼び出します。

### 3.1 Reviewer Agent (The Auditor)
- **役割**: 整合性チェックの専門家。コードは書かず、指摘に徹する。
- **System Prompt骨子**:
    > あなたは厳格なソフトウェア監査官です。
    > 提供されたドキュメント(SPEC, BLUEPRINT)とコード(Impl, Tests)を比較し、
    > 以下の観点で矛盾を洗い出してください。
    > 1. 要件の網羅性: SPECにある機能がテストされているか？
    > 2. ドキュメントの整合性: READMEとSPECに矛盾はないか？
    > 3. ルール準拠: `GuidlineCodingTesting.md` (型ヒント、Mock使用)に従っているか？
    > 
    > 褒める必要はありません。問題点と具体的な修正案、重要度(High/Mid/Low)をリストアップしてください。

### 3.2 Interviewer Agent (The Architect)
- **役割**: 要件定義の専門家。ユーザーの曖昧な発言を構造化する。
- **System Prompt骨子**:
    > あなたは熟練したソフトウェアアーキテクトです。
    > ユーザーの要望を実現するための技術的・仕様的な決定事項を特定してください。
    > 未決定事項については、**必ず複数の選択肢(Option A/B/C)**を提示し、
    > それぞれの **Pros(メリット)** と **Cons(デメリット)** を明確に説明して、ユーザーに決定を促してください。

### 3.3 Coder Agent (The Implementer)
- **役割**: 実装担当。テストを通すコードを書く。
- **System Prompt骨子**:
    > あなたはPythonのエキスパート開発者です。
    > `SPEC.md` と既存のテストコードに従い、実装を行ってください。
    > ガイドラインに従い、型ヒントを完備し、Docstringを記述してください。

## 4. データフロー (Review Command)

1. **User**: `cospec review` を実行。
2. **Analyzer**: 
    - `README*.md`, `docs/*.md` を読み込む。
    - `src/`, `tests/` のファイルリストと主要コード（トークン制限に注意）を読み込む。
3. **LLM (Reviewer)**: 整合性チェックを実行。
4. **Reporter**: `docs/review_{date}_{agent}.md` を生成。
5. **UI**: レポートの概要をターミナルに表示し、詳細ファイルへのリンクを表示。

## 5. 将来の拡張
- **Git Integration**: レビュー結果をGitHub PRのコメントとして投稿する機能。
- **Auto Fix**: `review` の指摘事項のうち、単純な修正（Typos, Style）を自動適用する `cospec fix`。