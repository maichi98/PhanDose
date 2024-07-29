from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtplanModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path = None,
                 path_rtplan: Path = None,
                 series_description: str = None):

        super().__init__(series_instance_uid, series_description, "RP")

        self._path_rtplan = path_rtplan
        self._dir_dicom = dir_dicom

    @property
    def path_rtplan(self):

        if not self._path_rtplan:
            self._path_rtplan = next(path_dicom
                                     for path_dicom in self._dir_dicom.glob("*.dcm")
                                     if dcm.dcmread(path_dicom).SeriesInstanceUID == self.series_instance_uid)

        return self._path_rtplan

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self):
        return dcm.dcmread(str(self.path_rtplan))

    def nifti(self):
        pass
