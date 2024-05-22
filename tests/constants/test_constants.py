from phandose import constants

import unittest


class TestConstants(unittest.TestCase):

    def test_test_dir_phantom_library_exists(self):
        self.assertTrue(constants.DIR_PHANTOM_LIBRARY.exists())


if __name__ == "__main__":
    unittest.main()
