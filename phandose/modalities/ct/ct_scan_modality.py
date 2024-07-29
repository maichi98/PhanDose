from phandose.modalities.modality import Modality

from pathlib import Path
import pydicom as dcm


class CTScanModality(Modality):
    """
    Class for the CT scan modality.

    Attributes
    ----------
    series_instance_uid : (str)
        Series Instance UID of the CT scan.

    series_description : (str)
        Series Description of the CT scan.

    dir_dicom : (Path)
        Directory containing the CT DICOM files.

    Methods
    -------
    set_series_description()
        Setter method for the series description of the CT scan, the series description is set to SeriesDescription
        attribute of the first DICOM slice.

    dicom()
        method to return the CT scan modality in DICOM format, yields DICOM slice objects that have the same
        SeriesInstanceUID as the CT scan in order.

    nifti()
        method to return the CT scan modality in NIfTI format.
    """

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path,
                 series_description: str = None):
        """
        Constructor for the CTScanModality class.

        Attributes
        ----------
        series_instance_uid : (str)
            Series Instance UID of the CT scan.

        dir_dicom : (Path)
            Directory containing the CT DICOM files.

        series_description : (str)
            Series Description of the CT scan. (Optional)
        """

        super().__init__(series_instance_uid, series_description, "CT")
        self._dir_dicom = dir_dicom

    @property
    def dir_dicom(self) -> Path:
        """
        Getter method for the directory containing the CT DICOM files.

        Returns
        -------
        Path
            Directory containing the CT DICOM files.
        """

        return self._dir_dicom

    def set_series_description(self):
        """
        Setter method for the series description of the CT scan, the series description is set to SeriesDescription
        attribute of the first DICOM slice.
        """

        self._series_description = next(self.dicom()).SeriesDescription

    def dicom(self) -> iter(dcm.dataset.FileDataset):
        """
        Getter method for the DICOM slices of the CT scan, yields DICOM slice objects that have the same
        SeriesInstanceUID as the CT scan in order.

        Returns
        -------
        iter(dcm.dataset.FileDataset)
            DICOM slice objects of the CT scan
        """

        for path_dicom in self._dir_dicom.glob("*.dcm"):
            dicom_slice = dcm.dcmread(str(path_dicom))
            if dicom_slice.SeriesInstanceUID == self.series_instance_uid:
                yield dicom_slice

    def nifti(self):
        pass
