# OpenCode Diary: cospec 開発記録

## 2026-01-04 レビュープロンプトサイズ問題の解決

### BaseAgent.run_tool() の最適化
- **問題**: レビュー時のプロンプトが 100,472文字（約100KB）あり、システムの引数長制限を超えてエラーになる
- **原因**: `ProjectAnalyzer.collect_context()` が以下のすべてを全文読み込んでいる
  - `docs/*.md`: すべてのマークダウンファイル
  - `src/cospec/**/*.py`: すべてのPythonファイル
- **影響**: `qwen`, `opencode` などのCLIツールに直接引数でプロンプトを渡せない

### 解決策の実装
- **ファイルベースアプローチ**: 長いプロンプト（8000文字超）を一時ファイルに保存して渡す
- **`--file` プレースホルダー対応**: opencode 用に `--file /tmp/xxx.txt "このファイルをプロンプトとして評価して"` 形式をサポート
- **`{prompt}` プレースホルダー対応**: qwen 用に `@/tmp/xxx.txt` 形式をサポート
- **一時ファイルの適切なクリーンアップ**: finally ブロックでファイル削除

### テストと品質保証
- ruff linting: すべてのチェックをパス
- mypy type checking: 型注釈を修正完了
- pytest: 24 passed

## 2026-01-04 AI-Agent選択ロジックの実装

### ツール選択ロジックの実装
- **hear/test-gen 用ロジック**:
  - `COSPEC_DEV_TOOL` 環境変数の読み込み対応（`env_file=".env"`）
  - `select_tool_for_development()`: 開発用ツールを優先
- **review 用ロジック**:
  - `select_tool_for_review()`: 開発ツール以外からランダムに2つを選択
  - 複数ツールレビューの実装

### CLI コマンドの更新
- `hear`, `test-gen`: 自動選択ロジックを適用
- `review`: 2ツールで順次レビュー実行、サマリー表示

### 実装内容の記録
- 環境変数の動作確認（`export COSPEC_DEV_TOOL=opencode`）
- ツール選択ロジックのドキュメント化
- PLAN.md に実装計画と実施内容を記録
- WorkingLog.md に実施内容と品質保証を記録

## 2026-01-04 設定管理の強化

### 設定ファイルの永続化
- `CospecConfig.save_to_file()` メソッドの追加
- `.cospec/config.json` への自動保存
- 既存設定とのマージ処理

### AI-Agent管理コマンドの実装
- `cospec agent add`: コマンドの `--help` 実行と解析、設定の自動生成と保存
- `cospec agent list`: 登録済み AI-Agent の一覧表示
- `cospec agent test`: AI-Agent の動作確認

### テストの実装
- `tests/test_agent.py` の作成
- モックを使用したコマンド実行テスト
- ヘルプ出力解析ロジックのテスト
- 設定ファイルの読み書きテスト

### ドキュメントの更新
- README.ja.md: AI-Agent 管理セクションの追加
- PLAN.md: 実装計画と実施内容の記録
- AGENTS.md: agent コマンドの説明を追加
- WorkingLog.md: 実施内容の記録

### 品質保証
- ruff: All checks passed
- mypy: Success: no issues found
- pytest: 24 passed
