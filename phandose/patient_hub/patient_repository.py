from phandose.modalities import Modality
from phandose.patient import Patient

from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
from datetime import datetime


class PatientRepository:

    def __init__(self, db_url: str, db_name: str):

        self._client = MongoClient(db_url)
        self._db = self._client[db_name]
        self.patients = self._db["patients"]

    def add_patient(self, patient: Patient):

        patient_dict = patient.to_dict()
        now = datetime.utcnow()
        patient_dict["created_at"] = now
        patient_dict["updated_at"] = now

        try:
            self.patients.insert_one(patient_dict)

        except DuplicateKeyError:
            raise ValueError(f"Patient {patient.patient_id} already exists in the repository !")

        print(f"Patient {patient.patient_id} added to the repository")

    def get_patient(self, patient_id: str) -> Patient:
        pass

    def delete_patient(self, patient_id: str):
        pass


