from pathlib import Path


class PatientHub:

    def __init__(self, dir_patient_hub: Path):

        self._dir_patient_hub = dir_patient_hub
        self._dir_patient_hub.mkdir(parents=True, exist_ok=True)

    @property
    def dir_patient_hub(self):
        return self._dir_patient_hub
