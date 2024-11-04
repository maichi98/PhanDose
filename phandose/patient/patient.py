from phandose.modalities import Modality, create_modality

from pathlib import Path


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
    def dict_modalities(self):
        return {modality.modality_id: modality for modality in self._list_modalities}

    def add_modality(self, modality_id: str, modality_type: str, dir_dicom: Path = None, **kwargs):

        if modality_id not in self.dict_modalities.keys():
            self._list_modalities.append(create_modality(modality_id=modality_id,
                                                         modality_type=modality_type,
                                                         dir_dicom=dir_dicom,
                                                         **kwargs))

    def get_modality(self, modality_id: str):
        return self.dict_modalities.get(modality_id)
