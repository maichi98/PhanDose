from .modality import Modality

from phandose.utils import dicom_utils
from phandose import conversions

from abc import ABC
from typing import Generator
from pathlib import Path
import pydicom as dcm


class ScanModality(Modality, ABC):

    def __init__(self,
                 modality_id: str,
                 modality_type: str,
                 dicom_paths: Generator[Path, None, None] = None,
                 series_description: str = None,
                 dir_dicom: Path = None):

        super().__init__(modality_id=modality_id,
                         modality_type=modality_type,
                         series_description=series_description,
                         dir_dicom=dir_dicom)

        self._dicom_paths = dicom_paths

    @property
    def dicom_paths(self) -> Generator[Path, None, None]:

        if not self._dicom_paths:
            self.dicom_paths = dicom_utils.find_dicom_paths_of_scan(dir_dicom=self._dir_dicom,
                                                                    series_instance_uid=self.modality_id)

        return self._dicom_paths

    @dicom_paths.setter
    def dicom_paths(self, dicom_paths: Generator[Path, None, None] | list[Path]):

        if isinstance(dicom_paths, list):
            dicom_paths = (path for path in dicom_paths)
        self._dicom_paths = dicom_paths

    def set_series_description(self):
        self._series_description = next(self.dicom()).SeriesDescription

    def dicom(self) -> Generator[dcm.dataset.FileDataset, None, None]:

        yield from (dcm.dcmread(str(path_dicom)) for path_dicom in self.dicom_paths)

    def dataframe(self):
        return conversions.convert_scan_to_dataframe(self.dicom())

    def store(self, storage_handler):
        storage_handler.store_scan(self)


class CTScanModality(ScanModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 dicom_paths: Generator[Path, None, None] = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="CT",
                         dir_dicom=dir_dicom,
                         dicom_paths=dicom_paths,
                         series_description=series_description)


class PETScanModality(ScanModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 dicom_paths: Generator[Path, None, None] = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="PET",
                         dir_dicom=dir_dicom,
                         dicom_paths=dicom_paths,
                         series_description=series_description)
