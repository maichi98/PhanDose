from abc import ABC, abstractmethod
from pathlib import Path
import pydicom as dcm


class Modality(ABC):
    """
    Abstract class that represents a modality.

    Attributes:
    -----------
    series_instance_uid : (str)
        Series Instance UID.

    Methods:
    --------
    dicom()
        Abstract method that returns the modality in DICOM format.

    nifti()
        Abstract method that returns the modalities in NIfTI format.
    """

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path,
                 modality: str = None,
                 series_description: str = None):
        """
        Constructor of the class Modality.

        Parameters:
        -----------
        series_instance_uid : (str)
            Series Instance UID.

        series_description : (str), optional
            Series Description.
        """

        if not dir_dicom.exists():
            raise FileNotFoundError(f"{str(dir_dicom)} does not exist !")

        self._series_instance_uid = series_instance_uid
        self._series_description = series_description
        self._modality = modality
        self._dir_dicom = dir_dicom

    @property
    def series_instance_uid(self):
        """
        Getter method for the Series Instance UID.
        """

        return self._series_instance_uid

    @property
    def series_description(self):
        """
        Getter method for the Series Description.
        """

        return self._series_description

    @property
    def modality(self):
        """
        Getter method for the Modality.
        """
        return self._modality

    def __str__(self):
        """
        String representation of the class Modality.
        """

        return (f"Series Instance UID: {self._series_instance_uid}, "
                f"Modality: {self._modality}, "
                f"Series Description: {self._series_description}")

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
