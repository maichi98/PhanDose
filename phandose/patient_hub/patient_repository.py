from phandose.patient import Patient

from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from pymongo import MongoClient


class PatientRepository(ABC):

    def __init__(self, db_name: str = "phandose_db"):

        self.db_name = db_name
        self._client = self._connect()
        self._db = self._client[db_name]
        self.patients = self._db["patients"]

    @abstractmethod
    def _connect(self) -> MongoClient:
        pass

    def add_patient(self, patient: Patient):
        """
        Add a patient to the repository

        Parameters
        ----------
        patient: (Patient)
            The patient to add to the repository

        """

        patient_dict = patient.to_dict()
        now = datetime.now(timezone.utc)
        patient_dict["created_at"] = now
        patient_dict["updated_at"] = now

        try:
            self.patients.insert_one(patient_dict)

        except DuplicateKeyError:
            raise ValueError(f"Patient {patient.patient_id} already exists in the repository !")


class LocalPatientRepository(PatientRepository):

    def _connect(self) -> MongoClient:
        return MongoClient("mongodb://localhost:27017/")
