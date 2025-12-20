# Test Suite

Test suite for the uv-venv GitHub Action.

## Quick Start

```bash
# Run all tests (auto-setup venv and deps with uv)
invoke test
```

## Test Structure

```
tests/
├── test_tasks.py              # Unit tests for invoke tasks
├── test_verup.py              # Unit tests for versioning script
└── test_action_integration.py # Integration tests for the action
```

## Running Tests

All test commands automatically create `.venv` and install dependencies using `uv`:

```bash
invoke test              # All tests
invoke test-unit         # Unit tests only
invoke test-integration  # Integration tests only
invoke test-coverage     # With coverage report
invoke test-fast         # Exclude slow tests
```

## Test Categories

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow tests (git operations, etc.)

## Test Files

### test_tasks.py
Tests for `tasks.py` invoke tasks:
- Version task factory
- UV installation task
- Task registration

### test_verup.py
Tests for `scripts/verup.sh`:
- Version parsing
- Version bumping (release/feature/bug)
- Git integration

### test_action_integration.py
Tests for `action.yml`:
- YAML structure
- Platform-specific steps
- Environment setup
- UV and venv creation

## CI

Tests run automatically on push/PR:
- Unit tests: Python 3.8-3.12 on Ubuntu
- Action tests: Python 3.8-3.12 on Ubuntu/Windows/macOS
- Coverage uploaded for Python 3.11
