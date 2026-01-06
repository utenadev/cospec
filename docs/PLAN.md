# 実装計画 (Implementation Plan)

## 2026-01-05 SPEC.md 仕様変更（認証委譲・Prompt-First）

### 目的
実装の現状およびユーザー決定に基づき、`SPEC.md` の記述を修正する。

### タスク
- [x] **FR-002: 要件ヒアリング (`hear`) の更新**
  - [x] 「対話形式」から「指令プロンプト生成」へ機能説明を変更
  - [x] AIエージェントによる主体的な実行フローを記述
- [x] **非機能要件: LLM連携の更新**
  - [x] APIキー環境変数管理の記述を削除
  - [x] 外部AIエージェント（CLI）への認証委譲と登録制（`agent add`）を明記

## 2026-01-05 cospec hear 改修 (Prompt-First)

### 目的
`cospec hear` を「対話型コマンド」から「AIエージェントへの指令生成コマンド」へ転換する。
AIエージェントがファイル操作ツールを用いて自律的にヒアリングとSPEC修正を行えるようにする。

### タスク
- [x] **プロンプトテンプレートの作成**
  - [x] `src/cospec/prompts/hearer.md` を新規作成
  - [x] 役割（アーキテクト）、行動指針（Pros/Cons提示）、ツール使用ルールを定義
- [x] **HearerAgent のリファクタリング**
  - [x] 正規表現による不明点抽出ロジックは「ヒント」として活用
  - [x] 外部LLM実行ロジックを削除し、プロンプト生成ロジックへ変更
- [x] **CLIコマンドの修正**
  - [x] `cospec hear` がプロンプトを標準出力するように変更
  - [x] ユーザーへのガイドメッセージ追加
- [x] **検証**
  - [x] テスト用 `tests/fixtures/spec_ambiguous.md` の作成
  - [x] 実際にGemini-CLIでプロンプトを読み込み、ヒアリング動作をシミュレーション

## 2026-01-05 CLI UX改善

### 実施済み
- [x] **CLI引数なし実行時の挙動改善**
  - [x] `main.py` の `Typer` 初期化時に `no_args_is_help=True` を追加
  - [x] `cospec` および `cospec agent` コマンドで引数なし実行時にヘルプが表示されることを確認
- [x] **Taskfile.yml の修正**
  - [x] `task check` 等で内部タスク呼び出しが失敗する問題を修正（文字列指定からYAMLオブジェクトへ変更）

## 2026-01-05 ドキュメント構造の整理・Overviewファイル分割

### 背景
docs/ ディレクトリが煩雑になり、OverviewDesignThinking.md と OverviewCodingTestingThinking.md に開発プロセス・ワークフローが混在して参照しにくかったため分割を検討。

### 計画
- [x] **ディレクトリ構造の整理**
  - [x] `.rules/` ディレクトリを新規作成（ガイドライン・思想ファイル）
  - [x] `docs/diary/` ディレクトリ作成（AIエージェントの作業ログ）
  - [x] `docs/report/` ディレクトリ作成（コードレビューレポート）
- [x] **ファイル分割・見直し**
  - [x] `OverviewDesignThinking.md` から開発プロセス（セクション3）を削除
  - [x] `OverviewCodingTestingThinking.md` からTaskfile/自動化（セクション3）を削除し、言語中立表現に修正
  - [x] `OverviewBasicRule.md` を新規作成（13K, 277行）
    - [x] 第1章: Human-AI協働のフロー設計（考え方）
    - [x] 第2章: go-task/Taskfile.yml開発インターフェース統一
    - [x] 第3章: PLAN.md / WorkingLog.md 実装計画
    - [x] 第4章: QAヒアリング → TDG実行 実践ワークフロー
- [x] **ファイル移動**
  - [x] Overview*ファイルを `.rules/` へ移動
  - [x] ダイアリー3件を `docs/diary/` へ移動
  - [x] レビューレポート6件を `docs/report/` へ移動
  - [x] 空のレビューファイル3件を削除
- [x] **参照更新**
  - [x] CLAUDE.md のガイドライン一覧を更新
  - [x] README.ja.md の3箇所の参照を修正
  - [x] README.md の1箇所を修正
  - [x] HISTORY_CONTEXT.md に BasicRule.md を追記
- [x] **Gitコミット**
  - [x] 全変更をステージング
  - [x] コミット作成: refactor: reorganize documentation structure and split Overview files
  - [x] リモートへプッシュ

## 2026-01-04 レビュー指摘事項への対応
- [x] **ドキュメント内のディレクトリ構造修正**
    - `docs/BLUEPRINT.md` を更新し、`src/cospec` レイアウトを反映。
- [x] **エージェントシステムの構造化**
    - `src/cospec/agents/` パッケージを作成。
    - `BaseAgent` および `ReviewerAgent` を実装。
    - `review` コマンドを新しいエージェントクラスを使うようにリファクタリング。
- [x] **`init` コマンドの強化**
    - `OverviewCodingTestingThinking.md` やその他のガイドラインファイルを生成対象に追加。
- [x] **言語設定の追加**
        - `CospecConfig` に `language` フィールドを追加（デフォルト: `ja`）。
        - `BaseAgent` でプロンプトに言語指示（日本語回答の強制）を自動付与するように更新。
    - [x] **バグ修正**
        - `review` コマンドで生成されるファイル名の日付変数が展開されない問題を修正（f-stringエスケープ解除）。

## 2026-01-04 ドキュメント整備
- [x] **READMEの更新**
    - `README.md` を現状の実装（`review` コマンド、外部ツール連携）に合わせて大幅更新。
    - `README.ja.md` (日本語版) を作成。

## 2026-01-04 レビュー精度向上
- [x] **コンテキスト認識の強化**
    - `Analyzer`: `WorkingLog.md` の除外設定を解除し、`PLAN.md` と共にコンテキストに含める。
    - `ReviewerAgent`: プロンプトを更新し、計画済みのタスク（PLAN.md記載）を「実装漏れ」として指摘しないよう指示を追加。

## 2026-01-04 Taskfile.yml 拡張と新コマンド実装
### Phase 1: Taskfile.yml 強化
- [ ] **基本タスクの追加**
  - [ ] `task hear`: `cospec hear` コマンドの実行タスク
  - [ ] `task test-gen`: `cospec test-gen` コマンドの実行タスク
  - [ ] `task docs:check`: ドキュメントとコードの整合性チェックタスク
  - [ ] `task build:package`: パッケージビルドタスクの追加

### Phase 2: `cospec hear` コマンド実装
- [x] **HearerAgent の作成**
  - [x] `src/cospec/agents/hearer.py` を作成
  - [x] SPEC.md から不明点を抽出するロジックを実装
  - [x] インタラクティブな質問生成機能を実装
- [x] **CLI コマンドの統合**
  - [x] `main.py` に `hear` コマンドを追加
  - [x] 必要な引数とオプションを定義
  - [x] ヘルプメッセージを追加
- [x] **テストの実装**
  - [x] `tests/test_hear.py` を作成
  - [x] モックを使用した単体テストを実装
  - [x] 統合テストを追加

### Phase 3: `cospec test-gen` コマンド実装
- [ ] **TestGeneratorAgent の作成**
  - [ ] `src/cospec/agents/test_generator.py` を作成
  - [ ] SPEC.md と PLAN.md からテストケースを自動生成するロジックを実装
  - [ ] pytest 形式のテストコード出力機能を実装
- [ ] **CLI コマンドの統合**
  - [ ] `main.py` に `test-gen` コマンドを追加
  - [ ] 出力先ディレクトリの指定オプションを追加
  - [ ] テンプレートエンジンの導入を検討
- [ ] **テストの実装**
  - [ ] `tests/test_test_gen.py` を作成
  - [ ] 生成されたテストコードの検証ロジックを実装

### Phase 4: ドキュメントと品質保証
- [ ] **ドキュメントの更新**
  - [ ] `docs/BLUEPRINT.md` に hear/test-gen の設計を反映
  - [ ] `docs/OverviewDesignThinking.md` に TDG フローを追記
  - [ ] `docs/OverviewCodingTestingThinking.md` に具体的な実装フローを追加
- [ ] **品質保証の強化**
  - [ ] 統合テスト環境の構築
  - [ ] E2E テストの実装
  - [ ] エラーハンドリングの改善

### Phase 5: 将来の拡張計画
- [ ] **Phase 2 計画 (Webサービス化)**
  - [ ] FastAPI ベースの API サーバー構成の設計
  - [ ] Web フロントエンドの要件定義
- [ ] **Phase 3 計画 (マルチ言語対応)**
  - [ ] Go 言語対応の設計検討
  - [ ] TypeScript/Node.js 対応の設計検討
- [ ] **CI/CD パイプライン構築**
  - [ ] GitHub Actions ワークフローの作成
  - [ ] 自動テストとデプロイの設定

## 2026-01-04 AI-Agent追加機能の実装

### Phase 6: AI-Agent追加コマンドの実装

- [x] **要件定義**
  - [x] README.ja.md の用語統一（AI → AI-Agent、AIコーディングエージェント → AI-Agent、Agentic Coding Tools → AI-Agent）
  - [x] README.ja.md に汎用性についての記述を追加
  - [x] 機能要件の詳細化

- [x] **設定管理の強化**
  - [x] `CospecConfig` に外部ファイルからの設定読み込み機能を追加
  - [x] 設定ファイルのパスを指定（デフォルト: `.cospec/config.json`）
  - [x] 設定ファイルの永続化機能

- [x] **`cospec agent add` コマンドの実装**
  - [x] CLI オプションの定義
    - [x] `--name`: AI-Agent名（必須）
    - [x] `--command`: 実行コマンド名（必須）
    - [x] `--help`: コマンドライン引数解析用のヘルプフラグ（デフォルト: `--help`）
  - [x] 指定コマンドの `--help` 実行と出力解析
    - [x] subprocess でヘルプ出力を取得
    - [x] ヘルプ出力から引数構造を推論
    - [x] プロンプトプレースホルダーの位置を検出
  - [x] ToolConfig の自動生成
    - [x] コマンド名と引数リストの構築
    - [x] プロンプトの渡し方（`{prompt}` プレースホルダー）を推論
  - [x] 設定ファイルへの保存
    - [x] 設定を `.cospec/config.json` に永続化
    - [x] 既存設定とのマージ処理

- [x] **`cospec agent list` コマンドの実装**
  - [x] 登録済み AI-Agent の一覧表示
  - [x] 各エージェントの設定（コマンド、引数）を表示

- [x] **`cospec agent test` コマンドの実装**
  - [x] 指定 AI-Agent の実行確認
  - [x] テストプロンプトを使用して正常動作を検証
  - [x] エラーハンドリングと診断メッセージ

- [x] **テストの実装**
  - [x] `tests/test_agent.py` を作成
  - [x] モックを使用したコマンド実行テスト
  - [x] ヘルプ出力解析ロジックのテスト
  - [x] 設定ファイルの読み書きテスト

- [ ] **ドキュメントの更新**
  - [ ] `README.ja.md` に agent コマンドの使用方法を追加
  - [ ] `docs/BLUEPRINT.md` に設定管理の設計を反映
  - [ ] `AGENTS.md` に新しいコマンドの説明を追加

## 2026-01-04 AI-Agent選択ロジックの実装

### Phase 7: AI-Agent自動選択の強化

- [ ] **要件定義**
  - [x] hear, test-gen: 開発利用ツールと同じを優先
  - [x] review: 利用ツール以外を勧める
  - [x] review: 2ツールで実行する

- [ ] **設定管理の拡張**
  - [ ] `COSPEC_DEV_TOOL` 環境変数の追加
  - [ ] `CospecConfig` に `dev_tool` フィールド追加
  - [ ] 設定ファイルからの読み込み対応

- [ ] **ツール選択ロジックの実装**
  - [ ] **hear/test-gen 用ロジック**:
    - [ ] `dev_tool` が設定されていればそれを使用
    - [ ] 未設定なら `default_tool` を使用
  - [ ] **review 用ロジック**:
    - [ ] 利用ツール以外からランダムに選択
    - [ ] 最低2つのツールが登録されていること確認
    - [ ] ツールが足りない場合はデフォルトを使用

- [ ] **レビューの複数ツール対応**
  - [ ] 2つのツールで順次レビューを実行
  - [ ] 2つのレポートを保存
  - [ ] 比較サマリーを表示

- [ ] **テストの実装**
  - [ ] ツール選択ロジックのテスト
  - [ ] 複数ツールレビューのテスト

- [x] **ドキュメントの更新**
  - [x] `README.ja.md` に自動選択ロジックの説明を追加
  - [x] `AGENTS.md` を更新

### 実施内容の記録
- [x] 環境変数 `COSPEC_DEV_TOOL` の動作確認
- [x] 前提条件（2つ以上のAI-Agent）の明記
- [x] ツール選択ロジックのドキュメント化

### 未解決の問題

#### 1. レビュープロンプトのサイズ問題
- **現象**: レビュー時のプロンプトが 100,472文字（約100KB）あり、システムの引数長制限を超えてエラーになる
- **原因**: `ProjectAnalyzer.collect_context()` が以下のすべてを全文読み込んでいる
  - `docs/*.md`: すべてのマークダウンファイル
  - `src/cospec/**/*.py`: すべてのPythonファイル
- **影響**: `qwen`, `opencode` などのCLIツールに直接引数でプロンプトを渡せない

#### 2. 環境変数の読み込み問題
- [x] `.env` ファイルからの環境変数読み込みが機能した（`env_file=".env"`）
- [x] `COSPEC_DEV_TOOL` 環境変数が正しく読み込める

#### 3. opencode コマンド実行時のエラー
- [x] `opencode` コマンド実行時のエラー
  - エラー: `[Errno 7] Argument list too long: 'opencode'`
  - 原因: プロンプトが直接引数で渡されている
  - 解決: `--file` オプションで一時ファイル経由で渡す方式を実装

### 実施した解決策

#### コンテキストサイズ最適化
- [x] **実装**: `BaseAgent.run_tool()` にファイルベースアプローチを実装
  - [x] 長いプロンプト（8000文字超）を一時ファイルに保存
  - [x] `{file}` プレースホルダー対応（opencode 用: `--file /tmp/xxx.txt "このファイルを..."`）
  - [x] `{prompt}` プレースホルダー対応（qwen 用: `@/tmp/xxx.txt`）
  - [x] 一時ファイルの適切なクリーンアップ
- [x] **設定ファイルの更新**:
  - `opencode` の args を `["--file", "/tmp/cospec_prompt.txt", "このファイルをプロンプトとして評価して"]` に変更
  - `dev_tool` を `"opencode"` に設定

#### ツール選択ロジックの実装
- [x] **実装**: ツール選択ロジックの実装
  - [x] `CospecConfig.dev_tool` フィールド追加
  - [x] `.env` ファイル読み込み有効化
  - [x] `select_tool_for_development()`: hear/test-gen 用
  - [x] `select_tool_for_review()`: review 用
- [x] **CLI コマンド**:
  - [x] `hear`, `test-gen`: 自動選択ロジック適用
  - [x] `review`: 2ツールで順次レビュー実行、サマリー表示

#### ドキュメント更新
- [x] README.ja.md に自動選択ロジックの説明を追加
- [x] README.ja.md に前提条件（2つ以上のAI-Agent）を明記
- [x] PLAN.md に問題点と解決策を記録
- [x] PLAN.md に実施内容を記録

#### 品質保証
- [x] ruff: All checks passed
- [x] mypy: Success: no issues found
- [x] pytest: 24 passed

#### 未完了
- [x] 実機動作確認
  - [x] `select_tool_for_review()` のロジック検証
  - [x] opencode が除外され、qwen と MistralVibe が選択されることを確認

## 2026-01-04 AI-Agent追加とopencode問題の解決

### AI-Agentの追加作業
- [x] **Crush AI-Agent の追加**
  - [x] `cospec agent add Crush --command crush` を実行
  - [x] 設定ファイルに追加（`crush run {prompt}`形式）
  - [x] コマンド誤りを修正（`{prompt}` → `run {prompt}`）

- [x] **MistralVibe AI-Agent の追加**
  - [x] `cospec agent add MistralVibe --command vibe` を実行
  - [x] 設定ファイルに追加（`vibe -p {prompt}`形式）

- [x] **Gemini-CLI AI-Agent の追加**
  - [x] `cospec agent add Gemini-CLI --command gemini` を実行
  - [x] 設定ファイルに追加（`gemini {prompt}`形式）

- [x] **不要なAI-Agentの削除**
  - [x] ダミーAI-Agent（`mycli`）を設定ファイルから削除
  - [x] 使わないAI-Agent（`MistralVibe`, `Crush`）を削除

- [x] **設定ファイルの整理**
  - [x] `qwen` → `Qwen` に変更（大文字スタートに統一）
  - [x] `opencode` → `Opencode` に変更（大文字スタートに統一）
  - [x] ダミーAI-Agent（`mycli`）を削除
  - [x] `--print-logs` オプションを削除（不要なログ出力を抑制）
  - [x] 引数を修正（`--file` オプションを削除し、`run {prompt}`形式に統一）

### opencode 問題の解決
- [x] **問題の根本原因調査**
  - [x] opencode CLIはセッション管理型エージェントであり、stdoutには回答を出力しない
  - [x] subprocess経由ではファイルに生成された結果をキャプチャできない
  - [x] 対話型環境では動作可能だが、非対話型のCLI連携には不向き

- [x] **実機テスト**
  - [x] 直接コマンドでの動作確認（`echo "プロンプト" | opencode run`）
  - [x] 設定修正後の動作確認（「明日の横浜の天気」で正常応答を確認）

- [x] **結論**
  - Opencodeは外部ツールからsubprocess呼び出しするユースケースに適していない
  - CLI連携にはqwenのような直接stdoutに応答を出力するツールが適している
  - ドキュメントに制限事項を明記し、より簡潔なCLIツールを推奨すべき

> All checks passed.

