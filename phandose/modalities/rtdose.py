from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtdoseModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path,
                 series_description: str = None):

        super().__init__(series_instance_uid, dir_dicom, "RS", series_description)

        self._path_rtdose = None

    @property
    def path_rtdose(self):
        """
        Getter method for the path of the RTDOSE file.
        """

        if self._path_rtdose is not None:
            return self._path_rtdose

