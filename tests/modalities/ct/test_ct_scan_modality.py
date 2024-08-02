from phandose.modalities.ct import CTScanModality

from unittest.mock import MagicMock, patch
from pathlib import Path
import unittest


class TestCTScanModality(unittest.TestCase):

    def setUp(self):

        self.series_instance_uid = "1.2.840.10008.1.2.3.4"
        self.dir_dicom = Path("/path/to/dicom/directory")
        self.series_description = "CT Scan"
        self.ct_modality = CTScanModality(series_instance_uid=self.series_instance_uid,
                                          dir_dicom=self.dir_dicom,
                                          series_description=self.series_description)

    def test_initialization_with_series_description(self):

        self.assertEqual(self.ct_modality.series_instance_uid, self.series_instance_uid)
        self.assertEqual(self.ct_modality.dir_dicom, self.dir_dicom)
        self.assertEqual(self.ct_modality.series_description, self.series_description)
        self.assertEqual(self.ct_modality.modality, "CT")

    @patch("phandose.modalities.ct.CTScanModality.dicom")
    def test_initialization_without_series_description(self, mock_dicom):

        mock_dicom.return_value = iter([MagicMock(SeriesDescription='Test Series Description')])
        ct_modality = CTScanModality(series_instance_uid=self.series_instance_uid,
                                     dir_dicom=self.dir_dicom)

        self.assertEqual(ct_modality.series_instance_uid, self.series_instance_uid)
        self.assertEqual(ct_modality.dir_dicom, self.dir_dicom)
        self.assertEqual(ct_modality.series_description, 'Test Series Description')
        self.assertEqual(ct_modality.modality, "CT")


if __name__ == '__main__':
    unittest.main()
