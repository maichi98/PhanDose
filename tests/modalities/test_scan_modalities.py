from phandose.modalities import ScanModality, CTScanModality

from unittest.mock import patch, MagicMock
from pathlib import Path
import unittest
import os


class TestScanModality(unittest.TestCase):

    class DummyScanModality(ScanModality):
        def __init__(self, **kwargs):
            super().__init__(modality_id="12345", modality_type="Dummy", **kwargs)

    def setUp(self):
        self.modality = self.DummyScanModality(
            dicom_paths=(Path(f"/mock/path/file_{i}.dcm") for i in range(3)),
            series_description="Test Description",
            dir_dicom=Path("/mock/path")
        )

    def test_initialization(self):
        """ Test initialization of ScanModality """
        self.assertEqual(self.modality.modality_id, "12345")
        self.assertEqual(self.modality.modality_type, "Dummy")
        self.assertEqual(self.modality.series_description, "Test Description")
        self.assertEqual(self.modality.dir_dicom, Path("/mock/path"))

    @patch("phandose.modalities.scan_modalities.dicom_utils.find_dicom_paths_of_scan")
    def test_lazy_dicom_paths(self, mock_find_paths):
        """ Test lazy loading of dicom_paths """
        mock_find_paths.return_value = (Path(f"/mock/path/file_{i}.dcm") for i in range(3))
        modality = self.DummyScanModality(dir_dicom=Path("/mock/path"))

        # Access dicom_paths
        paths = list(modality.dicom_paths)
        self.assertEqual(len(paths), 3)
        self.assertEqual(str(paths[0]), str(Path("/mock/path/file_0.dcm")))
        mock_find_paths.assert_called_once()

    @patch("pydicom.dcmread")
    def test_dicom_method(self, mock_dcmread):
        """ Test the dicom method to read DICOM files """
        mock_dcmread.return_value = MagicMock()
        dicoms = list(self.modality.dicom())
        self.assertEqual(len(dicoms), 3)
        mock_dcmread.assert_called()

    @patch("phandose.modalities.scan_modalities.conversions.convert_scan_to_dataframe")
    def test_dataframe_method(self, mock_convert_to_df):
        """ Test the dataframe method """
        mock_convert_to_df.return_value = MagicMock()
        df = self.modality.dataframe()
        self.assertIsNotNone(df)
        mock_convert_to_df.assert_called_once()

    def test_to_dict(self):
        """ Test the to_dict method """
        expected_dict = {
            "modality_id": "12345",
            "modality_type": "Dummy",
            "series_description": "Test Description",
            "dicom_paths": [
                str(Path("/mock/path/file_0.dcm")),
                str(Path("/mock/path/file_1.dcm")),
                str(Path("/mock/path/file_2.dcm"))
            ]
        }

        # Normalize the dicom_paths from the modality for comparison
        actual_dict = self.modality.to_dict()
        actual_dict["dicom_paths"] = [str(Path(p)) for p in actual_dict["dicom_paths"]]

        self.assertEqual(actual_dict, expected_dict)


class TestCTScanModality(unittest.TestCase):

    def setUp(self):

        self.dir_patient = Path(__file__).parents[2] / "sample_data" / "AGORL_P6"

        self.series_instance_uid_1 = "1.3.12.2.1107.5.1.4.49226.30000020030308450423400000381"
        self.dir_dicom_paths_1 = self.dir_patient / "CT" / self.series_instance_uid_1

        self.series_instance_uid_2 = "1.3.12.2.1107.5.1.4.49226.30000020030308450423400000657"
        self.dir_dicom_paths_2 = self.dir_patient / "CT" / self.series_instance_uid_2

    def test_dir_patient_exists(self):
        self.assertTrue(self.dir_patient.exists(), "Patient directory does not exist !")

        for i, dir_dicom_paths in enumerate([self.dir_dicom_paths_2, self.dir_dicom_paths_2]):

            self.assertTrue(dir_dicom_paths.exists(), f"Scan modality {i + 1} DICOM directory does not exist!")
            self.assertTrue(any(dir_dicom_paths.iterdir()), f"Scan modality {i + 1} DICOM directory is empty !")

    def test_initialization(self):

        modality = CTScanModality(modality_id=self.series_instance_uid_1, dir_dicom=self.dir_patient / "CT")

        self.assertEqual(modality.modality_id, self.series_instance_uid_1)
        self.assertEqual(modality.modality_type, "CT")
        self.assertEqual(modality.series_description, "RT_ORL SS IV")
        self.assertEqual(len(list(modality.dicom())), len(os.listdir(self.dir_dicom_paths_1)))

    def test_dicom_reading(self):

        modality = CTScanModality(modality_id=self.series_instance_uid_1, dir_dicom=self.dir_patient / "CT")
        dicoms = list(modality.dicom())

        self.assertEqual(len(dicoms), len(os.listdir(self.dir_dicom_paths_1)))

        # Let's check that if you read a dicom slice, when you read it again, you get all slices
        _ = next(modality.dicom())

        dicoms = list(modality.dicom())
        self.assertEqual(len(dicoms), len(os.listdir(self.dir_dicom_paths_1)))

    def test_dataframe(self):
        """ Test that the dataframe method returns a valid DataFrame """

        modality = CTScanModality(modality_id=self.series_instance_uid_1, dir_dicom=self.dir_patient / "CT")
        df = modality.dataframe()

        self.assertIsNotNone(df, "DataFrame is None")
        self.assertFalse(df.empty, "DataFrame is empty")
        self.assertIn("x", df.columns, "Missing 'x' column in DataFrame")
        self.assertIn("y", df.columns, "Missing 'y' column in DataFrame")
        self.assertIn("z", df.columns, "Missing 'z' column in DataFrame")
        self.assertIn("intensity", df.columns, "Missing 'intensity' column in DataFrame")


if __name__ == "__main__":
    unittest.main()
