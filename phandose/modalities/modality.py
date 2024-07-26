from abc import ABC, abstractmethod
from pathlib import Path
import pydicom as dcm


class Modality(ABC):

    def __init__(self,
                 series_instance_uid: str,
                 series_description: str = None,
                 modality: str = None):

        self._series_instance_uid = series_instance_uid
        self._series_description = series_description
        self._modality = modality

    @property
    def series_instance_uid(self):
        return self._series_instance_uid

    @property
    def series_description(self):

        if not self._series_description:
            self.set_series_description()

        return self._series_description

    @property
    def modality(self):
        return self._modality

    @abstractmethod
    def set_series_description(self):
        pass

    @abstractmethod
    def dicom(self):
        """
        Abstract method that returns the modality in DICOM format.
        """

        pass

    @abstractmethod
    def nifti(self):
        """
        Abstract method that returns the modality in NIfTI format.
        """

        pass
