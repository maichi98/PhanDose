from phandose.modalities.modality import Modality

from pathlib import Path
import pydicom as dcm


class RtstructModality(Modality):
    """
    Class for RTSTRUCT modality.

    Attributes
    ----------
    series_instance_uid : (str)
        Series Instance UID of the RTSTRUCT modality.

    path_rtstruct : (Path)
        Path to the RTSTRUCT DICOM file.

    series_description : (str)
        Series Description of the RTSTRUCT modality.

    Methods
    -------
    set_series_description()
        Setter method for the series description of the RTSTRUCT modality, the series description is extracted
        from the DICOM object metadata.

    dicom()
        Method to return the RTSTRUCT modality in DICOM format.

    nifti()
        Method to return the RTSTRUCT modality in NIfTI format.
    """

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path = None,
                 path_rtstruct: Path = None,
                 series_description: str = None):
        """
        Constructor for the RtstructModality class.

        Parameters
        ----------
        series_instance_uid : (str)
            Series Instance UID of the RTSTRUCT series.

        dir_dicom : (Path), optional
            Directory containing the RTSTRUCT DICOM file, optional if path_rtstruct is provided.

        path_rtstruct : (Path), optional
            Path to the RTSTRUCT DICOM file, optional if not provided, it will be determined from dir_dicom.

        series_description : (str), optional
            Series Description of the RTSTRUCT series.
        """

        super().__init__(series_instance_uid, series_description, "RS")
        self._path_rtstruct = path_rtstruct
        self._dir_dicom = dir_dicom

    @property
    def path_rtstruct(self) -> Path:
        """
        Getter for the path to the RTSTRUCT DICOM file.

        Returns
        -------
        Path
            the path to the RTSTRUCT DICOM file.
        """

        if not self._path_rtstruct:
            self._path_rtstruct = next(path_dicom
                                       for path_dicom in self._dir_dicom.glob("*.dcm")
                                       if dcm.dcmread(path_dicom).SeriesInstanceUID == self.series_instance_uid)

        return self._path_rtstruct

    def set_series_description(self):
        """
        Setter for the series description of the RTSTRUCT modality, the series description is extracted from the
        DICOM object metadata.
        """

        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        """
        Getter for the RTSTRUCT DICOM object.

        Returns
        -------
        dcm.dataset.FileDataset
            RTSTRUCT modality in DICOM format.
        """

        return dcm.dcmread(str(self.path_rtstruct))

    def nifti(self):
        pass
