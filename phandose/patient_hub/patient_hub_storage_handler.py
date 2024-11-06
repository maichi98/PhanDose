from phandose.modalities import (CTScanModality,
                                 PETScanModality,
                                 RtdoseModality,
                                 RtplanModality,
                                 RtstructModality)
from phandose.patient_hub import PatientHub
from phandose.patient import Patient

from pathlib import Path
import shutil


class PatientHubStorageHandler:

    def __init__(self, patient: Patient, patient_hub: PatientHub):

        self._patient = patient
        self._patient_hub = patient_hub

    def store_patient(self):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # Store patient modalities :
        for modality in self._patient.list_modalities:
            modality.store(self)

        # Store the CT or PET modality associated with the primary rtdose :
        scan = self._patient.fetch_scan_linked_to_primary_rtdose()
        dst_folder = f"{scan.modality_type}_TO_TOTALSEGMENTATOR"
        shutil.copytree(src=scan.dir_dicom, dst=dir_patient / dst_folder)

    def store_ct_scan(self, modality: CTScanModality):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # CT directory :
        dir_ct = dir_patient / "CT" / modality.modality_id
        dir_ct.mkdir(parents=True, exist_ok=True)

        # Store CT slices :
        for dicom_slice in modality.dicom():

            path_src = dicom_slice.filename
            path_dst = str(dir_ct / Path(path_src).name)

            shutil.copy2(src=path_src, dst=path_dst)

        # set dir_dicom attribute of the CT modality to the new directory :
        modality.dir_dicom = dir_ct

    def store_pet_scan(self, modality: PETScanModality):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # PET directory :
        dir_pet = dir_patient / "PET" / modality.modality_id
        dir_pet.mkdir(parents=True, exist_ok=True)

        # Store PET slices :
        for dicom_slice in modality.dicom():

            path_src = dicom_slice.filename
            path_dst = str(dir_pet / Path(path_src).name)

            shutil.copy2(src=path_src, dst=path_dst)

        # set dir_dicom attribute of the PET modality to the new directory :
        modality.dir_dicom = dir_pet

    def store_rtdose(self, modality: RtdoseModality):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # RTDOSE directory :
        dir_rtdose = dir_patient / "RD"
        dir_rtdose.mkdir(parents=True, exist_ok=True)

        # Store RTDOSE :
        path_src = modality.path_rtdose
        path_dst = dir_rtdose / Path(path_src).name

        shutil.copy2(src=path_src, dst=path_dst)

        # set path_rtdose attribute of the RTDOSE modality to the new path :
        modality.path_rtdose = path_dst

    def store_rtplan(self, modality: RtplanModality):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # RTPLAN directory :
        dir_rtplan = dir_patient / "RP"
        dir_rtplan.mkdir(parents=True, exist_ok=True)

        # Store RTPLAN :
        path_src = modality.path_rtplan
        path_dst = dir_rtplan / Path(path_src).name

        shutil.copy2(src=path_src, dst=path_dst)

        # set path_rtplan attribute of the RTPLAN modality to the new path :
        modality.path_rtplan = path_dst

    def store_rtstruct(self, modality: RtstructModality):

        # Patient directory :
        dir_patient = self._patient_hub.dir_patient_hub / self._patient.patient_id

        # RTSTRUCT directory :
        dir_rtstruct = dir_patient / "RS"
        dir_rtstruct.mkdir(parents=True, exist_ok=True)

        # Store RTSTRUCT :
        path_src = modality.path_rtstruct
        path_dst = dir_rtstruct / Path(path_src).name

        shutil.copy2(src=path_src, dst=path_dst)

        # set path_rtstruct attribute of the RTSTRUCT modality to the new path :
        modality.path_rtstruct = path_dst
