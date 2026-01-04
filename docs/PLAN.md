# Implementation Plan

## 2026-01-04 Review Feedback Response
- [x] **Fix Directory Structure in Docs**
    - Update `docs/BLUEPRINT.md` to reflect `src/cospec` layout.
- [x] **Restructure Agent System**
    - Create `src/cospec/agents/` package.
    - Implement `BaseAgent` and `ReviewerAgent`.
    - Refactor `review` command to use the new agent class.
- [x] **Enhance `init` Command**
    - Include `OverviewCodingTestingThinking.md` and other guideline files in the generation list.
- [x] **Add Language Configuration**
    - Add `language` field to `CospecConfig` (default: `ja`).
    - Update `BaseAgent` to append language instructions to prompts.
