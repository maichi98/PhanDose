from phandose.patient import Patient

from pathlib import Path


class PatientHub:

    def __init__(self, dir_patient_hub: Path):

        self._dir_patient_hub = dir_patient_hub
        self._dir_patient_hub.mkdir(parents=True, exist_ok=True)

    def add_patient(self, patient: Patient):

        # set the patient directory in the PatientHub directory :
        path_patient = self._dir_patient_hub / patient.patient_id

        # Save each patient's modality :

            