from .modality import Modality

from abc import ABC, abstractmethod
from typing import Generator
from pathlib import Path
import pydicom as dcm
import dicom2nifti
import tempfile
import ants


class ScanModality(Modality, ABC):

    def __init__(self,
                 modality_id: str,
                 modality_type: str,
                 dir_dicom: Path,
                 series_description: str = None,
                 path_nifti: Path = None):

        super().__init__(modality_id=modality_id, modality_type=modality_type, series_description=series_description)

        self._dir_dicom = dir_dicom
        self._path_nifti = path_nifti

    @property
    def dir_dicom(self) -> Path:
        return self._dir_dicom

    @dir_dicom.setter
    def dir_dicom(self, dir_dicom: Path):
        self._dir_dicom = dir_dicom

    @property
    def path_nifti(self) -> Path:
        return self._path_nifti

    @path_nifti.setter
    def path_nifti(self, path_nifti: Path):
        self._path_nifti = path_nifti

    def set_series_description(self):
        self._series_description = next(self.dicom()).SeriesDescription

    def dicom(self) -> Generator[dcm.dataset.FileDataset, None, None]:
        """
        Getter method for the DICOM slices of the Scan, yields DICOM slice objects that have the same
        SeriesInstanceUID as the scan in order.

        Returns
        -------
        Generator[dcm.dataset.FileDataset, None, None]
            DICOM slice objects of the scan
        """

        for path_dicom in self._dir_dicom.rglob("*.dcm"):
            dicom_slice = dcm.dcmread(str(path_dicom))
            if dicom_slice.SeriesInstanceUID == self.modality_id:
                yield dicom_slice

    def convert_to_nifti(self, path_nifti: Path, overwrite: bool = True):
        """
        Converts the DICOM slices of the Scan to a NIfTI file.

        Parameters
        ----------
        path_nifti : (Path)
            Path to the NIfTI file

        overwrite : (bool), optional
            Overwrite the NIfTI file if it already exists, (Default is False)

        """

        if path_nifti.exists() and not overwrite:
            raise FileExistsError(f"{path_nifti} already exists !")

        dicom2nifti.convert_dicom.dicom_array_to_nifti(list(self.dicom()),
                                                       str(path_nifti),
                                                       reorient_nifti=True)

        self.path_nifti = path_nifti

    def nifti(self):

        if not self.path_nifti:
            path_tmp_nifti = Path(tempfile.mkdtemp()) / f"{self.modality_id}.nii.gz"
            self.path_nifti = path_tmp_nifti

        if not self.path_nifti.exists():
            self.convert_to_nifti(self.path_nifti, overwrite=False)

        return ants.image_read(str(self.path_nifti))

    def run_total_segmentation_task(self, dir_output: Path):
        pass

    @abstractmethod
    def store(self, storage_handler):
        pass


class CTScanModality(ScanModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="CT",
                         dir_dicom=dir_dicom,
                         series_description=series_description)

    def store(self, storage_handler):
        storage_handler.store_ct_scan(self)


class PETScanModality(ScanModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="PET",
                         dir_dicom=dir_dicom,
                         series_description=series_description)

    def store(self, storage_handler):
        storage_handler.store_pet_scan(self)
