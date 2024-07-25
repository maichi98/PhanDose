from .modality import Modality

from pathlib import Path
import pydicom as dcm


class CTScanModality(Modality):
    """
    Class that represents a CT Scan modality.

    Attributes:
    -----------
    series_instance_uid : (str)
        Series Instance UID.

    list_path_slices : (list[Path])
        List of paths to the slices of the CT Scan.

    series_description : (str), optional
        Series Description.

    Methods:
    --------
    dicom()
        Returns the CT modality in DICOM format.

    nifti()
        Returns the CT modality in NIfTI format.
    """

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom_slices: Path,
                 series_description: str = None):

        """
        Constructor of the class CTScanModality.

        Parameters:
        -----------
        series_instance_uid : (str)
            Series Instance UID.

        dir_dicom_slices : (Path)
            Directory of the DICOM slices of the CT Scan.

        series_description : (str), optional
            Series Description.
        """

        super().__init__(series_instance_uid, series_description)
        self._dir_dicom_slices = dir_dicom_slices

    @property
    def dir_dicom_slices(self):
        """
        Getter method for the Directory of the DICOM slices of the CT Scan.
        """

        return self._dir_dicom_slices

    def dicom(self):
        """
        Returns the CT modality in DICOM format.
        """
        for path_slice in self._dir_dicom_slices.glob('*.dcm'):
            dcm_slice = dcm.read_file(path_slice)
            if dcm_slice.SeriesInstanceUID == self._series_instance_uid:
                yield dcm_slice

    def nifti(self):
        """
        Returns the CT modality in NIfTI format.
        """

        pass
