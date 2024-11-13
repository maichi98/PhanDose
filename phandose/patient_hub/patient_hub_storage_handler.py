from phandose.modalities import (ScanModality,
                                 StandAloneModality)

from phandose.patient_hub import PatientHub
from phandose.patient import Patient

from pathlib import Path
import shutil


class PatientHubStorageHandler:

    def __init__(self, patient: Patient, patient_hub: PatientHub):

        self._patient = patient
        self._patient_hub = patient_hub

    def store_scan(self, modality: ScanModality):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # Scan directory :
        dir_scan = dir_patient / modality.modality_type / modality.modality_id
        dir_scan.mkdir(parents=True, exist_ok=True)

        # Store scan slices :
        for dicom_slice in modality.dicom():

            path_src = dicom_slice.filename
            path_dst = str(dir_scan / Path(path_src).name)

            shutil.copy2(src=path_src, dst=path_dst)

        # set dir_dicom attribute of the scan modality to the new directory :
        modality.dir_dicom = dir_scan

    def store_standalone(self, modality: StandAloneModality):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # Modality directory :
        dir_modality = dir_patient / modality.modality_type
        dir_modality.mkdir(parents=True, exist_ok=True)

        # Store standalone modality :
        path_src = modality.path_dicom
        path_dst = dir_modality / Path(path_src).name

        shutil.copy2(src=path_src, dst=path_dst)

        # set path_dicom attribute of the standalone modality to the new path :
        modality.path_dicom = path_dst
