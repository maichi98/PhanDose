from phandose.modalities import StandAloneModality

from unittest.mock import patch, MagicMock
from pathlib import Path
import unittest


class TestStandAloneModality(unittest.TestCase):

    class DummyStandAloneModality(StandAloneModality):
        def __init__(self, **kwargs):
            super().__init__(modality_id="12345", modality_type="Dummy", **kwargs)

        def dataframe(self):
            return {"mock": "dataframe"}  # Mocked dataframe representation

    def setUp(self):
        self.modality = self.DummyStandAloneModality(
            path_dicom=Path("/mock/path/file.dcm"),
            series_description="Test Description",
            dir_dicom=Path("/mock/path"),
        )

    def test_initialization(self):
        """ Test initialization of StandAloneModality """
        self.assertEqual(self.modality.modality_id, "12345")
        self.assertEqual(self.modality.modality_type, "Dummy")
        self.assertEqual(self.modality.series_description, "Test Description")
        self.assertEqual(self.modality.dir_dicom, Path("/mock/path"))
        self.assertEqual(self.modality.path_dicom, Path("/mock/path/file.dcm"))

    def test_set_path_dicom(self):
        """ Test setting path_dicom """
        self.modality.path_dicom = Path("/new/mock/path/file.dcm")
        self.assertEqual(self.modality.path_dicom, Path("/new/mock/path/file.dcm"))

    @patch("pydicom.dcmread")
    def test_dicom_method(self, mock_dcmread):
        """ Test the dicom method to read a single DICOM file """
        mock_dcmread.return_value = MagicMock()
        dicom = self.modality.dicom()
        self.assertIsNotNone(dicom)
        mock_dcmread.assert_called_once_with(str(self.modality.path_dicom))

    def test_to_dict(self):
        """ Test the to_dict method """
        expected_dict = {
            "modality_id": "12345",
            "modality_type": "Dummy",
            "series_description": "Test Description",
            "path_dicom": "/mock/path/file.dcm",
        }
        self.assertEqual(self.modality.to_dict(), expected_dict)

    def test_string_representation(self):
        """ Test the __str__ and __repr__ methods """
        expected_str = "Modality: Dummy - UID: 12345"
        self.assertEqual(str(self.modality), expected_str)
        self.assertEqual(repr(self.modality), expected_str)