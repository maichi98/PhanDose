from abc import ABC, abstractmethod


class PatientBuilder(ABC):

    @abstractmethod
    def build_dict_modalities(self):
        pass
