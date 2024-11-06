from phandose.patient_hub.patient_hub import PatientHub
from phandose.patient import Patient


class PatientHubLoadingHandler:

    def __init__(self,
                 patient: Patient,
                 patient_hub: PatientHub):

        self._patient = patient
        self._patient_hub = patient_hub

    def load_patient(self):
        pass
