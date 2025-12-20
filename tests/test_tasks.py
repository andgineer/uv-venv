"""Unit tests for tasks.py"""
import pytest
from unittest.mock import Mock, patch, call
from invoke import Context
import sys
import os

# Add parent directory to path to import tasks
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tasks


class TestVerTaskFactory:
    """Tests for ver_task_factory function"""

    @pytest.mark.unit
    @patch.object(Context, 'run')
    def test_ver_task_factory_release(self, mock_run):
        """Test that release version task calls verup.sh with 'release'"""
        c = Context()
        task = tasks.ver_task_factory('release')
        task(c)

        mock_run.assert_called_once_with('./scripts/verup.sh release')

    @pytest.mark.unit
    @patch.object(Context, 'run')
    def test_ver_task_factory_feature(self, mock_run):
        """Test that feature version task calls verup.sh with 'feature'"""
        c = Context()
        task = tasks.ver_task_factory('feature')
        task(c)

        mock_run.assert_called_once_with('./scripts/verup.sh feature')

    @pytest.mark.unit
    @patch.object(Context, 'run')
    def test_ver_task_factory_bug(self, mock_run):
        """Test that bug version task calls verup.sh with 'bug'"""
        c = Context()
        task = tasks.ver_task_factory('bug')
        task(c)

        mock_run.assert_called_once_with('./scripts/verup.sh bug')


class TestUvTask:
    """Tests for uv task"""

    @pytest.mark.unit
    @patch.object(Context, 'run')
    def test_uv_task_calls_install_script(self, mock_run):
        """Test that uv task calls the uv install script"""
        c = Context()
        tasks.uv(c)

        mock_run.assert_called_once_with('curl -LsSf https://astral.sh/uv/install.sh | sh')


class TestNamespace:
    """Tests for task namespace configuration"""

    @pytest.mark.unit
    def test_all_version_types_registered(self):
        """Test that all version types are registered as tasks"""
        for version_type in tasks.ALLOWED_VERSION_TYPES:
            task_name = f'ver-{version_type}'
            assert task_name in tasks.namespace.task_names, \
                f"Task '{task_name}' should be registered in namespace"

    @pytest.mark.unit
    def test_uv_task_registered(self):
        """Test that uv task is registered"""
        assert 'uv' in tasks.namespace.task_names, \
            "Task 'uv' should be registered in namespace"

    @pytest.mark.unit
    def test_allowed_version_types_constant(self):
        """Test that ALLOWED_VERSION_TYPES contains expected values"""
        expected = ['release', 'bug', 'feature']
        assert tasks.ALLOWED_VERSION_TYPES == expected, \
            f"ALLOWED_VERSION_TYPES should be {expected}"
