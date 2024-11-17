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

            added_modality = patient.list_modalities[0]
            self.assertEqual(added_modality.modality_id, "M12345")
            self.assertEqual(added_modality.modality_type, "CT")

    def test_from_dir_dicom(self):
        """ Test creating a patient from a directory of DICOM files. """

        patient_id = "AGORL_P2"
        dir_dicom = Path(__file__).parents[2] / "sample_data" / patient_id

        # Create the patient from the directory
        patient = Patient.from_dir_dicom(patient_id=patient_id, dir_dicom=dir_dicom)

        # Assertions
        self.assertEqual(patient.patient_id, patient_id)

        # Check the total number of modalities
        self.assertEqual(len(patient.list_modalities), 8)

        # Define the expected modalities for comparison
        expected_modalities = [
            {"modality_id": "1.2.752.243.1.1.20200515135827571.8400.38735",
             "modality_type": "RD",
             "series_description": "larynx"},

            {"modality_id": "1.2.752.243.1.1.20200515135827571.8500.67423",
             "modality_type": "RD",
             "series_description": "larynx"},

            {"modality_id": "1.2.752.243.1.1.20200515135827571.8600.52276",
             "modality_type": "RD",
             "series_description": "larynx"},

            {"modality_id": "1.2.752.243.1.1.20200515135827570.8000.55215",
             "modality_type": "RP",
             "series_description": "larynx"},

            {"modality_id": "1.2.752.243.1.1.20200515135550293.6300.36151",
             "modality_type": "RS",
             "series_description": "RS: Approved Structure Set"},

            {"modality_id": "1.2.840.113619.2.290.3.279712783.286.1586324222.579.4",
             "modality_type": "PET",
             "series_description": "CT ORL"},

            {"modality_id": "1.3.12.2.1107.5.1.4.49226.30000020042207402018700000674",
             "modality_type": "CT",
             "series_description": "RT_THORAX SS IV"},

            {"modality_id": "1.3.12.2.1107.5.1.4.49226.30000020042207402018700000976",
             "modality_type": "CT",
             "series_description": "RT_THORAX AC IV"},
        ]

        # Convert patient modalities to a dictionary keyed by modality_id for easier validation
        patient_modalities_dict = {
            modality.modality_id: modality for modality in patient.list_modalities
        }

        # Validate each expected modality
        for expected in expected_modalities:
            with self.subTest(modality_id=expected["modality_id"]):
                modality = patient_modalities_dict.get(expected["modality_id"])
                self.assertIsNotNone(modality, f"Modality ID {expected['modality_id']} not found in patient.")
                self.assertEqual(modality.modality_type, expected["modality_type"])
                self.assertEqual(modality.series_description, expected["series_description"])


if __name__ == "__main__":
    unittest.main()
