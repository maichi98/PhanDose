from phandose.patient import Patient

from pathlib import Path


class PatientManager:

    def __init__(self, dir_patient_hub: Path):

        self._dir_patient_hub = dir_patient_hub
        self._dir_patient_hub.mkdir(parents=True, exist_ok=True)

    def save_patient(self, patient: Patient) -> None:
        path_patient = self._dir_patient_hub / patient.patient_id
        path_patient.mkdir(parents=True, exist_ok=True)

    def load_patient(self, patient_id: str) -> Patient:
        path_patient = self._dir_patient_hub / patient_id
        return Patient(patient_id)

