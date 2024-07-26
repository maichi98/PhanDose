from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtdoseModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path = None,
                 path_rtdose: Path = None,
                 series_description: str = None):

        super().__init__(series_instance_uid, series_description, "RD")

        self._path_rtdose = path_rtdose
        self._dir_dicom = dir_dicom

    @property
    def path_rtdose(self):

        if not self._path_rtdose:
            self._path_rtdose = next(path_dicom
                                     for path_dicom in self._dir_dicom.glob("*.dcm")
                                     if dcm.dcmread(path_dicom).SeriesInstanceUID == self.series_instance_uid)

        return self._path_rtdose

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self):
        return dcm.dcmread(str(self.path_rtdose))

    def nifti(self):
        pass
