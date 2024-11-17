from phandose.modalities import Modality

from unittest.mock import patch
from pathlib import Path
import pandas as pd
import unittest


class TestModality(unittest.TestCase):

    def test_abstract_class(self):
        """ Test that attempting to instantiate the abstract class raises a TypeError """
        with self.assertRaises(TypeError):
            Modality(modality_id="1234", modality_type="CT")

    class DummyModality(Modality):
        def set_series_description(self):
            self._series_description = "Dummy series description"

        def dicom(self):
            return "Dummy DICOM"

        def dataframe(self) -> pd.DataFrame:
            return pd.DataFrame()

        def to_dict(self) -> dict:
            return {
                "modality_id": self.modality_id,
                "modality_type": self.modality_type,
                "series_description": self.series_description,
                "dir_dicom": self.dir_dicom
            }

    def setUp(self):

        self.modality = self.DummyModality(
            modality_id="12345",
            modality_type="DummyType",
            series_description="Test Description",
            dir_dicom=Path("/valid/path")
        )

    def test_correct_initialization(self):
        """ Test that the modality is correctly initialized """
        self.assertEqual(self.modality.modality_id, "12345")
        self.assertEqual(self.modality.modality_type, "DummyType")
        self.assertEqual(self.modality.series_description, "Test Description")
        self.assertEqual(self.modality.dir_dicom, Path("/valid/path"))

    def test_series_description_lazy_initialization(self):
        """ Test that the series description is updated correctly """
        self.modality.set_series_description()
        self.assertEqual(self.modality.series_description, "Dummy series description")

    def test_valid_dir_dicom_setter(self):
        """ Test that the dir_dicom setter works correctly """

        with patch.object(Path, "exists", return_value=True):
            self.modality.dir_dicom = Path("/valid/path")
            self.assertEqual(self.modality.dir_dicom, Path("/valid/path"))

    def test_invalid_dir_dicom_setter(self):
        """ Test that the dir_dicom setter raises a FileNotFoundError when the directory doesn't exist """

        with self.assertRaises(FileNotFoundError):
            self.modality.dir_dicom = Path("/invalid/path")

    def test_dicom(self):
        """ Test that the dicom method returns the correct value """
        self.assertEqual(self.modality.dicom(), "Dummy DICOM")

    def test_dataframe(self):
        """ Test that the dataframe method returns a pandas DataFrame """
        self.assertIsInstance(self.modality.dataframe(), pd.DataFrame)

    def test_to_dict(self):
        """ Test that the to_dict method returns the correct dictionary """
        expected_dict = {
            "modality_id": "12345",
            "modality_type": "DummyType",
            "series_description": "Test Description",
            "dir_dicom": Path("/valid/path")
        }
        self.assertEqual(self.modality.to_dict(), expected_dict)

    def test_string_representation(self):
        """ Test the __str__ and __repr__ methods """
        expected_str = "Modality: DummyType - UID: 12345"
        self.assertEqual(str(self.modality), expected_str)
        self.assertEqual(repr(self.modality), expected_str)

    def test_missing_abstract_method_implementation(self):
        """ Test that subclass missing abstract methods cannot be instantiated """

        class IncompleteModality(Modality):
            def set_series_description(self):
                pass

        with self.assertRaises(TypeError):
            IncompleteModality(modality_id="67890", modality_type="Incomplete")


if __name__ == '__main__':
    unittest.main()
