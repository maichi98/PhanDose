from phandose.modalities import Modality, create_modality
from phandose.utils import get_logger

from pathlib import Path
from typing import cast

# Set up logger :
logger = get_logger("Patient")


class Patient:

    def __init__(self,
                 patient_id: str,
                 list_modalities: list[Modality] = None):

        self._patient_id = patient_id
        self._list_modalities = list_modalities if list_modalities else []
        logger.debug(f"Created patient with ID {patient_id}, containing {len(self._list_modalities)} modalities")

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def list_modalities(self):
        return self._list_modalities

    @property
    def dict_modalities(self):
        return {modality.modality_id: modality for modality in self._list_modalities}

    def add_modality(self, modality_id: str, modality_type: str, dir_dicom: Path = None, **kwargs):

        logger.debug(f"Attempting to add {modality_type} modality with ID {modality_id} to patient {self.patient_id} ... ")

        if modality_id in self.dict_modalities.keys():
            logger.error(f"Modality with ID {modality_id} already exists in the patient !")
            raise ValueError(f"Modality with ID {modality_id} already exists in the patient !")

        self._list_modalities.append(create_modality(modality_id=modality_id,
                                                     modality_type=modality_type,
                                                     dir_dicom=dir_dicom,
                                                     **kwargs))

        logger.debug(f"Added {modality_type} modality with ID {modality_id} to patient {self.patient_id}")

    def get_modality(self, modality_id: str):
        return self.dict_modalities.get(modality_id)

    def fetch_primary_rtdose(self):

        logger.debug(f"Fetching primary RTDOSE for patient {self.patient_id} ...")

        from phandose.modalities import RtdoseModality

        for modality in self.list_modalities:

            if isinstance(modality, RtdoseModality) and modality.is_primary_dose():
                logger.debug(f"Primary RTDOSE found for patient {self.patient_id}, with UID {modality.modality_id}")
                return modality

        logger.error(f"No primary RTDOSE found in the patient {self.patient_id} !")
        raise ValueError("No primary RTDOSE found in the patient !")

    def fetch_scan_linked_to_primary_rtdose(self):

        from phandose.modalities import RtplanModality, RtstructModality

        primary_rtdose = self.fetch_primary_rtdose()
        uid_rtplan = primary_rtdose.get_referenced_rtplan_uid()

        rtplan = cast(RtplanModality, self.get_modality(uid_rtplan))
        uid_rtstruct = rtplan.get_referenced_rtstruct_uid()

        rtstruct = cast(RtstructModality, self.get_modality(uid_rtstruct))
        uid_scan = rtstruct.get_referenced_scan_uid()

        return uid_scan
