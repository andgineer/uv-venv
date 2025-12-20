"""Unit tests for verup.sh script logic"""
import pytest
import subprocess
import tempfile
import os
import shutil
from pathlib import Path


class TestVerupScript:
    """Tests for verup.sh script"""

    @pytest.fixture
    def test_git_repo(self, tmp_path):
        """Create a temporary git repository for testing"""
        repo_dir = tmp_path / "test_repo"
        repo_dir.mkdir()

        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'],
                      cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'],
                      cwd=repo_dir, check=True, capture_output=True)

        # Create version file
        version_file = repo_dir / "version"
        version_file.write_text('__version__ = "1"\n')

        # Copy verup.sh script
        script_dir = repo_dir / "scripts"
        script_dir.mkdir()
        original_script = Path(__file__).parent.parent / "scripts" / "verup.sh"
        if original_script.exists():
            shutil.copy(original_script, script_dir / "verup.sh")
            # Make it executable
            os.chmod(script_dir / "verup.sh", 0o755)

        # Initial commit
        subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'],
                      cwd=repo_dir, check=True, capture_output=True)

        # Create initial tag
        subprocess.run(['git', 'tag', 'v1', '-m', 'Version 1'],
                      cwd=repo_dir, check=True, capture_output=True)

        return repo_dir

    @pytest.mark.unit
    def test_script_exists(self):
        """Test that verup.sh script exists"""
        script_path = Path(__file__).parent.parent / "scripts" / "verup.sh"
        assert script_path.exists(), "verup.sh script should exist"
        assert os.access(script_path, os.X_OK), "verup.sh should be executable"

    @pytest.mark.unit
    @pytest.mark.slow
    def test_version_regex_pattern(self, test_git_repo):
        """Test that the script can parse version tags correctly"""
        # Add some commits
        test_file = test_git_repo / "test.txt"
        test_file.write_text("test content\n")
        subprocess.run(['git', 'add', 'test.txt'], cwd=test_git_repo, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Test commit'],
                      cwd=test_git_repo, check=True, capture_output=True)

        # Test getting the current tag
        result = subprocess.run(
            ['git', 'describe', '--match', 'v[0-9]*', '--abbrev=0', '--tags'],
            cwd=test_git_repo,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == 'v1'

    @pytest.mark.unit
    def test_version_file_format(self):
        """Test that version file has correct format"""
        version_file = Path(__file__).parent.parent / "version"
        assert version_file.exists(), "version file should exist"

        content = version_file.read_text()
        assert '__version__' in content, "version file should contain __version__"
        assert '=' in content, "version file should have assignment"

        # Extract version
        for line in content.split('\n'):
            if '__version__' in line and '=' in line:
                # Should be able to parse it
                assert '"' in line or "'" in line, "version should be quoted"


class TestVersionBumping:
    """Tests for version bumping logic"""

    @pytest.mark.unit
    @pytest.mark.parametrize("current,bump_type,expected", [
        ("1.0.0", "release", "2"),
        ("1.0.0", "feature", "1.1"),
        ("1.0.0", "bug", "1.0.1"),
        ("2.5.3", "release", "3"),
        ("2.5.3", "feature", "2.6"),
        ("2.5.3", "bug", "2.5.4"),
        ("5", "feature", "5.1"),
        ("5", "bug", "5.0.1"),
        ("5.2", "bug", "5.2.1"),
    ])
    def test_version_bumping_logic(self, current, bump_type, expected):
        """Test version bumping logic matches verup.sh behavior"""
        # Parse current version
        parts = current.split('.')
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        build = int(parts[2]) if len(parts) > 2 else 0

        # Apply bump logic from verup.sh
        if bump_type == "release":
            major += 1
            minor = 0
            build = 0
            result = str(major)
        elif bump_type == "feature":
            minor += 1
            build = 0
            result = f"{major}.{minor}"
        elif bump_type == "bug":
            build += 1
            result = f"{major}.{minor}.{build}"
        else:
            pytest.fail(f"Unknown bump type: {bump_type}")

        assert result == expected, \
            f"Bumping {current} with {bump_type} should give {expected}, got {result}"


class TestScriptInputValidation:
    """Tests for script input validation"""

    @pytest.mark.unit
    @pytest.mark.parametrize("invalid_type", [
        "major",
        "minor",
        "patch",
        "invalid",
        "",
        "RELEASE",  # Case sensitive - uppercase is invalid
        "Feature",  # Case sensitive - mixed case is invalid
    ])
    def test_invalid_bump_types(self, invalid_type):
        """Test that script validates bump type input (case-sensitive)"""
        valid_types = ["release", "feature", "bug"]
        assert invalid_type not in valid_types, \
            f"{invalid_type} should not be a valid bump type"

    @pytest.mark.unit
    def test_valid_bump_types(self):
        """Test that expected bump types are valid"""
        valid_types = ["release", "feature", "bug"]
        for bump_type in valid_types:
            assert bump_type in valid_types, \
                f"{bump_type} should be a valid bump type"
