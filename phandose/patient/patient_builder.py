from .patient import Patient

from pathlib import Path
import pydicom as dcm


class PatientBuilderFromDirectory:

    def __init__(self):

        self._patient_id = None
        self._list_modalities = None

    def patient_id(self, patient_id: str):
        self._patient_id = patient_id
        return self

    def list_modalities(self, dir_patient: Path):

        dict_modalities = {}

        # Iterate over the files in the directory of the patient :
        for path_file in dir_patient.rglob("*"):

            # Check if the file is a DICOM file :
            if path_file.is_file() and path_file.suffix == ".dcm":

                # Read the DICOM file :
                dicom_slice = dcm.dcmread(str(path_file))

    def build(self):
        return Patient(patient_id=self._patient_id,
                       list_modalities=self._list_modalities)
