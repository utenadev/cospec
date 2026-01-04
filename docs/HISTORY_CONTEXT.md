# HISTORY_CONTEXT: プロジェクト立ち上げの経緯

## 1. プロジェクトの起源
この `cospec` プロジェクトは、`llminfo-cli` の開発プロセスにおいて策定された「LLM協働開発ガイドライン」を実証・自動化するためのツールとしてスピンオフしました。

## 2. 達成された状態 (Current State)
- **ディレクトリ**: `../cospec` が作成済み。
- **ドキュメント**:
    - `docs/OverviewDesignThinking.md`: 設計思想（Codebase as Context）。
    - `docs/OverviewCodingTestingThinking.md`: 実装・テスト思想（TDG, Taskfile）。
    - `docs/SPEC.md`: 要件定義（FR-001 `init` ～ FR-006 `fix`）。
    - `docs/BLUEPRINT.md`: アーキテクチャ設計（Reviewer/Interviewer/Coderエージェント）。
- **タスクランナー**:
    - `Taskfile.yml`: `llminfo-cli` からコピーし、プロジェクト名を `cospec` に変更済み。
- **その他**:
    - `.gitignore`: 標準的なPython設定。

## 3. 未実施の項目 (Missing Items)
以下のファイルや設定はまだ存在しません。**次のセッションで最初に作成する必要があります。**

1.  **`pyproject.toml`**: パッケージ依存関係定義（Typer, Rich等）。
2.  **Gitリポジトリ**: `git init` が実行されていない。
3.  **ソースコードディレクトリ**: `cospec/` パッケージディレクトリが未作成。
4.  **仮想環境**: `venv` が未作成。

## 4. 次のアクションプラン (Next Steps)
1.  **環境構築**:
    - `git init`
    - `pyproject.toml` の作成
    - `task setup` の実行
2.  **スケルトン作成**:
    - `mkdir cospec`
    - `cospec/main.py` (Typer entry point) の作成
3.  **FR-001 (init) の実装**:
    - 自分自身の仕様（`docs/*.md`）をテンプレートとして出力する機能の実装。
