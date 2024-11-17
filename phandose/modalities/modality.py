from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


class Modality(ABC):
    """
    Abstract base class for modalities like CT, PET, RTSTRUCT, RTDOSE, RTPLAN.

    Subclasses must implement :
    - set_series_description(): Method to initialize the series description.
    - dicom(): Method to return the modality in DICOM format.
    - dataframe(): Method to return the modality as a pandas DataFrame representing values at each world coordinate.
    - to_dict(): Method to serialize the modality as a dictionary.

    """

    def __init__(self,
                 modality_id: str,
                 modality_type: str,
                 series_description: str = None,
                 dir_dicom=None):
        """
        Initializes the Modality with the identifier and modality type.

        Attributes
        ----------
        modality_id : (str)
            Unique identifier for the modality

        modality_type : (str)
            Type of the modality (e.g. CT, PET, RS, RP, RD)

        series_description : (str, Optional)
            Description of the series, defaults to None

        dir_dicom : (Path, Optional)
            Directory containing the DICOM files for the modality, defaults to None

        """

        self._modality_id = modality_id
        self._modality_type = modality_type
        self._series_description = series_description
        self._dir_dicom = dir_dicom

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

    @property
    def dir_dicom(self) -> Path:
        return self._dir_dicom

    @dir_dicom.setter
    def dir_dicom(self, dir_dicom: Path):

        if not dir_dicom.exists():
            raise FileNotFoundError(f"Directory {dir_dicom} doesn't exist !")

        self._dir_dicom = dir_dicom

    @abstractmethod
    def set_series_description(self):
        """ Set the series description for the modality """
        pass

    @abstractmethod
    def dicom(self):
        """ Return the modality in DICOM format """
        pass

    @abstractmethod
    def dataframe(self) -> pd.DataFrame:
        """ Return the modality as a pandas DataFrame representing values at each world coordinate """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """ Return a dictionary representation of the modality """
        pass

    def __str__(self):
        return f"Modality: {self.modality_type} - UID: {self.modality_id}"

    __repr__ = __str__
