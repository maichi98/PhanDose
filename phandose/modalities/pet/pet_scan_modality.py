from phandose.modalities.modality import Modality

from typing import Generator
from pathlib import Path
import pydicom as dcm


class PETScanModality(Modality):
    """
    Class for the PET scan modality.

    Attributes
    ----------
    series_instance_uid : (str)
        Series Instance UID of the PET scan.

    series_description : (str)
        Series Description of the PET scan.

    dir_dicom : (Path)
        Directory containing the PET DICOM files.

    Methods
    -------
    set_series_description()
        Setter method for the series description of the PET scan, the series description is set to SeriesDescription
        attribute of the first DICOM slice.

    dicom()
        method to return the PET scan modality in DICOM format, yields DICOM slice objects that have the same
        SeriesInstanceUID as the PET scan in order.

    nifti()
        method to return the PET scan modality in NIfTI format.
    """

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path,
                 series_description: str = None):
        """
        Constructor for the PETScanModality class.

        Attributes
        ----------
        series_instance_uid : (str)
            Series Instance UID of the PET scan.

        dir_dicom : (Path)
            Directory containing the PET DICOM files.

        series_description : (str)
            Series Description of the PET scan. (Optional)
        """

        super().__init__(series_instance_uid, series_description, "PET")
        self._dir_dicom = dir_dicom

    @property
    def dir_dicom(self) -> Path:
        """
        Getter method for the directory containing the PET DICOM files.

        Returns
        -------
        Path
            Directory containing the PET DICOM files.
        """

        return self._dir_dicom

    def set_series_description(self):
        """
        Setter method for the series description of the PET scan, the series description is set to SeriesDescription
        attribute of the first DICOM slice.
        """

        self._series_description = next(self.dicom()).SeriesDescription

    def dicom(self) -> Generator[dcm.dataset.FileDataset, None, None]:
        """
        Getter method for the DICOM slices of the PET scan, yields DICOM slice objects that have the same
        SeriesInstanceUID as the PET scan in order.

        Returns
        -------
        Generator[dcm.dataset.FileDataset, None, None]
            DICOM slice objects of the PET scan
        """

        for path_dicom in self._dir_dicom.glob("*.dcm"):
            dicom_slice = dcm.dcmread(str(path_dicom))
            if dicom_slice.SeriesInstanceUID == self.series_instance_uid:
                yield dicom_slice

    def nifti(self):
        pass

    def __repr__(self):
        """
        Returns a developer-friendly representation of the PETScanModality object.

        Returns
        -------
        str
            Developer-friendly representation of the PETScanModality object.

        """

        return (f"PETScanModality(series_instance_uid={self.series_instance_uid},"
                f"series_description={self.series_description},"
                f"dir_dicom={self.dir_dicom})")
