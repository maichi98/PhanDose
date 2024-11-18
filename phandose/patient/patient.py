from phandose.modalities import Modality, create_modality
from phandose.utils import (get_modality_from_dicom_slice,
                            get_logger)

from pathlib import Path
from typing import Dict
import pydicom as dcm

# Initialize the logger :
logger = get_logger("phandose.patient")


class Patient:

    def __init__(self,
                 patient_id: str,
                 list_modalities: list[Modality] = None):
        """
        Initialize a Patient object.

        Parameters
        ----------
        patient_id : (str)
            The unique patient ID of the patient.

        """

        self._patient_id = patient_id
        self._list_modalities = list_modalities if list_modalities else []

        logger.debug(f"Patient object initialized with ID: {self.patient_id} and {len(self.list_modalities)} modalities")
        for i, modality in enumerate(self.list_modalities):
            logger.debug(f"Patient {self.patient_id} modality {i + 1} : {modality.modality_id} ({modality.modality_type})")

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def list_modalities(self):
        return self._list_modalities

    @property
    def dict_modalities(self) -> Dict[str, Modality]:
        return {modality.modality_id: modality for modality in self._list_modalities}

    def add_modality(self, modality_id: str, modality_type: str, dir_dicom: Path = None,
                     log_silently_if_exists: bool = False,
                     **kwargs):
        """
        Add a modality to the patient.

        Parameters
        ----------
        modality_id : (str)
            The unique modality ID of the modality.

        modality_type : (str)
            The type of the modality (e.g. CT, PET, RD, RP, RS).

        dir_dicom : (Path, Optional)
            The directory containing the DICOM files for the modality.

        log_silently_if_exists : (bool, Optional)
            If True, the logger will not be displayed if the modality already exists for the patient, by default False.

        **kwargs : (dict)
            Additional keyword arguments to pass to the modality creation function.

        """
        try:

            if modality_id in self.dict_modalities.keys():
                if not log_silently_if_exists:
                    logger.warning(f"Modality {modality_id} already exists for patient {self.patient_id} !")
                return

            logger.debug(f"Adding modality {modality_id} to patient {self.patient_id} ...")
            self._list_modalities.append(create_modality(modality_id=modality_id,
                                                         modality_type=modality_type,
                                                         dir_dicom=dir_dicom,
                                                         **kwargs))

            logger.info(f"Successfully added modality {modality_id} ({modality_type}) to patient {self.patient_id} !")

        except Exception as e:
            logger.error(f"Failed to add modality {modality_id} ({modality_type}) to patient {self.patient_id} : {e}")
            raise e

    def get_modality(self, modality_id: str) -> Modality:
        return self.dict_modalities.get(modality_id)

    def to_dict(self) -> Dict[str, any]:

        return {
            "patient_id": self.patient_id,
            "modalities": [modality.to_dict() for modality in self.list_modalities]
        }

    @staticmethod
    def from_dir_dicom(patient_id: str, dir_dicom: Path) -> 'Patient':
        """
        Create a Patient object from a directory containing DICOM files.

        Parameters
        ----------
        patient_id : (str)
            The unique patient ID of the patient.

        dir_dicom : (Path)
            The directory containing the DICOM files for the patient.

        Returns
        -------
        patient : Patient
            The patient object created from the DICOM files and the patient ID.
        """

        logger.debug(f"Attempting to create patient object for ID {patient_id}, from DICOM directory : {dir_dicom} ...")

        # Initialize the patient object :
        patient = Patient(patient_id=patient_id)

        # Check if directory exists and is not empty :
        if not dir_dicom.exists() or not any(dir_dicom.rglob("*.dcm")):
            logger.error(fr"No DICOM files found in directory {dir_dicom} !")
            raise FileNotFoundError(f"No DICOM files found in directory {dir_dicom} !")

        errors = []

        # Loop over all the DICOM files in the directory :
        for path_dicom in dir_dicom.rglob("*.dcm"):
            try:
                dicom_slice = dcm.read_file(str(path_dicom))
                modality_type = get_modality_from_dicom_slice(dicom_slice)

                if modality_type in ['CT', 'PET']:
                    modality_id = dicom_slice.SeriesInstanceUID
                    kwargs = {}

                elif modality_type in ['RD', 'RP', 'RS']:
                    modality_id = dicom_slice.SOPInstanceUID
                    kwargs = {"path_dicom": path_dicom}

                else:
                    raise ValueError(f"Unknown modality type {modality_type} for file {str(path_dicom)}")

                series_description = dicom_slice.SeriesDescription

                # Add the modality to the patient object :
                patient.add_modality(modality_id=modality_id,
                                     modality_type=modality_type,
                                     dir_dicom=path_dicom.parent,
                                     series_description=series_description,
                                     log_silently_if_exists=True,
                                     **kwargs)

            except Exception as e:
                errors.append((str(path_dicom), str(e)))

        # Log summary of errors
        if errors:
            logger.warning(f"Completed Patient creation for {patient_id} with {len(errors)} errors.")
            for path, error in errors:
                logger.warning(f"Error for file {path}: {error}")

        logger.debug(fr"Completed Patient creation for {patient_id} from DICOM directory : {dir_dicom} "
                     fr"with {len(errors)} errors.")
        return patient

    @staticmethod
    def from_dict(dict_patient: Dict[str, any]) -> 'Patient':
        """
        Create a Patient object from a dictionary representation.

        Parameters
        ----------
        dict_patient : (Dict)
            The dictionary representation of the patient object, containing the patient ID and modalities.

        Returns
        -------
        patient : Patient
            The patient object created from the dictionary representation.

        """

        logger.debug("Creating patient object from dictionary representation ...")

        # Initialize the patient object :
        patient_id = dict_patient.get("patient_id")
        if not patient_id:
            logger.error("Failed to create Patient object: 'patient_id' key is missing in dictionary !")
            raise ValueError("dict_patient must contain a 'patient_id' key!")

        patient = Patient(patient_id=patient_id)

        # Add the modalities to the patient object :
        list_dict_modalities = dict_patient.get("modalities", [])

        try:
            for i, dict_modality in enumerate(list_dict_modalities):
                logger.debug(f"Processing modality {i + 1}/{len(list_dict_modalities)} for patient {patient_id} :")
                patient.add_modality(**dict_modality)

            logger.debug(f"Completed creation of Patient object from dictionary with ID {patient_id} "
                         f"and {len(patient.list_modalities)} modalities.")

        except Exception as e:
            logger.error(f"Failed to create Patient object from dictionary! Error : {e}")
            raise e

        return patient
