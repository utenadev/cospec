# cospec Development Commands

## Essential Commands

### Project Setup
```bash
task setup              # Setup virtual environment and dependencies
source venv/bin/activate # Activate virtual environment (Linux/macOS)
venv\Scripts\activate   # Activate virtual environment (Windows)
```

### Quality Assurance (MUST PASS before committing)
```bash
task check              # Run all checks (lint + type-check + test)
task test               # Run tests
task lint               # Run linters (ruff check and format)
task lint-fix           # Run linters and fix issues automatically
task type-check         # Run type checking (mypy)
```

### Project Operations
```bash
cospec init             # Initialize a new project
cospec review           # Review codebase consistency
cospec hear             # Interactive requirement clarification
cospec test-gen         # Generate tests from specifications
cospec status           # Check project status
```

### Testing
```bash
pytest                  # Run all tests
pytest -xvs             # Stop on first failure with verbose output
pytest tests/test_file.py -xvs  # Run specific test file
```

### Development Workflow
```bash
# 1. Setup environment
task setup
source venv/bin/activate

# 2. Make changes to code

# 3. Validate changes (MUST PASS)
task check

# 4. Generate tests if needed
cospec test-gen

# 5. Review consistency
cospec review

# 6. Commit changes
git add .
git commit -m "Your message"
git push
```

### Clean Up
```bash
task clean              # Clean temporary files and caches
```

## Environment Variables
- `COSPEC_LANGUAGE=ja` - Language for AI responses (ja/en)
- `COSPEC_DEFAULT_TOOL=qwen` - Default tool for reviews