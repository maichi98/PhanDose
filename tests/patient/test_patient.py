from phandose.modalities import Modality
from phandose.patient import Patient

from unittest.mock import patch, MagicMock
from pathlib import Path
import unittest


class TestPatient(unittest.TestCase):

    def setUp(self):
        self.patient = Patient(patient_id="P12345")

    def test_initialization(self):
        """Test initialization with and without modalities."""
        self.assertEqual(self.patient.patient_id, "P12345")
        self.assertEqual(len(self.patient.list_modalities), 0)

        # Test initialization with modalities
        modality = MagicMock(spec=Modality)
        patient_with_modalities = Patient(patient_id="P67890", list_modalities=[modality])
        self.assertEqual(len(patient_with_modalities.list_modalities), 1)

    @patch("phandose.modalities.create_modality")
    def test_add_modality(self, mock_create_modality):
        """ Test adding a modality """

        # Configure the mock modality
        mock_modality = MagicMock(spec=Modality, modality_id="M12345", modality_type="CT")
        mock_create_modality.return_value = mock_modality

        # Add a new modality
        self.patient.add_modality(
            modality_id="M12345",
            modality_type="CT",
            dir_dicom=Path("/mock/path"),
        )

        # Check that the modality was added
        self.assertEqual(len(self.patient.list_modalities), 1)

        # Verify properties of the added modality
        added_modality = self.patient.list_modalities[0]
        self.assertEqual(added_modality.modality_id, "M12345")
        self.assertEqual(added_modality.modality_type, "CT")

        # Test adding a duplicate modality
        self.patient.add_modality(
            modality_id="M12345",
            modality_type="CT",
            dir_dicom=Path("/mock/path"),
        )

        # Ensure the duplicate modality was not added
        self.assertEqual(len(self.patient.list_modalities), 1)

    def test_get_modality(self):
        """Test retrieving a modality."""
        modality = MagicMock(spec=Modality, modality_id="M12345")
        self.patient._list_modalities.append(modality)

        retrieved_modality = self.patient.get_modality("M12345")
        self.assertEqual(retrieved_modality, modality)

        self.assertIsNone(self.patient.get_modality("NonExistent"))

    def test_to_dict(self):
        """Test serializing a patient to a dictionary."""
        modality = MagicMock(spec=Modality, modality_id="M12345")
        modality.to_dict.return_value = {"mock": "modality"}
        self.patient._list_modalities.append(modality)

        patient_dict = self.patient.to_dict()
        self.assertEqual(patient_dict["patient_id"], "P12345")
        self.assertEqual(len(patient_dict["modalities"]), 1)
        self.assertEqual(patient_dict["modalities"][0], {"mock": "modality"})

    def test_from_dict(self):
        """Test creating a patient from a dictionary."""
        dict_patient = {
            "patient_id": "P12345",
            "modalities": [
                {"modality_id": "M12345", "modality_type": "CT", "dir_dicom": "/mock/path"}
            ],
        }

        with patch("phandose.modalities.create_modality") as mock_create_modality:
            mock_modality = MagicMock(spec=Modality)
            mock_create_modality.return_value = mock_modality

            patient = Patient.from_dict(dict_patient)
            self.assertEqual(patient.patient_id, "P12345")
            self.assertEqual(len(patient.list_modalities), 1)
            self.assertEqual(patient.list_modalities[0], mock_modality)

    @patch("phandose.patient.dcm.read_file")
    @patch("phandose.utils.get_modality_from_dicom_slice")
    def test_from_dir_dicom(self, mock_get_modality, mock_dcmread):
        """Test creating a patient from a DICOM directory."""
        mock_dcm_slice = MagicMock()
        mock_dcm_slice.SeriesInstanceUID = "Series12345"
        mock_dcm_slice.SOPInstanceUID = "SOP12345"
        mock_dcm_slice.SeriesDescription = "Test Series"

        mock_dcmread.return_value = mock_dcm_slice
        mock_get_modality.side_effect = ["CT", "RP"]

        with patch("pathlib.Path.rglob") as mock_rglob:
            mock_rglob.return_value = [Path("/mock/path/file1.dcm"), Path("/mock/path/file2.dcm")]

            patient = Patient.from_dir_dicom(patient_id="P12345", dir_dicom=Path("/mock/path"))
            self.assertEqual(patient.patient_id, "P12345")
            self.assertEqual(len(patient.list_modalities), 2)
            self.assertEqual(patient.list_modalities[0].modality_id, "Series12345")
            self.assertEqual(patient.list_modalities[1].modality_id, "SOP12345")


if __name__ == "__main__":
    unittest.main()
