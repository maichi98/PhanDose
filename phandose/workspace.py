from .patient import Patient


class Workspace:

    def __init__(self,
                 list_patients: list[Patient] = None,
                 ):

        self._dict_patients = {patient.patient_id: patient
                               for patient in list_patients} if list_patients is not None else {}

    @property
    def dict_patients(self):
        return self._dict_patients

    def add_patient(self, patient: Patient):
        self._dict_patients[patient.patient_id] = patient