from phandose.modalities.modality import Modality

from pathlib import Path
import pydicom as dcm


class RtplanModality(Modality):
    """
    Class for RTPLAN modality.

    Attributes
    ----------
    series_instance_uid : (str)
        Series Instance UID of the RTPLAN modality.

    path_rtplan : (Path)
        Path to the RTPLAN DICOM file.

    series_description : (str)
        Series Description of the RTPLAN modality.

    Methods
    -------
    set_series_description()
        Setter method for the series description of the RTPLAN modality, the series description is extracted
        from the DICOM object metadata.

    dicom()
        Method to return the RTPLAN modality in DICOM format.

    nifti()
        Method to return the RTPLAN modality in NIfTI format.
    """

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path = None,
                 path_rtplan: Path = None,
                 series_description: str = None):
        """
        Constructor for the RtplanModality class.

        Parameters
        ----------
        series_instance_uid : (str)
            Series Instance UID of the RTPLAN series.

        dir_dicom : (Path), optional
            Directory containing the RTPLAN DICOM file, optional if path_rtplan is provided.

        path_rtplan : (Path), optional
            Path to the RTPLAN DICOM file, optional if not provided, it will be determined from dir_dicom.

        series_description : (str), optional
            Series Description of the RTPLAN series.
        """

        super().__init__(series_instance_uid, series_description, "RP")
        self._path_rtplan = path_rtplan
        self._dir_dicom = dir_dicom

    @property
    def path_rtplan(self) -> Path:
        """
        Getter for the path to the RTPLAN DICOM file.

        Returns
        -------
        Path
            the path to the RTPLAN DICOM file.
        """

        if not self._path_rtplan:
            self._path_rtplan = next(path_dicom
                                     for path_dicom in self._dir_dicom.glob("*.dcm")
                                     if dcm.dcmread(path_dicom).SeriesInstanceUID == self.series_instance_uid)

        return self._path_rtplan

    def set_series_description(self):
        """
        Setter for the series description of the RTPLAN modality, the series description is extracted from the
        DICOM object metadata.
        """

        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        """
        Getter for the RTPLAN DICOM object.

        Returns
        -------
        dcm.dataset.FileDataset
            RTPLAN modality in DICOM format.
        """

        return dcm.dcmread(str(self.path_rtplan))

    def nifti(self):
        pass
