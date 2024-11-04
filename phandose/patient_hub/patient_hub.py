from phandose.patient import Patient, create_patient_from_dicom_directory

from pathlib import Path


class PatientHub:

    def __init__(self, dir_patient_hub: Path):

        self._dir_patient_hub = dir_patient_hub
        self._dir_patient_hub.mkdir(parents=True, exist_ok=True)

    def store_patient_modalities(self, patient: Patient):

        dir_patient = self._dir_patient_hub / patient.patient_id
        dir_patient.mkdir(parents=True, exist_ok=True)

        for modality in patient.list_modalities:
            modality.store_dicom(dir_patient)

    def load_patient_modalities(self, patient_id: str) -> Patient:

        dir_patient = self._dir_patient_hub / patient_id
        patient = create_patient_from_dicom_directory(patient_id=patient_id, dir_dicom=dir_patient)

        return patient
