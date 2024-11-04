from .modality import Modality

from typing import Generator
from pathlib import Path
import pydicom as dcm
import shutil


class PETScanModality(Modality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path,
                 series_description: str = None):

        super().__init__(modality_id=modality_id, modality_type="PET", series_description=series_description)

        self._dir_dicom = dir_dicom

    @property
    def dir_dicom(self) -> Path:
        return self._dir_dicom

    def set_series_description(self):
        self._series_description = next(self.dicom()).SeriesDescription

    def dicom(self) -> Generator[dcm.dataset.FileDataset, None, None]:
        """
        Getter method for the DICOM slices of the CT scan, yields DICOM slice objects that have the same
        SeriesInstanceUID as the CT scan in order.

        Returns
        -------
        Generator[dcm.dataset.FileDataset, None, None]
            DICOM slice objects of the CT scan
        """

        for path_dicom in self._dir_dicom.rglob("*.dcm"):
            dicom_slice = dcm.dcmread(str(path_dicom))
            if dicom_slice.SeriesInstanceUID == self.modality_id:
                yield dicom_slice

    def nifti(self):
        pass

    def store_dicom(self, dir_patient: Path):

        dir_pet = dir_patient / "PET" / self.modality_id
        dir_pet.mkdir(parents=True, exist_ok=True)

        for path_dicom in self.dir_dicom.rglob("*.dcm"):
            dicom_slice = dcm.dcmread(str(path_dicom))

            if dicom_slice.SeriesInstanceUID == self.modality_id:
                shutil.copy2(src=str(path_dicom),
                             dst=str(dir_pet / path_dicom.name))