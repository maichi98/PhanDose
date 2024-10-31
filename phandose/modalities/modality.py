from abc import ABC, abstractmethod


class Modality(ABC):
    """
    The Modality interface for the different modalities (RTSTRUCT, RTPLAN, RTDOSE, CT).

    """

    def __init__(self,
                 modality_id: str,
                 modality_type: str,
                 series_description: str = None):
        """
        Initializes the Modality with the identifier and modality type.

        Attributes
        ----------
        modality_id : (str)
            Identifier of the modality

        modality_type : (str)
            Type of the modality (RTSTRUCT, RTPLAN, RTDOSE, CT)

        series_description : (str), optional
            Description of the series, (Default is None)

        """

        self._modality_id = modality_id
        self._modality_type = modality_type
        self._series_description = series_description

    @property
    def modality_id(self) -> str:
        return self._modality_id

    @property
    def modality_type(self) -> str:
        return self._modality_type

    @property
    def series_description(self) -> str:
        if self._series_description is None:
            self.set_series_description()

        return self._series_description

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

    def __str__(self):
        return f"Modality: {self.modality_type} - UID: {self.modality_id}"

    __repr__ = __str__
