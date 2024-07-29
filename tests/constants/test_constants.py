from phandose import constants

from pathlib import Path
import unittest


class TestConstants(unittest.TestCase):
    """"
    Unit tests for verifying the existence of the Phantom library directory, workspace directory, and logs directory.
    """

    def test_dir_phantom_library_exists(self):
        """
        Test if the Phantom library directory exists.
        """

        self.assertTrue(Path(constants.DIR_PHANTOM_LIBRARY).exists())

    def test_dir_workspace_exists(self):
        """
        Test if the workspace directory exists.
        """

        self.assertTrue(Path(constants.DIR_WORKSPACE).exists())

    def test_dir_logs_exists(self):
        """
        Test if the logs directory exists.
        """

        self.assertTrue(Path(constants.DIR_LOGS).exists())


if __name__ == "__main__":
    unittest.main()
