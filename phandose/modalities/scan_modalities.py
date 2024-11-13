from .modality import Modality

from phandose import conversions

from abc import ABC
from typing import Generator
from pathlib import Path
import pydicom as dcm


class ScanModality(Modality, ABC):

    def __init__(self,
                 modality_id: str,
                 modality_type: str,
                 dir_dicom: Path,
                 series_description: str = None):

        super().__init__(modality_id=modality_id, modality_type=modality_type, series_description=series_description)

        self._dir_dicom = dir_dicom

    @property
    def dir_dicom(self) -> Path:
        return self._dir_dicom

    @dir_dicom.setter
    def dir_dicom(self, dir_dicom: Path):

        if not dir_dicom.exists():
            raise FileNotFoundError(f"{dir_dicom} does not exist !")

        self._dir_dicom = dir_dicom

    def set_series_description(self):
        self._series_description = next(self.dicom()).SeriesDescription

    def dicom_paths(self) -> Generator[Path, None, None]:

        # DICOM slices' paths with their Instance Number:
        list_dicom_paths = []

        for path_dicom in self.dir_dicom.rglob("*.dcm"):

            try:
                dcm_slice = dcm.dcmread(str(path_dicom), stop_before_pixels=True)

                if dcm_slice.SeriesInstanceUID == self.modality_id:
                    instance_number = dcm_slice.get("InstanceNumber", None)

                    if instance_number:
                        list_dicom_paths.append((path_dicom, instance_number))

            except dcm.errors.InvalidDicomError:
                # Skip files that are not valid DICOM files
                continue

        # Sort by Instance Number:
        for path_dicom, _ in sorted(list_dicom_paths, key=lambda x: x[1]):
            yield path_dicom

    def dicom(self) -> Generator[dcm.dataset.FileDataset, None, None]:

        for path_dicom in self.dicom_paths():
            yield dcm.dcmread(str(path_dicom))

    def dataframe(self):
        return conversions.convert_scan_to_dataframe(self.dicom())

    def store(self, storage_handler):
        storage_handler.store_scan(self)


class CTScanModality(ScanModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="CT",
                         dir_dicom=dir_dicom,
                         series_description=series_description)


class PETScanModality(ScanModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="PET",
                         dir_dicom=dir_dicom,
                         series_description=series_description)
