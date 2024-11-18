from phandose.modalities import Modality, ScanModality, StandAloneModality
from phandose.patient import Patient

from abc import ABC, abstractmethod
from pathlib import Path
import shutil


class StorageHandler(ABC):

    @abstractmethod
    def save_patient(self, patient: Patient):
        pass

    @abstractmethod
    def delete_patient(self, patient_id: str):

        pass

    def save_modality(self, patient_id: str, modality: Modality):

        if isinstance(modality, ScanModality):
            self._save_scan_modality(patient_id=patient_id, modality=modality)

        elif isinstance(modality, StandAloneModality):
            self._save_standalone_modality(patient_id=patient_id, modality=modality)

        else:
            raise ValueError(f"Unsupported modality type: {modality.modality_type}")

    def delete_modality(self, patient_id: str, modality: Modality):

        if isinstance(modality, ScanModality):
            self._delete_scan_modality(patient_id=patient_id, modality=modality)

        elif isinstance(modality, StandAloneModality):
            self._delete_standalone_modality(patient_id=patient_id, modality=modality)

        else:
            raise ValueError(f"Unsupported modality type: {modality.modality_type}")

    @abstractmethod
    def _save_scan_modality(self, patient_id: str, modality: ScanModality):
        pass

    @abstractmethod
    def _delete_scan_modality(self, patient_id: str, modality: ScanModality):
        pass

    @abstractmethod
    def _save_standalone_modality(self, patient_id: str, modality: StandAloneModality):
        pass

    @abstractmethod
    def _delete_standalone_modality(self, patient_id: str, modality: StandAloneModality):
        pass


class LocalStorageHandler(StorageHandler):

    def __init__(self, dir_storage: Path):

        self._dir_storage = dir_storage

    @property
    def dir_storage(self):
        return self._dir_storage

    def save_patient(self, patient: Patient):

        for modality in patient.list_modalities:
            self.save_modality(patient_id=patient.patient_id, modality=modality)

    def delete_patient(self, patient_id: str):

        dir_patient = self.dir_storage / patient_id
        shutil.rmtree(dir_patient, ignore_errors=True)

    def _save_scan_modality(self, patient_id: str, modality: ScanModality):

        # Modality specific directory :
        dir_modality = self.dir_storage / patient_id / modality.modality_type / modality.modality_id
        dir_modality.mkdir(parents=True, exist_ok=True)

        urls = []

        # Save the scan data:
        for path_src in modality.dicom_paths:
            path_dst = dir_modality / path_src.name
            shutil.copy2(path_src, path_dst)
            urls.append(path_dst)

        modality.dir_dicom = dir_modality
        modality.dicom_paths = urls

    def _delete_standalone_modality(self, patient_id: str, modality: ScanModality):

        dir_modality = self.dir_storage / patient_id / modality.modality_type / modality.modality_id
        shutil.rmtree(dir_modality, ignore_errors=True)

    def _save_standalone_modality(self, patient_id: str, modality: StandAloneModality):

        # Modality specific directory :
        dir_modality = self.dir_storage / patient_id / modality.modality_type
        dir_modality.mkdir(parents=True, exist_ok=True)

        # Save the standalone data:
        path_src = modality.path_dicom
        path_dst = dir_modality / path_src.name
        shutil.copy2(path_src, path_dst)

        modality.dir_dicom = dir_modality
        modality.path_dicom = path_dst

    def _delete_scan_modality(self, patient_id: str, modality: StandAloneModality):

        path_modality = self.dir_storage / patient_id / modality.modality_type / modality.path_dicom.name
        path_modality.unlink(missing_ok=True)
