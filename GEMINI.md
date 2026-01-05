# GEMINI.md: Context & Instructions for `cospec`

This file provides context and guidelines for AI agents working on the `cospec` project.

**Must Read:** 本プロジェクトで開発を行う前に、以下のガイドを必ず読んでください。

### ✅ 必須ガイド
開発判断の**唯一の根拠**となるガイドライン：
1. **`.rules/OverviewDesignThinking.md`**: 設計思想（**なぜ**このルールがあるのか）
2. **`.rules/OverviewBasicRule.md`**: 実践ルール（**どうやって**開発するか）
3. **`.rules/OverviewCodingTestingThinking.md`**: コーディング思想（**どのような**コードを書くか）

**思想 → 実践の順で読む**: 必ず OverviewDesignThinking で「なぜ」を理解してから、OverviewBasicRule で「どうやって」を確認

---

## 1. Project Overview
**Name:** `cospec`
**Purpose:** A CLI platform designed to facilitate high-quality software development through collaboration between humans and AI agents.
**Core Concepts:**
*   **Codebase as Context:** Documentation serves as the ground truth for AI.
*   **Consistency First:** Eliminate discrepancies between docs and code before implementation.
*   **Decision Support:** AI provides options with Pros/Cons to support human decision-making.

## 2. Current Status (Implementation Phase)
*   **CLI Core:** Core commands (`init`, `status`, `review`, `hear`, `test-gen`, `agent`) are implemented using Typer and Rich.
*   **Documentation:** Specifications (`SPEC.md`) and architectural blueprints (`BLUEPRINT.md`) are the ground truth for development.
*   **Agents:** Initial implementation of `ReviewerAgent`, `HearerAgent`, and `TestGeneratorAgent` exists in `src/cospec/agents/`.
*   **Automation:** `Taskfile.yml` is fully functional for setup, testing, linting, and quality checks.

## 3. Architecture & Tech Stack
Based on `docs/BLUEPRINT.md`:
*   **Language:** Python
*   **CLI Framework:** `Typer`
*   **UI Library:** `Rich`
*   **Configuration:** `Pydantic Settings`
*   **Task Runner:** `go-task`

## 4. Development Guidelines
Adhere strictly to `.rules/OverviewCodingTestingThinking.md`:

### Coding Standards ("Guardrails for AI")
*   **Strong Typing:** Use `Pydantic` for data structures. Avoid `Any`.
*   **Self-Documenting:** Write Docstrings *before* implementation to guide generation.

### Testing Strategy ("Test-Driven Generation")
1.  **Scaffold:** Agree on test scenarios (in Japanese/English) with the user.
2.  **Test Generation:** Write failing tests (Red) first.
3.  **Implementation:** Write code to pass tests (Green).
4.  **Refactoring:** Clean up code while ensuring tests pass.
*   **Mocking:** Mock all external I/O (HTTP, DB) during tests. Use Dependency Injection.

## 5. Standard Commands (Taskfile)
The project uses `go-task` as the unified interface.
*   `task setup`: Initialize environment (venv, dependencies).
*   `task test`: Run tests (pytest).
*   `task lint`: Run linters (ruff, mypy).
*   `task check`: **Mandatory pre-commit check** (Lint + Type Check + Test).

## 6. Project Structure
```
cospec/
├── docs/                  # Specifications & Thinking models (Ground Truth)
│   ├── SPEC.md            # Functional Requirements
│   ├── BLUEPRINT.md       # Architecture & Tech Stack
│   └── PLAN.md            # Current implementation plan
├── .rules/                # Project rules and guidelines
├── src/                   # Source code
│   └── cospec/
│       ├── agents/        # Agent logic
│       ├── core/          # Core utilities (config, analyzer)
│       └── main.py        # CLI entry point
├── tests/                 # Unit and integration tests
├── Taskfile.yml           # Task definitions
└── GEMINI.md              # Agent Context (This file)
```

## 7. Language Policy
- **User communication**: Japanese
- **Code comments**: English
- **Commit messages**: English
- **Documentation**: docs/以下の *.md は、既に日本語のものは継続して日本語で記述する
```
