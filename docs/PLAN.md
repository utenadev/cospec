# 実装計画 (Implementation Plan)

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
    