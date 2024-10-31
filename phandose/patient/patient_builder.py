from phandose.modalities import create_modality
from phandose.patient import Patient

from pathlib import Path


class PatientBuilder:

    def __init__(self):
        """
        Initialize the PatientBuilder with empty attributes.

        """

        self._patient_id = None
        self._list_modalities = []

    def set_patient_id(self, patient_id: str):
        """
        Set the Patient ID for the Patient object to build.

        """

        self._patient_id = patient_id

    def add_modality(self, modality_id: str, modality_type: str, dir_dicom: Path = None, **kwargs):

        if modality_id not in [modality.modality_id for modality in self._list_modalities]:

            self._list_modalities.append(create_modality(modality_id=modality_id,
                                                         modality_type=modality_type,
                                                         dir_dicom=dir_dicom,
                                                         **kwargs))

    def build(self) -> Patient:
        """
        Build and return the Patient object.

        Parameters:
        -----------
        Patient
            The constructed Patient object.

        """

        patient = Patient(patient_id=self._patient_id, list_modalities=self._list_modalities)
        self._patient_id = None
        self._list_modalities = []
        return patient
