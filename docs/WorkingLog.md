# 作業ログ (Working Log): cospec

## 2026-01-05 SPEC.md 仕様変更（認証委譲・Prompt-First）

### 背景
`cospec hear` の Prompt-First アプローチへの移行に伴い、`SPEC.md` の記述が実態と乖離していたため修正が必要となった。
また、AIエージェントの認証（APIキー）についても、`cospec` 側での環境変数管理を廃止し、外部ツールへの委譲を明確化する方針が決定された。

### 実施内容
- **FR-002 (`hear`) の更新**:
  - 機能を「AI指令プロンプト生成」と再定義。
  - AIエージェントが主体となってファイル操作を行うワークフローを明記。
- **非機能要件の更新**:
  - APIキーの環境変数管理に関する記述を削除。
  - 認証は各AIエージェント（CLIツール）に委譲し、`cospec agent add` で登録されたツールを利用することを明記。

### 参照
- PLAN.md: 2026-01-05 SPEC.md 仕様変更（認証委譲・Prompt-First）

## 2026-01-05 cospec hear 改修 (Prompt-First)

### 背景
当初の `cospec hear` 実装は、正規表現で抽出した不明点を外部LLMコマンドに投げ、回答を表示するだけの「一方通行」な仕様だった。
AIエージェントが主体となってヒアリングを行い、`SPEC.md` を直接修正できるようにするため、「Prompt-First」アプローチへの移行を決定。

### 実施内容
- **プロンプトテンプレート (`src/cospec/prompts/hearer.md`) の作成**:
  - AIエージェント（Hearer）の役割、行動指針、ツール使用ルールを定義。
  - 曖昧さを解消するための「Pros/Cons付き選択肢提示」を明文化。

- **HearerAgent のリファクタリング**:
  - 正規表現ロジックは「自動ヒント生成」として再利用。
  - 外部LLM実行ロジックを全削除し、プロンプト生成ロジックへ変更。

- **CLIコマンド (`cospec hear`) の刷新**:
  - 対話モードを廃止し、AIエージェントへの指令書（System Prompt）を出力する仕様に変更。
  - ユーザーはこの出力をコピーして、任意のエージェント（Gemini, Claude等）に指示できる。

### 品質保証
- `cospec hear` コマンドがエラーなくプロンプトを出力することを確認。
- プロンプトに正規表現スキャン結果（ヒント）が正しく埋め込まれることを確認。
- `task check` により既存機能への影響がないことを確認。

### 参照
- PLAN.md: 2026-01-05 cospec hear 改修 (Prompt-First)

## 2026-01-05 CLI UX改善

### 実施内容
- **CLI引数なし実行時の挙動改善**:
  - `cospec` コマンドを引数なしで実行した際にエラー（Missing command）になる問題を修正。
  - `typer.Typer(no_args_is_help=True)` を設定し、ヘルプメッセージが表示されるように変更。
  - メインコマンド (`app`) と `agent` コマンド (`agent_app`) の両方に適用。

- **Taskfile.yml の修正**:
  - `task check` および `task quality:check` における内部タスク呼び出しの構文エラーを修正。
  - 文字列指定（`'task: lint'`）からYAMLオブジェクト指定（`task: lint`）へ変更し、`go-task` が正しく解釈できるようにした。

### 品質保証
- `task check` を実行し、Lint, Type Check, Test がすべてパスすることを確認。

### 参照
- PLAN.md: 2026-01-05 CLI UX改善

## 2026-01-05 ドキュメント構造の整理・Overviewファイル分割

### 背景・動機
当初、`docs/` ディレクトリ配下にすべてのドキュメントがフラットに配置されていたが、以下の課題が生じた:
- Overviewファイル（設計思想・開発ガイドライン）に開発プロセスとワークフローが混在し、参照性が悪い
- AIレビューレポート（6ファイル）とダイアリー（3ファイル、合計約32K）が docs/ 直下に散乱
- 空のレビューファイル（3ファイル）が残っている

### 実施内容

#### 新しいディレクトリ構造の確立
- **`.rules/`**: ガイドライン・思想ファイルの専用ディレクトリ
  - プロジェクトのルート直下に配置し、ドキュメントディレクトリの煩雑さを解消
- **`docs/diary/`**: AIエージェントの作業ログ（CLAUDE_DIARY.md, GEMINI_DIARY.md, OPENCODE_DIARY.md）
- **`docs/report/`**: コードレビューレポート（2026-01-04の6件）
- 不要ファイル削除: 空のレビューファイル3件（232706_opencode.md, 233009_opencode.md, 233113_qwen.md）

#### Overview*ファイルの分割と再編成
- **`OverviewDesignThinking.md` の再編**（7.8K → 5.0K）
  - セクション3「開発プロセス」を削除し、設計思想とプロジェクト拡張性のみに焦点化
  - Codebase as Context 哲学と SPEC/BLUEPRINT の役割の明確化

- **`OverviewCodingTestingThinking.md` の再編**（5.1K → 3.6K）
  - セクション3「Taskfile自動化」を削除し、コーディング思想とテスト戦略に集中
  - 言語中立化: Python固有表現（Docstring）を「ドキュメントコメント」に統一

- **`OverviewBasicRule.md` の新規作成**（13K, 277行）
  - Human-AI協働開発の実践ワークフローを網羅的に記載
  - 第1章: Human-AI協働のためのフロー設計（考え方）
  - 第2章: go-task/Taskfile.yml（開発インターフェース統一）
  - 第3章: PLAN.md / WorkingLog.md（実装計画とタスク管理）
  - 第4章: QAヒアリング → TDG実行（具体的な実践手順）
  - 将来的な言語・フレームワーク拡張（Python CLI → Web Server, Go, TypeScript）も考慮

#### 参照更新
- **CLAUDE.md**: ガイドライン一覧に BasicRule.md を追加
- **README.ja.md**: 3箇所（ガイドライン一覧、 `cospec init` 説明、開発ガイドリンク）
- **README.md**: 1箇所（ `cospec init` の出力内容説明）
- **HISTORY_CONTEXT.md**: ドキュメント一覧に BasicRule.md を追記

### 判断・選択

#### なぜ「.rules/」をプロジェクトルートに配置したか
当初は `docs/.rules/` も検討したが、**「ドキュメントと思想・ルールの分離」** を明確にするために、プロジェクトルート直下に配置した。これにより:
- AIエージェントが設計思想を理解したい → `.rules/` を見る
- 開発履歴やレビューレポートを確認したい → `docs/` 配下を見る
と役割が明確になり、参照が高速化される。

#### なぜ BasicRule.md に実践手順を集約したか
従来の Overview*ファイルでは、「TDGの思想（なぜ）」と「TDGのやり方（How）」が同じセクションに記載されていた。`OverviewBasicRule.md` という実践ガイドを独立させることで:
- **設計思想**: OverviewDesign/CodingTesting *Thinking.md で **なぜ** を理解
- **実践手順**: OverviewBasicRule.md で **どうやるか** を把握
という関心の分離を実現し、開発者・AIエージェント双方の理解速度向上を図った。

#### 空ファイル削除について
3件の空レビューファイル（0バイトまたは397B）は、AIエージェントのエラーにより生成されたスタブと考えられたため、履歴としても価値が低いと判断し削除。レビュー内容が有効なファイルは `docs/report/` に維持。

### Gitコミット
- **コミット**: `refactor: reorganize documentation structure and split Overview files`
- **コメント**: 🤖 Generated with Claude Code
- **変更ファイル数**: 19ファイル
- **変更内訳**: 新規作成2ファイル, リネーム11ファイル, 削除3ファイル, 修正4ファイル
- **参照**: コミットハッシュ `e402636`

### 参照
- PLAN.md: 2026-01-05ドキュメント構造の整理・Overviewファイル分割
- OverviewBasicRule.md: 第3章「実装計画とタスク管理（PLAN.md / WorkingLog.md）」

---

## 2026-01-04 AI-Agent追加機能の実装

### ドキュメント更新
- `README.ja.md` の用語統一（AI → AI-Agent、AIコーディングエージェント → AI-Agent、Agentic Coding Tools → AI-Agent）
- `README.ja.md` に汎用性についての記述を追加（AI-Agent は qwen, opencode の利用をサンプルとしているが、この２つに限定せずプロンプトを与えてファイルを読めるAI-Agentであれば利用可能である）
- `AGENTS.md` に agent コマンドの説明を追加
- `PLAN.md` に実装計画を追加

### 設定管理の強化
- `CospecConfig` に `save_to_file()` メソッドを追加
- `load_config()` 関数に外部ファイルからの設定読み込み機能を追加（デフォルト: `.cospec/config.json`）
- 設定ファイルの永続化機能を実装

### AI-Agent管理コマンドの実装
- **`cospec agent add` コマンド**:
  - `--name` オプションで AI-Agent名を指定
  - `--command` オプションで実行コマンド名を指定
  - `--help` オプションでコマンドライン引数解析用のヘルプフラグを指定（デフォルト: `--help`）
  - 指定されたコマンドに `--help` を実行し、出力を解析して ToolConfig を自動生成
  - 設定を `.cospec/config.json` に永続化

- **`cospec agent list` コマンド**:
  - 登録済み AI-Agent の一覧表示
  - 各エージェントの設定（コマンド、引数）を表示

- **`cospec agent test` コマンド**:
  - 指定 AI-Agent の実行確認
  - テストプロンプトを使用して正常動作を検証
  - エラーハンドリングと診断メッセージを表示

### テストの実装
- `tests/test_agent.py` を作成
- モックを使用したコマンド実行テスト
- 設定ファイルの読み書きテスト
- 全24件のテストが合格（既存20件 + 新規4件）

### 品質保証
- ruff linting: すべてのチェックをパス
- mypy type checking: 型注釈を修正完了
- pytest: 24 passed

### AI-Agentの追加と整理
- **AI-Agentの追加（Crush, MistralVibe, Gemini-CLI）**:
  - `Crush`: `crush run {prompt}` 形式で追加
  - `MistralVibe`: `vibe -p {prompt}` 形式で追加
  - `Gemini-CLI`: `gemini {prompt}` 形式で追加
  - ダミーAI-Agent（`mycli`）を削除

- **設定ファイルの整理**:
  - `opencode` → `Opencode` に名称変更
  - `--print-logs` オプションを削除し、不要なログ出力を抑制
  - 引数を修正（`--file` オプションを削除し、`run {prompt}`形式に統一）

### opencode 問題の調査と解決
- **問題の根本原因特定**:
  - opencode CLIはセッション管理型エージェントであり、stdoutには回答を出力しない
  - subprocess経由ではファイルに生成された結果をキャプチャできない
  - 対話型環境では動作可能だが、非対話型のCLI連携には不向き

- **実機テスト**:
  - 直接コマンドでの動作確認（`echo "明日の横浜の天気" | opencode run`）
  - 設定修正後の動作確認で正常応答を確認
  - opencodeが実際に天気情報を取得し、応答として表示することを確認

- **結論**:
  - opencode CLIはセッション管理型エージェントであるため、外部ツールからのsubprocess呼び出しには不向きであることが判明
  - 直接コマンド実行では正常に動作し、天気情報を取得して応答として表示することが確認された

### AI-Agentの結果返し方調査結果

現在登録されているすべてのAI-Agentの動作特性を調査し、結果の返し方を整理:

- **Qwen**: stdout（標準出力）に直接応答を出力 ✅
- **Crush**: runサブコマンドで非対話モードとなり、stdoutに応答を出力 ✅
- **Opencode**: runサブコマンドでstdoutに応答を出力（セッション管理型だがCLI連携可能）✅
- **MistralVibe**: -pオプションでプログラムモードとなり、stdoutに応答を出力 ✅
- **Gemini-CLI**: 位置引数でプロンプトを受け取り、stdoutに応答を出力 ✅

**まとめ**:
- すべてのAI-Agentはstdoutに応答を出力する方式
- BaseAgent.run_tool()と完全互換
- 以前のopencode問題は、存在しない`--file`オプションを使おうとしたのが原因
- CLI連携自体は問題なく可能であることを確認

### ネーミングルールの統一

AI-Agentの名称を大文字スタート（PascalCase/CamelCase）に統一:
- `qwen` → `Qwen`
- `mycli` → 削除（ダミーAI-Agent）
- `opencode` → `Opencode`（既に変更済み）
- `Crush` → `Crush`（既に対応済み）
- `MistralVibe` → `MistralVibe`（既に対応済み）
- `Gemini-CLI` → `Gemini-CLI`（既に対応済み）
## 2026-01-04

### 設定管理の拡張
- `CospecConfig` に `dev_tool` フィールド追加
- 環境変数 `COSPEC_DEV_TOOL` の読み込み対応
- `select_tool_for_development()` メソッド追加：開発用ツール選択
- `select_tool_for_review()` メソッド追加：レビュー用ツール選択

### ツール選択ロジックの実装
- **hear/test-gen 用**:
  - `COSPEC_DEV_TOOL` が設定されていればそれを使用
  - 未設定なら `default_tool` を使用
- **review 用**:
  - 利用ツール以外からランダムに2つを選択
  - 最低2つのツールが登録されているか確認
  - ツールが足りない場合はデフォルトを使用
  - 2つのツールで順次レビューを実行
  - レビューサマリーを表示

### CLI コマンドの更新
- `hear` コマンドで自動選択ロジックを適用
- `test-gen` コマンドで自動選択ロジックを適用
- `review` コマンドで複数ツールレビューを実装

### テストと品質保証
- 環境変数の動作確認（`export COSPEC_DEV_TOOL=opencode`）
- ツール選択ロジックのテスト
- ruff linting: すべてのチェックをパス
- mypy type checking: 型注釈を修正完了

### ドキュメント更新
- `README.ja.md` にツール選択ロジックの説明を追加
- 前提条件（2つ以上のAI-Agent）の明記
- `PLAN.md` に実装計画と実施内容を記録

## 2026-01-04

### GitHub へのプッシュ
- `gh` コマンドを使用して GitHub 上にパブリックリポジトリ `utenadev/cospec` を作成。
- 初回プッシュを完了し、リモート（origin/main）を設定。

### レビュー機能の強化: コンテキスト認識
- `Analyzer`: `docs/WorkingLog.md` と `docs/PLAN.md` をレビューのコンテキストに含めるように変更。
- `ReviewerAgent`: プロンプトを更新し、計画済みのタスク（PLAN.md記載）を考慮してレビューを行うよう指示。これにより「実装漏れ」と「計画的先送り」を区別可能に。

### ドキュメント整備
- `README.md`: 実装状況（外部ツール連携、`review`, `init` コマンド）に合わせて内容を刷新。
- `README.ja.md`: 日本語版READMEを作成。

### バグ修正
- `review` コマンド: 生成ファイル名のタイムスタンプ変数が正しく展開されない不具合を修正。
- 既存の不正ファイル (`docs/review_{date_str}_*.md`) を適切な名前にリネーム。

### 開発プロセスの改善: `PLAN.md` の導入
- `docs/PLAN.md` を作成: 実装タスクのチェックリスト管理を開始。今回のレビュー対応分を日本語で記録済み。
- `docs/OverviewDesignThinking.md` 更新: 実装前に `PLAN.md` を作成・更新するルールを追加。

### エージェントシステムの構造化と機能改善
- アーキテクチャ改善:
    - 外部ツール呼び出しロジックを `src/cospec/agents/` パッケージにカプセル化（`ReviewerAgent`）。
    - ドキュメント (`BLUEPRINT.md`) を現在の `src` レイアウトに合わせて修正。
- 機能拡張:
    - `Config`: 言語設定 (`language`) を追加し、レビュー指示に反映（デフォルト: `ja`）。
    - `init` コマンド: `OverviewCodingTestingThinking.md` などのガイドラインファイル生成を追加。
- リファクタリング:
    - `main.py` を再構成し、`init` の内容拡充と `review` のエージェント利用への切り替えを実施。

### `cospec review` コマンドの実装
- 機能: ドキュメントとコードの不整合をレビューするコマンドを実装。
- アーキテクチャ:
    - `Analyzer`: `docs/*.md` と `src/**/*.py` からコンテキストを収集。
    - `External Tool Integration`: 自前でLLMクライアントを持たず、既存ツール（`qwen`, `opencode`）をサブプロセスとして呼び出す方式を採用。
    - `Config`: ツール名や実行コマンドを `Pydantic Settings` で管理。
- 実装詳細:
    - `src/cospec/core/analyzer.py`, `src/cospec/core/config.py` を作成。
    - `src/cospec/main.py` に `review` コマンドを追加。
    - レポートを `docs/review_YYYYMMDD_HHMMSS_{tool}.md` として保存。
- テスト: `tests/test_review.py` で `subprocess.run` をモックして正常系を検証。

### `cospec init` コマンドの実装
- `LICENSE` ファイル（MIT License）を作成。
- `docs/OverviewDesignThinking.md` に「作業ログの自動更新」に関する開発指針を追記。
    - AIエージェントがコミット時に自律的に `docs/WorkingLog.md` を更新することを規定。

### プロジェクト初期セットアップ
- `pyproject.toml` の作成と依存関係の定義:
    - 実行用: `typer`, `rich`, `pydantic-settings`, `openai`, `python-dotenv`
    - 開発用: `pytest`, `ruff`, `mypy`, `build`
- `.gitignore` の強化（Python標準パターンの追加）。
- Git リポジトリの初期化と初回コミットの実行 (`feat: initial project setup with cospec CLI skeleton`)。
- プロジェクト構造の骨組み（Scaffolding）を作成:
    - `src/cospec/main.py`: Typer を使用したエントリーポイント。
    - `src/cospec/__init__.py`: パッケージ初期化ファイル。
    - `tests/`: テストコード用ディレクトリ。
- `Taskfile.yml` の最適化:
    - `task setup`: 仮想環境の作成と開発モードでのインストール。
    - `task run`, `task test`, `task lint`, `task check` 等の自動化コマンドを定義。
- 環境の検証:
    - `task setup` が正常に終了することを確認。
    - 仮想環境内での `cospec --help` の動作を確認。
- `README.md` の作成（プロジェクト概要、セットアップ手順）。
- `GEMINI.md` の生成（AIエージェント向けのコンテキスト指示書）。
- `docs/WorkingLog.md` の作成（本ドキュメント）。

## 2026-01-04 Taskfile.yml 拡張と実装計画

### 実装計画の作成
- `docs/PLAN.md` を大幅に拡張し、5つのフェーズに分けて詳細な実装計画を作成。
- Phase 1: Taskfile.yml 強化と基本タスクの追加
- Phase 2: `cospec hear` コマンドの実装
- Phase 3: `cospec test-gen` コマンドの実装
- Phase 4: ドキュメントと品質保証の強化
- Phase 5: 将来の拡張計画（Webサービス化、マルチ言語対応）

### Taskfile.yml の機能拡張
- **新規コマンドタスクの追加**:
  - `task hear`: `cospec hear` コマンドの実行タスク
  - `task test-gen`: `cospec test-gen` コマンドの実行タスク
- **テストタスクの拡張**:
  - `task test:integration`: 統合テストの実行
  - `task test:e2e`: エンドツーエンドテストの実行
- **ドキュメント管理タスク**:
  - `task docs:check`: ドキュメントとコードの整合性チェック
  - `task docs:sync`: ドキュメントの自動同期
  - `task docs:validate`: ドキュメント整合性検証
- **品質保証タスク**:
  - `task quality:check`: 綜合的な品質チェック（lint + type-check + test + docs:check）
  - `task build:package`: パッケージビルドタスク

## 2026-01-04 `cospec test-gen` コマンド実装

### TestGeneratorAgent の作成
- **`src/cospec/agents/test_generator.py`** を新規作成:
  - `extract_test_scenarios_from_spec()`: SPEC.md からテストシナリオを抽出するロジックを実装
    - 機能要件の期待される挙動を抽出（functional タイプ）
    - ユーザー入力の条件を抽出（input_validation タイプ）
    - エラー処理のシナリオを抽出（error_handling タイプ）
    - 出力形式のシナリオを抽出（output_format タイプ）
    - 重複排除ロジックを実装
  - `extract_test_scenarios_from_plan()`: PLAN.md から統合テストシナリオを抽出
  - `generate_pytest_test_code()`: pytest 形式のテストコードを生成
    - フィーチャーごとにテストファイルを分類
    - キャメルケースのクラス名生成
    - メソッド名の重複回避ロジック
  - `generate_tests()`: テストケース生成のメインメソッド

### CLI コマンドの統合
- **`main.py` に `test_gen` コマンドを追加**:
  - `--tool` オプション: 使用する外部ツールを指定（qwen, opencode）
  - `--output` オプション: 出力先ディレクトリを指定（デフォルト: tests/generated/）
  - `--validate` オプション: 生成されたテストファイルの検証
  - ヘルプメッセージとエラーハンドリングを実装
  - テストシナリオと生成ファイルのサマリー表示

### テストの実装
- **`tests/test_test_gen.py`** を新規作成:
  - シナリオ抽出ロジックの単体テスト（SPEC.md, PLAN.md）
  - pytest テストコード生成のテスト
  - メソッド名生成ロジックのテスト
  - エラーハンドリングテスト（SPEC.md 不存在、出力先指定）
  - ファイル出力機能のテスト
  - 生成ファイルの検証ロジックのテスト

### 実装完了
- ✅ TestGeneratorAgent の作成完了
- ✅ CLI コマンドの統合完了
- ✅ テストの実装完了
- ✅ git commit と WorkingLog.md の更新完了

### 次のステップ
- Phase 4: ドキュメントと品質保証の強化に進む
- Taskfile.yml でのテスト自動化タスクの統合
- ドキュメント整合性チェックの強化

## 2026-01-04 `cospec hear` コマンド実装

### HearerAgent の作成
- **`src/cospec/agents/hearer.py`** を新規作成:
  - `extract_unclear_points()`: SPEC.md から不明点を抽出するロジックを実装
    - 条件分岐の不明点（"不明"、"未定"、"?" を含むもの）
    - ユーザー入力の不明点（"任意"、"オプション" などの判断基準）
    - エラー処理の不明点（"未定義"、"不明" を含むもの）
    - 出力形式の不明点（"?"、"不明" を含むもの）
  - `generate_interactive_questions()`: 抽出した不明点からインタラクティブな質問を生成
  - `hear_requirements()`: ヒアリングプロセス全体を実行し、AIに質問内容を提示

### CLI コマンドの統合
- **`main.py` に `hear` コマンドを追加**:
  - `--tool` オプション: 使用する外部ツールを指定（qwen, opencode）
  - `--output` オプション: ヒアリング結果の出力先を指定
  - ヘルプメッセージとエラーハンドリングを実装
  - AI からの回答を表示し、ユーザーにフィードバックを提供

### テストの実装
- **`tests/test_hear.py`** を新規作成:
  - 不明点抽出ロジックの単体テスト（条件、入力、エラー処理）
  - 質問生成ロジックのテスト
  - エラーハンドリングテスト（SPEC.md 不存在、外部ツールエラー）
  - モックを使用した外部ツール連携のテスト
  - 網羅的なテストケースでコードカバレッジを確保
## 2026-01-04 実装完了・品質保証・ドキュメント更新

### 実装完了の確認
- ✅ Phase 1: Taskfile.yml 拡張
- ✅ Phase 2: `cospec hear` コマンド
- ✅ Phase 3: `cospec test-gen` コマンド
- 全機能の実装が完了し、テストに合格

### 品質保証の実施
- **テスト実行**: 全20件のテストが合格
  - HearerAgent: 8件のテスト
  - TestGeneratorAgent: 10件のテスト
  - init: 2件のテスト
  - review: 1件のテスト
- **コード品質チェック**:
  - ruff linting: すべてのチェックをパス
  - ruff formatting: 8ファイルを自動フォーマット
  - mypy type checking: 型注釈を修正完了
  - コード品質基準を満たすことを確認

### バージョン管理
- git commit: feat: implement cospec hear and test-gen commands with comprehensive testing
- 4つのコミットで段階的に実装を完了
- ブランチ: main (origin/main より 4 commits 先)

### README.md の更新
- `hear` と `test-gen` を "Planned" から "Implemented" セクションに移動
- すべての主要機能が実装済みであることを反映

### ドキュメントファイル
- `CLAUDE.md`: Claude Code のためのガイドライン
- `docs/CLAUDE_DIARY.md`: 開発日誌（技術的決定と学び）
- `docs/WorkingLog.md`: 実装履歴
- `docs/PLAN.md`: 実装計画（5フェーズ詳細）

### 実装されたコア機能
1. **HearerAgent**: SPEC.md のあいまいさを解決
2. **TestGeneratorAgent**: テスト駆動開発を支援
3. **CLI 統合**: typer によるコマンドラインインターフェース
4. **テスト戦略**: 包括的な自動テスト
5. **ドキュメント文化**: Doc-as-Context 哲学の実践

### 次のステップ
- Phase 4: ドキュメントと品質保証の継続的な強化
- Phase 5: 将来の拡張（必要に応じて）
- ユーザーフィードバックに基づく機能改善
