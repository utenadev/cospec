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
- [ ] **HearerAgent の作成**
  - [ ] `src/cospec/agents/hearer.py` を作成
  - [ ] SPEC.md から不明点を抽出するロジックを実装
  - [ ] インタラクティブな質問生成機能を実装
- [ ] **CLI コマンドの統合**
  - [ ] `main.py` に `hear` コマンドを追加
  - [ ] 必要な引数とオプションを定義
  - [ ] ヘルプメッセージを追加
- [ ] **テストの実装**
  - [ ] `tests/test_hear.py` を作成
  - [ ] モックを使用した単体テストを実装
  - [ ] 統合テストを追加

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
    