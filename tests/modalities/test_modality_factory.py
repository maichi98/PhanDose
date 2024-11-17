from phandose.modalities import (CTScanModality,
                                 PETScanModality,
                                 RtdoseModality,
                                 RtstructModality,
                                 RtplanModality)
from phandose.modalities import create_modality

from pathlib import Path
import unittest


class TestModalityFactory(unittest.TestCase):

    def test_create_ct_modality(self):
        """Test creating a CTScanModality."""
        modality = create_modality(
            modality_id="CT12345",
            modality_type="CT",
            dir_dicom=Path("/mock/path/ct"),
        )
        self.assertIsInstance(modality, CTScanModality)
        self.assertEqual(modality.modality_id, "CT12345")
        self.assertEqual(modality.modality_type, "CT")
        self.assertEqual(modality.dir_dicom, Path("/mock/path/ct"))

    def test_create_pet_modality(self):
        """Test creating a PETScanModality."""
        modality = create_modality(
            modality_id="PET12345",
            modality_type="PET",
            dir_dicom=Path("/mock/path/pet"),
        )
        self.assertIsInstance(modality, PETScanModality)
        self.assertEqual(modality.modality_id, "PET12345")
        self.assertEqual(modality.modality_type, "PET")
        self.assertEqual(modality.dir_dicom, Path("/mock/path/pet"))

    def test_create_rtdose_modality(self):
        """Test creating an RtdoseModality."""
        modality = create_modality(
            modality_id="RD12345",
            modality_type="RD",
            path_dicom=Path("/mock/path/rtdose.dcm"),
        )
        self.assertIsInstance(modality, RtdoseModality)
        self.assertEqual(modality.modality_id, "RD12345")
        self.assertEqual(modality.modality_type, "RD")
        self.assertEqual(modality.path_dicom, Path("/mock/path/rtdose.dcm"))

    def test_create_rtstruct_modality(self):
        """Test creating an RtstructModality."""
        modality = create_modality(
            modality_id="RS12345",
            modality_type="RS",
            path_dicom=Path("/mock/path/rtstruct.dcm"),
        )
        self.assertIsInstance(modality, RtstructModality)
        self.assertEqual(modality.modality_id, "RS12345")
        self.assertEqual(modality.modality_type, "RS")
        self.assertEqual(modality.path_dicom, Path("/mock/path/rtstruct.dcm"))

    def test_create_rtplan_modality(self):
        """Test creating an RtplanModality."""
        modality = create_modality(
            modality_id="RP12345",
            modality_type="RP",
            path_dicom=Path("/mock/path/rtplan.dcm"),
        )
        self.assertIsInstance(modality, RtplanModality)
        self.assertEqual(modality.modality_id, "RP12345")
        self.assertEqual(modality.modality_type, "RP")
        self.assertEqual(modality.path_dicom, Path("/mock/path/rtplan.dcm"))

    def test_invalid_modality_type(self):
        """Test that an invalid modality_type raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            create_modality(
                modality_id="Invalid12345",
                modality_type="INVALID",
                dir_dicom=Path("/mock/path/invalid"),
            )
        self.assertIn("Unsupported modality type 'INVALID'", str(context.exception))


if __name__ == "__main__":
    unittest.main()
