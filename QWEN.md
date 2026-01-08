# QWEN.md: Context & Instructions for `cospec` Qwen Agent

This file provides context and guidelines for Qwen AI agents working on the `cospec` project.

**Must Read:** 本プロジェクトで開発を行う前に、以下のガイドを必ず読んでください。

### ✅ 必須ガイド
開発判断の**唯一の根拠**となるガイドライン：
1. **`.rules/GuidlineDesign.md`**: 設計思想（**なぜ**このルールがあるのか）
2. **`.rules/GuidlineBasicRule.md`**: 実践ルール（**どうやって**開発するか）
3. **`.rules/GuidlineCodingTesting.md`**: コーディング思想（**どのような**コードを書くか）

**思想 → 実践の順で読む**: 必ず GuidlineDesign で「なぜ」を理解してから、GuidlineBasicRule で「どうやって」を確認

---

## 1. Project Overview

**Name:** `cospec`
**Purpose:** A CLI platform designed to facilitate high-quality software development through collaboration between humans and AI agents.

**Core Concepts:**
*   **Codebase as Context:** Documentation serves as the ground truth for AI.
*   **Consistency First:** Eliminate discrepancies between docs and code before implementation.
*   **Decision Support:** AI provides options with Pros/Cons to support human decision-making.

**Target Users:** Developers, AI agents, and teams using AI-Agent CLI tools for code reviews and specifications.

## 2. Prerequisites

*   **CLI tool installation:** Verify `qwen` command is available
    ```bash
    which qwen
    ```
*   **Credentials:** API credentials for Qwen models properly configured

## 3. Technical Architecture

*   **Language:** Python
*   **CLI Framework:** `Typer`
*   **UI Library:** `Rich`
*   **Configuration:** `Pydantic Settings`
*   **Task Runner:** `go-task`

## 4. Development Guidelines

Adhere strictly to the following:

1.  **Guidelines**
    *   Follow `.rules/GuidlineCodingTesting.md` for coding and testing standards
    *   Strong typing is mandatory: Avoid `Any` types, use `Pydantic` models
    *   Self-documenting code: Write docstrings **before** implementation
    *   Test-Driven Generation (TDG): Follow the scaffold → test → implement → refactor cycle
    *   Use `task check` before committing changes
    *   Mock external dependencies in tests

2.  **Workflow**
    *   Follow `.rules/GuidlineBasicRule.md` for development process
    *   PLAN.md: List tasks before implementation
    *   WorkingLog.md: Record work completion and decisions
    *   Before implementation, read SPEC.md/BLUEPRINT.md to understand requirements
    *   Use QA loops to clarify ambiguous requirements
    *   Follow Taskfile.yml interface standard: `setup`, `test`, `lint`, `check`

## 5. Command Usage

### For Code Reviews:

```bash
# Review codebase consistency against documentation
qwen api endpoint --model "qwen3-..." --input "以下のファイルを読んでレビューしてください：..."
```

### For Testing:

```bash
# Run automated checks
task check
# Run tests
task test
```

## 6. Integration Checklist

- [ ] Ensure `qwen` command is available in PATH
- [ ] API keys configured in environment or config file
- [ ] Test Qwen API connection before starting work
- [ ] Read `.rules/` 3 files before any development task
- [ ] Follow TDG workflow for implementation
- [ ] Pass `task check` before committing

## 7. Additional Resources

- [docs/SPEC.md](./docs/SPEC.md): Functional requirements
- [docs/BLUEPRINT.md](./docs/BLUEPRINT.md): Technical architecture
- [docs/PLAN.md](./docs/PLAN.md): Implementation plans
- [docs/WorkingLog.md](./docs/WorkingLog.md): Development history

## 8. Language Policy

- ユーザーとの会話：日本語
- ソースコードのコメントとドキュメント：英語
- コミットメッセージ：英語（コードベースとの一貫性維持のため）
- ドキュメント（docs/以下の*.md）：既に日本語のものは引き続き日本語で記述

---