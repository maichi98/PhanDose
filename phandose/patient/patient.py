from phandose.modalities import Modality, create_modality
from phandose import utils

from pathlib import Path
from typing import Dict
import pydicom as dcm


class Patient:

    def __init__(self,
                 patient_id: str,
                 list_modalities: list[Modality] = None):

        self._patient_id = patient_id
        self._list_modalities = list_modalities if list_modalities else []

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def list_modalities(self):
        return self._list_modalities

    @property
    def dict_modalities(self) -> Dict[str, Modality]:
        return {modality.modality_id: modality for modality in self._list_modalities}

    def add_modality(self, modality_id: str, modality_type: str, dir_dicom: Path = None, **kwargs):

        if modality_id not in self.dict_modalities.keys():

            self._list_modalities.append(create_modality(modality_id=modality_id,
                                                         modality_type=modality_type,
                                                         dir_dicom=dir_dicom,
                                                         **kwargs))

    def get_modality(self, modality_id: str) -> Modality:
        return self.dict_modalities.get(modality_id)

    def to_dict(self) -> Dict[str, any]:

        return {
            "patient_id": self.patient_id,
            "modalities": [modality.to_dict() for modality in self.list_modalities]
        }

    @staticmethod
    def from_dir_dicom(patient_id: str, dir_dicom: Path) -> 'Patient':

        # Initialize the patient object :
        patient = Patient(patient_id=patient_id)

        # Loop over all the DICOM files in the directory :
        for path_dicom in dir_dicom.rglob("*.dcm"):

            try:
                dicom_slice = dcm.read_file(str(path_dicom))
                modality_type = utils.get_modality_from_dicom_slice(dicom_slice)

                if modality_type in ['CT', 'PET']:
                    modality_id = dicom_slice.SeriesInstanceUID
                    kwargs = {}

                elif modality_type in ['RD', 'RP', 'RS']:

                    modality_id = dicom_slice.SOPInstanceUID
                    kwargs = {"path_dicom": path_dicom}

                else:
                    raise ValueError(f"Unknown modality type {modality_type} !")

                series_description = dicom_slice.SeriesDescription

                # Add the modality to the patient object :
                patient.add_modality(modality_id=modality_id,
                                     modality_type=modality_type,
                                     dir_dicom=path_dicom.parent,
                                     series_description=series_description,
                                     **kwargs)

            except Exception as e:
                print(f"Error reading DICOM file {path_dicom} : {e}")

        return patient

    @staticmethod
    def from_dict(dict_patient: Dict[str, any]) -> 'Patient':

        # Initialize the patient object :
        patient_id = dict_patient.get("patient_id")
        if not patient_id:
            raise ValueError("dict_patient must contain a 'patient_id' key !")

        patient = Patient(patient_id=patient_id)

        # Add the modalities to the patient object :
        list_dict_modalities = dict_patient.get("modalities", [])

        for dict_modality in list_dict_modalities:
            patient.add_modality(**dict_modality)

        return patient
