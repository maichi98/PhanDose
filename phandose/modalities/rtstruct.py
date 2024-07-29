from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtstructModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path = None,
                 path_rtstruct: Path = None,
                 series_description: str = None):

        super().__init__(series_instance_uid, series_description, "RS")

        self._path_rtstruct = path_rtstruct
        self._dir_dicom = dir_dicom

    @property
    def path_rtstruct(self):

        if not self._path_rtstruct:
            self._path_rtstruct = next(path_dicom
                                       for path_dicom in self._dir_dicom.glob("*.dcm")
                                       if dcm.dcmread(path_dicom).SeriesInstanceUID == self.series_instance_uid)

        return self._path_rtstruct

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self):
        return dcm.dcmread(str(self.path_rtstruct))

    def nifti(self):
        pass
