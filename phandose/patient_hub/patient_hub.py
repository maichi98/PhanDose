from .patient_repository import PatientRepository
from .storage_handler import StorageHandler

from phandose.patient import Patient


class PatientHub:

    def __init__(self, repository: PatientRepository, storage_handler: StorageHandler):

        self._repository = repository
        self._storage_handler = storage_handler

    def add_patient(self, patient: Patient):
        self._repository.add_patient(patient)
        print(f"Patient {patient.patient_id} added to the repository")

    def get_patient(self, patient_id: str):
        patient = self._repository.get_patient(patient_id)

        if not patient:
            raise ValueError(f"Patient {patient_id} not found in the repository")

        return patient
