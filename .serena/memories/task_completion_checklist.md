# cospec Development Workflow

## Complete Task Checklist

### 1. Project Setup (One-time)
```bash
task setup              # Setup virtual environment and dependencies
source venv/bin/activate # Activate virtual environment
```

### 2. Task Implementation

#### Before Starting
- **Read `.rules/OverviewDesignThinking.md`** - Understand design philosophy
- **Read `.rules/OverviewBasicRule.md`** - Follow development workflow
- **Read `.rules/OverviewCodingTestingThinking.md`** - Code quality standards
- **Match requirements** against SPEC.md/BLUEPRINT.md
- **List tasks** in PLAN.md and confirm

#### During Implementation
- **Follow TDG approach** - Write tests before implementation when possible
- **Use strong typing** - Avoid Any types, prefer specific annotations
- **Write docstrings** - Document all functions and classes
- **Mock external dependencies** - Use pytest-mock for testing

#### After Implementation

##### Quality Assurance (CRITICAL - MUST PASS)
```bash
task check              # Run all checks - MUST PASS before committing
```

**What `task check` validates:**
- **Linting**: ruff check and format (code style)
- **Type checking**: mypy (type safety)
- **Testing**: pytest (functionality)

##### If `task check` fails:
1. **Fix linting issues** with `task lint-fix`
2. **Resolve type errors** in mypy output
3. **Fix failing tests** and ensure all pass
4. **Re-run `task check`** until it passes

##### Test Generation (if applicable)
```bash
cospec test-gen         # Generate tests from specifications
```

##### Code Review
```bash
cospec review           # Check consistency with documentation
```

### 3. Commit Process
```bash
# 1. Validate changes
task check              # MUST PASS

# 2. Generate tests if needed
cospec test-gen

# 3. Review consistency
cospec review

# 4. Commit changes
git add .
git commit -m "Descriptive commit message in English"
git push
```

### 4. Documentation Update
- **Update WorkingLog.md** - Record what was implemented
- **Update PLAN.md** - Mark completed tasks
- **Update SPEC.md** - Add new features if applicable

## Key Principles

### Consistency First
- **Documentation is truth** - Code must match specs
- **Eliminate discrepancies** - Fix inconsistencies before implementation
- **Validate with `cospec review`** - Use AI to catch issues

### Quality Standards
- **`task check` is mandatory** - Never commit without passing
- **Strong typing required** - Use specific types, avoid Any
- **Test coverage** - All public APIs must have tests
- **Code style** - Follow ruff and mypy configuration

### AI-Human Collaboration
- **AI provides options** - Present Pros/Cons for decisions
- **Human makes choices** - Final decisions remain with humans
- **Interactive clarification** - Use `cospec hear` for ambiguous requirements