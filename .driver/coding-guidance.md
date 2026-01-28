# TaskTracker Coding Guidelines

## CLI Design Principles

### 1. Command Structure
- All CLI commands must have a `--help` option with clear descriptions
- Use consistent verb-noun naming: `add-task`, `list-tasks`, `complete-task`
- Return exit code 0 for success, non-zero for errors
- Print user-facing messages to stdout, errors to stderr

### 2. Error Handling
- Never use bare `except:` clauses - always catch specific exceptions
- CLI commands should catch exceptions and convert to user-friendly error messages
- Use `sys.exit(1)` for errors, never silent failures
- Log exceptions with full tracebacks for debugging

### 3. Data Validation
- Validate all user input at the CLI boundary
- Use Pydantic models for data validation when possible
- Reject invalid input early with clear error messages
- Never trust user input - sanitize before storage

### 4. Storage Patterns
- Use JSON for simple persistence, SQLite for complex queries
- Always handle missing/corrupted data files gracefully
- Implement atomic writes to prevent data corruption
- Include version numbers in data formats for migration support

### 5. Testing Requirements
- Every CLI command must have at least one test
- Test both success and error paths
- Use pytest fixtures for test data
- Mock file I/O in unit tests, use temp directories in integration tests

### 6. Code Style
- Functions should be under 20 lines
- Use type hints for all function signatures
- Prefer `pathlib.Path` over string paths
- Use f-strings for string formatting
- Constants should be UPPER_SNAKE_CASE at module level

### 7. Documentation
- Public functions need docstrings with Args and Returns sections
- Include usage examples in CLI help text
- Keep README updated with installation and usage instructions
