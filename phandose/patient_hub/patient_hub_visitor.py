from phandose.modalities import Modality

from abc import ABC, abstractmethod
from pathlib import Path


class PatientHubVisitor(ABC):

    @abstractmethod
    def visit_ct_scan(self, modality: Modality, dir_patient: Path):
        pass

    @abstractmethod
    def visit_pet_scan(self, modality: Modality, dir_patient: Path):
        pass

    @abstractmethod
    def visit_rtdose(self, modality: Modality, dir_patient: Path):
        pass

    @abstractmethod
    def visit_rtplan(self, modality: Modality, dir_patient: Path):
        pass

    @abstractmethod
    def visit_rtstruct(self, modality: Modality, dir_patient: Path):
        pass

