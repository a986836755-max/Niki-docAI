import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure we import from src
sys.path.insert(0, os.path.abspath("src"))

from pathlib import Path
from ndoc.flows import capability_flow
from ndoc.models.config import ProjectConfig, ScanConfig

class TestCapabilityFlow(unittest.TestCase):
    def setUp(self):
        self.config = ProjectConfig(scan=ScanConfig(root_path=Path("/tmp/test")))

    @patch('ndoc.flows.capability_flow.fs.walk_files')
    @patch('ndoc.flows.capability_flow.capabilities.CapabilityManager.ensure_languages')
    def test_run_detects_languages(self, mock_ensure, mock_walk):
        # Setup mock files
        mock_walk.return_value = [
            Path("test.py"),
            Path("test.js"),
            Path("test.unknown")
        ]
        
        # Run flow
        capability_flow.run(self.config, auto_install=False)
        
        # Verify ensure_languages called with correct languages
        # python -> python, js -> javascript
        expected_langs = {'python', 'javascript'}
        mock_ensure.assert_called_once()
        call_args = mock_ensure.call_args
        self.assertEqual(call_args[0][0], expected_langs)
        self.assertEqual(call_args[1]['auto_install'], False)

    @patch('ndoc.flows.capability_flow.capabilities.CapabilityManager.ensure_languages')
    def test_check_single_file(self, mock_ensure):
        # Test .py file
        capability_flow.check_single_file(Path("test.py"), auto_install=True)
        mock_ensure.assert_called_with({'python'}, auto_install=True)

    @patch('ndoc.flows.capability_flow.capabilities.CapabilityManager.ensure_languages')
    def test_check_single_file_unknown(self, mock_ensure):
        # Test unknown extension
        capability_flow.check_single_file(Path("test.unknown"), auto_install=True)
        mock_ensure.assert_not_called()

if __name__ == '__main__':
    unittest.main()
