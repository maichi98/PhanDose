from phandose.modalities import Modality
from phandose.patient import Patient

from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone
from pymongo import MongoClient


class PatientRepository:

    def __init__(self, db_url: str, db_name: str):

        self._client = MongoClient(db_url)
        self._db = self._client[db_name]
        self.patients = self._db["patients"]

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

    def get_patient(self, patient_id: str) -> Patient:

        """
        Retrieve a patient from the repository

        Parameters
        ----------
        patient_id: (str)
            The ID of the patient to retrieve

        Returns
        -------
        patient: Patient
            The patient with the specified ID, or None if the patient doesn't exist

        """

        patient_data = self.patients.find_one({"patient_id": patient_id})
        if not patient_data:
            return None  # Return None if the patient doesn't exist

        # Remove MongoDB-specific fields
        patient_data.pop("_id", None)
        patient_data.pop("created_at", None)
        patient_data.pop("updated_at", None)

        # Convert to Patient object
        return Patient.from_dict(patient_data)

    def delete_patient(self, patient_id: str):
        """
        Delete a patient from the repository

        Parameters
        ----------
        patient_id: (str)
            The ID of the patient to delete

        """

        result = self.patients.delete_one({"patient_id": patient_id})
        if result.deleted_count == 0:
            raise ValueError(f"Patient {patient_id} does not exist in the repository!")
