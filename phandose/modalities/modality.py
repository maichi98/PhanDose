from abc import ABC, abstractmethod


class Modality(ABC):
    """
    The Modality interface for the different modalities (RTSTRUCT, RTPLAN, RTDOSE, CT).

    """

    def __init__(self,
                 uid: str,
                 modality: str = None):
        """
        Initializes the Modality with the identifier and modality type.

        Attributes
        ----------
        uid : (str)
            The UID of the modality.

        modality : (str)
            The modality type (e.g. RS, RP, RD, CT).
        """

        self._uid = uid
        self.modality = modality

    @property
    def uid(self) -> str:

        return self._uid

    @property
    def series_instance_uid(self) -> str:

        return self.dicom().SeriesInstanceUID

    @property
    def series_description(self) -> str:

        return self.dicom().SeriesDescription

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

    def __str__(self):

        return f"Modality: {self.modality} - UID: {self.uid}"

    __repr__ = __str__

