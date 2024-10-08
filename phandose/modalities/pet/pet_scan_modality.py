from phandose.modalities.modality import Modality

from typing import Generator
from pathlib import Path
import pydicom as dcm


class PETScanModality(Modality):

    def __init__(self,
                 uid: str,
                 dir_dicom: Path):

        super().__init__(uid, "PET")
        self._dir_dicom = dir_dicom

    @property
    def dir_dicom(self) -> Path:

        return self._dir_dicom

    @property
    def series_instance_uid(self):

        return next(self.dicom()).SeriesInstanceUID

    @property
    def series_description(self):

        return next(self.dicom()).SeriesDescription

    def dicom(self) -> Generator[dcm.dataset.FileDataset, None, None]:
        """
        Getter method for the DICOM slices of the PET scan, yields DICOM slice objects that have the same
        SeriesInstanceUID as the PET scan in order.

        Returns
        -------
        Generator[dcm.dataset.FileDataset, None, None]
            DICOM slice objects of the PET scan
        """

        for path_dicom in self._dir_dicom.glob("*.dcm"):
            dicom_slice = dcm.dcmread(str(path_dicom))
            if dicom_slice.SeriesInstanceUID == self.series_instance_uid:
                yield dicom_slice

    def nifti(self):
        pass
