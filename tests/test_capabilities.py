import unittest
import sys
import os

# Ensure src is in path for testing
sys.path.insert(0, os.path.abspath("src"))

# Clean up any previous imports
if 'ndoc' in sys.modules:
    del sys.modules['ndoc']

from ndoc.core.capabilities import CapabilityManager
from unittest.mock import patch, MagicMock

class TestCapabilityManager(unittest.TestCase):
    
    def test_get_language_installed(self):
        # Python should be installed in the dev environment
        lang = CapabilityManager.get_language('python')
        self.assertIsNotNone(lang)

    def test_try_import_python(self):
        lang = CapabilityManager._try_import('python')
        self.assertIsNotNone(lang)

    def test_try_import_unknown(self):
        lang = CapabilityManager._try_import('non_existent_lang')
        self.assertIsNone(lang)

if __name__ == '__main__':
    unittest.main()
