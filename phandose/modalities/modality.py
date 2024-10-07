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
