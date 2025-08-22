# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GitHub Action that installs [uv](https://github.com/astral-sh/uv) and creates a virtual environment. It's designed to prevent Windows installation errors that occur when using uv without a virtual environment in GitHub Actions.

## Architecture

- `action.yml`: Main GitHub Action configuration with composite steps for both Windows (PowerShell) and Unix (Bash) environments
- `tasks.py`: Python invoke tasks for version management and uv installation
- `scripts/verup.sh`: Bash script for semantic version bumping with git tagging
- `version`: Version file updated by the versioning script

## Common Commands

### Version Management
- `invoke ver-release`: Bump major version (e.g., 1.0.0 → 2)
- `invoke ver-feature`: Bump minor version (e.g., 1.0.0 → 1.1)  
- `invoke ver-bug`: Bump patch version (e.g., 1.0.0 → 1.0.1)

### Development
- `invoke uv`: Install or upgrade uv locally

## Versioning System

The project uses a custom versioning scheme:
- Release versions: single digit (e.g., "3")
- Feature versions: major.minor (e.g., "3.1")
- Bug versions: major.minor.patch (e.g., "3.1.2")

Version bumping requires a clean git state and automatically creates git tags with commit messages summarizing changes since the last tag.

## Action Usage

Users reference this action in their workflows as:
```yaml
- name: Setup uv
  uses: andgineer/uv-venv@v3
```

The action handles platform differences automatically, installing uv and creating/activating a `.venv` virtual environment.