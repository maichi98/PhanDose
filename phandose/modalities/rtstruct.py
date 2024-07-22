from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtplanModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 path_rtplan: Path,
                 series_description: str = None):

        super().__init__(series_instance_uid, series_description)
        self._path_rtplan = path_rtplan

    def dicom(self):
        return dcm.dcmread(str(self._path_rtplan))

    def nifti(self):
        pass
