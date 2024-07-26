from .modality import Modality

from collections.abc import Iterator
from pathlib import Path
import pydicom as dcm


class CTScanModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path = None,
                 series_description: str = None):

        super().__init__(series_instance_uid, series_description, "CT")

        self._dir_dicom = dir_dicom

    def set_series_description(self):

        self._series_description = next(self.dicom()).SeriesDescription

    def dicom(self):

        for path_dicom in self._dir_dicom.glob("*.dcm"):
            dicom_slice = dcm.dcmread(str(path_dicom))
            if dicom_slice.SeriesInstanceUID == self.series_instance_uid:
                yield dicom_slice

    def nifti(self):
        pass
