"""Integration tests for the GitHub Action"""
import pytest
import yaml
from pathlib import Path


class TestActionConfiguration:
    """Tests for action.yml configuration"""

    @pytest.fixture
    def action_config(self):
        """Load action.yml configuration"""
        action_file = Path(__file__).parent.parent / "action.yml"
        with open(action_file) as f:
            return yaml.safe_load(f)

    @pytest.mark.integration
    def test_action_yml_exists(self):
        """Test that action.yml exists"""
        action_file = Path(__file__).parent.parent / "action.yml"
        assert action_file.exists(), "action.yml should exist"

    @pytest.mark.integration
    def test_action_has_required_fields(self, action_config):
        """Test that action.yml has required fields"""
        required_fields = ['name', 'description', 'runs']
        for field in required_fields:
            assert field in action_config, f"action.yml should have '{field}' field"

    @pytest.mark.integration
    def test_action_is_composite(self, action_config):
        """Test that action uses composite run type"""
        assert action_config['runs']['using'] == 'composite', \
            "Action should use composite run type"

    @pytest.mark.integration
    def test_action_has_steps(self, action_config):
        """Test that action has steps defined"""
        assert 'steps' in action_config['runs'], \
            "Action should have steps"
        assert len(action_config['runs']['steps']) > 0, \
            "Action should have at least one step"

    @pytest.mark.integration
    def test_action_has_windows_and_unix_steps(self, action_config):
        """Test that action has separate steps for Windows and Unix"""
        steps = action_config['runs']['steps']

        # Find platform-specific steps
        windows_steps = [s for s in steps if s.get('if') and 'Windows' in s['if']]
        unix_steps = [s for s in steps if s.get('if') and 'Windows' in s['if'] and '!=' in s['if']]

        assert len(windows_steps) > 0, "Action should have Windows-specific steps"
        assert len(unix_steps) > 0, "Action should have Unix-specific steps"

    @pytest.mark.integration
    def test_action_sets_virtual_env(self, action_config):
        """Test that action sets VIRTUAL_ENV environment variable"""
        steps = action_config['runs']['steps']

        for step in steps:
            run_content = step.get('run', '')
            if 'VIRTUAL_ENV' in run_content:
                # Found VIRTUAL_ENV setup
                assert 'GITHUB_ENV' in run_content, \
                    "Step should set VIRTUAL_ENV in GITHUB_ENV"
                return

        pytest.fail("Action should set VIRTUAL_ENV environment variable")

    @pytest.mark.integration
    def test_action_updates_path(self, action_config):
        """Test that action updates PATH with venv"""
        steps = action_config['runs']['steps']

        for step in steps:
            run_content = step.get('run', '')
            if 'GITHUB_PATH' in run_content:
                # Found PATH update
                assert '.venv' in run_content, \
                    "Step should add .venv to PATH"
                return

        pytest.fail("Action should update GITHUB_PATH")

    @pytest.mark.integration
    def test_action_installs_uv(self, action_config):
        """Test that action installs uv"""
        steps = action_config['runs']['steps']

        for step in steps:
            run_content = step.get('run', '')
            if 'astral.sh/uv/install' in run_content:
                # Found uv installation
                return

        pytest.fail("Action should install uv")

    @pytest.mark.integration
    def test_action_creates_venv(self, action_config):
        """Test that action creates virtual environment"""
        steps = action_config['runs']['steps']

        for step in steps:
            run_content = step.get('run', '')
            if 'uv venv' in run_content:
                # Found venv creation
                return

        pytest.fail("Action should create virtual environment with 'uv venv'")


class TestActionShellCommands:
    """Tests for action shell commands"""

    @pytest.fixture
    def action_config(self):
        """Load action.yml configuration"""
        action_file = Path(__file__).parent.parent / "action.yml"
        with open(action_file) as f:
            return yaml.safe_load(f)

    @pytest.mark.integration
    def test_windows_uses_powershell(self, action_config):
        """Test that Windows steps use PowerShell"""
        steps = action_config['runs']['steps']
        windows_steps = [s for s in steps if s.get('if') and 'Windows' in s['if'] and '!=' not in s['if']]

        for step in windows_steps:
            assert step.get('shell') == 'pwsh', \
                "Windows steps should use PowerShell (pwsh)"

    @pytest.mark.integration
    def test_unix_uses_bash(self, action_config):
        """Test that Unix steps use bash"""
        steps = action_config['runs']['steps']
        unix_steps = [s for s in steps if s.get('if') and 'Windows' in s['if'] and '!=' in s['if']]

        for step in unix_steps:
            assert step.get('shell') == 'bash', \
                "Unix steps should use bash"


class TestActionBranding:
    """Tests for action branding"""

    @pytest.fixture
    def action_config(self):
        """Load action.yml configuration"""
        action_file = Path(__file__).parent.parent / "action.yml"
        with open(action_file) as f:
            return yaml.safe_load(f)

    @pytest.mark.integration
    def test_action_has_branding(self, action_config):
        """Test that action has branding"""
        assert 'branding' in action_config, \
            "Action should have branding section"

    @pytest.mark.integration
    def test_action_branding_has_color(self, action_config):
        """Test that action branding has color"""
        if 'branding' in action_config:
            assert 'color' in action_config['branding'], \
                "Action branding should have color"


class TestWorkflowFiles:
    """Tests for workflow files"""

    @pytest.mark.integration
    def test_ci_workflow_exists(self):
        """Test that CI workflow exists"""
        ci_file = Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        assert ci_file.exists(), "CI workflow should exist"

    @pytest.mark.integration
    def test_publish_workflow_exists(self):
        """Test that publish workflow exists"""
        publish_file = Path(__file__).parent.parent / ".github" / "workflows" / "publish_release.yml"
        assert publish_file.exists(), "Publish workflow should exist"

    @pytest.mark.integration
    def test_workflows_are_valid_yaml(self):
        """Test that all workflow files are valid YAML"""
        workflows_dir = Path(__file__).parent.parent / ".github" / "workflows"
        if not workflows_dir.exists():
            pytest.skip("Workflows directory doesn't exist")

        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file) as f:
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError as e:
                    pytest.fail(f"{workflow_file.name} is not valid YAML: {e}")

    @pytest.mark.integration
    def test_publish_workflow_uses_github_ref_name(self):
        """Test that publish workflow uses github.ref_name for tag"""
        publish_file = Path(__file__).parent.parent / ".github" / "workflows" / "publish_release.yml"
        with open(publish_file) as f:
            content = f.read()

        # Should use github.ref_name instead of manually extracting version
        assert 'github.ref_name' in content, \
            "Publish workflow should use github.ref_name for tag reference"

        # Should not manually strip 'v' prefix from tags
        assert '${GITHUB_REF#refs/tags/v}' not in content, \
            "Publish workflow should not manually strip 'v' prefix from tags"
