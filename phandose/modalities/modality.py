from abc import ABC, abstractmethod


class Modality(ABC):
    """
    The Modality interface for the different modalities (RTSTRUCT, RTPLAN, RTDOSE, CT).

    Attributes
    ----------
    series_instance_uid : (str)
        The Series Instance UID of the modality.

    series_description : (str)
        The Series Description of the modality.

    modality : (str)
        The modality type (e.g. RS, RP, RD, CT).

    Methods
    -------
    set_series_description()
        Abstract method that sets the Series Description of the modality.

    dicom()
        Abstract method that returns the modality in DICOM format.

    nifti()
        Abstract method that returns the modality in NIfTI format.
    """

    def __init__(self,
                 series_instance_uid: str,
                 series_description: str = None,
                 modality: str = None):
        """
        Initializes the Modality with the Series Instance UID, Series Description, and modality type.

        Attributes
        ----------
        series_instance_uid : (str)
            The Series Instance UID of the modality.

        series_description : (str)
            The Series Description of the modality.

        modality : (str)
            The modality type (e.g. RS, RP, RD, CT).
        """

        self._series_instance_uid = series_instance_uid
        self._series_description = series_description
        self.modality = modality

    @property
    def series_instance_uid(self) -> str:
        """
        Getter for the Series Instance UID.

        Returns
        -------
        str
            The Series Instance UID of the modality.
        """

        return self._series_instance_uid

    @property
    def series_description(self) -> str:
        """
        Getter for the Series Description.

        Returns
        -------
        str
            The Series Description of the modality.
        """

        if not self._series_description:
            self.set_series_description()

        return self._series_description

    @abstractmethod
    def set_series_description(self):
        """
        Abstract method that sets the Series Description of the modality.
        """
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
        """
        Returns a user-friendly string representation of the Modality object.

        Returns
        -------
        str
            The string representation of the Modality object.
        """
        return (f"Modality: {self.modality} - "
                f"Series Instance UID: {self.series_instance_uid} - "
                f"Series Description: {self.series_description}")

    def __repr__(self):
        """
        Returns a developer-friendly string representation of the Modality object.

        Returns
        -------
        str
            The string representation of the Modality object.
        """
        return (f"Modality(series_instance_uid={self.series_instance_uid!r}, "
                f"series_description={self.series_description!r}, "
                f"modality={self.modality!r})")
