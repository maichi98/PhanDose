from phandose.modalities import create_modality
from phandose.patient import Patient

from pathlib import Path


class PatientBuilder:
    """
    Builder class to construct a Patient object.

    """

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

    def add_modality(self, modality: str, series_instance_uid: str, dir_dicom: Path = None, **kwargs):
        """
        Add a modality to the Patient object to build.

        Parameters:
        -----------
        modality : (str)
            Modality of the DICOM files, (e.g. CT, RD, RP, RS, PET).

        series_instance_uid : (str)
            Series Instance UID of the DICOM files.

        dir_dicom : (Path), optional
            Directory containing the DICOM files.

        kwargs : (dict)
            Additional arguments for modality creation.

        """

        if series_instance_uid not in [mod.series_instance_uid for mod in self._list_modalities]:

            self._list_modalities.append(create_modality(modality=modality,
                                                         series_instance_uid=series_instance_uid,
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
