# GEMINI.md: Context & Instructions for `cospec`

This file provides context and guidelines for AI agents working on the `cospec` project.

## 1. Project Overview
**Name:** `cospec`
**Purpose:** A CLI platform designed to facilitate high-quality software development through collaboration between humans and AI agents.
**Core Concepts:**
*   **Codebase as Context:** Documentation serves as the ground truth for AI.
*   **Consistency First:** Eliminate discrepancies between docs and code before implementation.
*   **Decision Support:** AI provides options with Pros/Cons to support human decision-making.

## 2. Current Status (Inception Phase)
*   **Documentation:** Comprehensive specifications and architectural blueprints exist in `docs/`.
*   **Source Code:** **Not yet implemented.** The directory structure for the source code (e.g., `cospec/`, `src/`) is currently missing.
*   **Automation:** A `Taskfile.yml` exists but appears to be a template or legacy artifact referencing `llminfo_cli`. It needs to be updated to match the `cospec` project name and structure.

## 3. Architecture & Tech Stack (Planned)
Based on `docs/BLUEPRINT.md`:
*   **Language:** Python
*   **CLI Framework:** `Typer`
*   **UI Library:** `Rich`
*   **Configuration:** `Pydantic Settings`
*   **Task Runner:** `go-task`

## 4. Development Guidelines
Adhere strictly to `docs/OverviewCodingTestingThinking.md`:

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

**Note:** The current `Taskfile.yml` requires updates to point to the correct `cospec` module instead of `llminfo_cli`.

## 6. Project Structure
```
cospec/
├── docs/                  # Specifications & Thinking models (Ground Truth)
│   ├── SPEC.md            # Functional Requirements
│   ├── BLUEPRINT.md       # Architecture & Tech Stack
│   └── Overview*.md       # Coding & Design Guidelines
├── Taskfile.yml           # Task definitions (needs update)
├── GEMINI.md              # Agent Context (This file)
└── [Pending] cospec/      # Source code (to be created)
```
