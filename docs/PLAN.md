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