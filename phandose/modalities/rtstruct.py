from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtstructModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 path_rtstruct: Path,
                 series_description: str = None):

        super().__init__(series_instance_uid, series_description)
        self._path_rtstruct = path_rtstruct

    def dicom(self):
        return dcm.dcmread(str(self._path_rtstruct))

    def nifti(self):
        pass
