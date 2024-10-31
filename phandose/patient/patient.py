from phandose.modalities import Modality


class Patient:

    def __init__(self,
                 patient_id: str,
                 list_modalities: list[Modality] = None):

        self._patient_id = patient_id
        self._dict_modalities = {modality.modality_id: modality
                                 for modality in list_modalities} if list_modalities is not None else {}

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def dict_modalities(self):
        return self._dict_modalities

    def add_modality(self, modality: Modality):
        self._dict_modalities[modality.modality_id] = modality

    def remove_modality(self, modality_id: str):
        self._dict_modalities.pop(modality_id)

    def get_modality(self, modality_id: str):
        return self._dict_modalities.get(modality_id)
