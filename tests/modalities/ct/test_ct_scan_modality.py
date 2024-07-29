from phandose.modalities import CTScanModality

from pathlib import Path
import unittest


class TestCTScanModality(unittest.TestCase):

    def setUp(self):

        self.series_instance_uid = "1.2.840.10008.1.2.3.4"
        self.dir_dicom = Path("/path/to/dicom/directory")
        self.series_description = "CT Scan"
        self.ct_modality = CTScanModality(self.series_instance_uid, self.dir_dicom, self.series_description)

    def test_initialization_with_series_description(self):

        self.assertEqual(self.ct_modality.series_instance_uid, self.series_instance_uid)
        self.assertEqual(self.ct_modality.dir_dicom, self.dir_dicom)
        self.assertEqual(self.ct_modality.series_description, self.series_description)
        self.assertEqual(self.ct_modality.modality, "CT")

    @patch('phandose.modalities.CTScanModality.dicom')
    def test_initialization_without_series_description(self, mock_dicom):

        mock_dicom.return_value =

