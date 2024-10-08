from phandose.modalities.modality import Modality

from pathlib import Path
import pydicom as dcm


class RtdoseModality(Modality):

    def __init__(self,
                 series_instance_uid: str,
                 dir_dicom: Path = None,
                 path_rtdose: Path = None,
                 series_description: str = None):
        """
        Constructor for the RtdoseModality class.

        Attributes
        ----------
        series_instance_uid : (str)
            Series Instance UID of the RTDOSE series

        dir_dicom : (Path)
            Directory containing the RTDOSE DICOM file, (Optional, can be None but only if path_rtdose is provided)

        path_rtdose : (Path)
            Path to the RTDOSE DICOM file, (Optional, if not provided, it will be determined from dir_dicom)

        series_description : (str)
            Series Description of the RTDOSE series
        """

        super().__init__(series_instance_uid, series_description, "RD")
        self._path_rtdose = path_rtdose
        self._dir_dicom = dir_dicom

    @property
    def path_rtdose(self) -> Path:
        """
        Getter for the path to the RTDOSE DICOM file

        Returns
        -------
        Path
            the path to the RTDOSE DICOM file
        """

        if not self._path_rtdose:
            self._path_rtdose = next(path_dicom
                                     for path_dicom in self._dir_dicom.glob("*.dcm")
                                     if dcm.dcmread(path_dicom).SeriesInstanceUID == self.series_instance_uid)

        return self._path_rtdose

    def set_series_description(self):
        """
        Setter for the series description of the RTDOSE modality, the series description is extracted from the
        DICOM object metadata
        """

        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        """
        Getter for the RTDOSE DICOM object

        Returns
        -------
        dcm.dataset.FileDataset
            RTDOSE modality in DICOM format
        """

        return dcm.dcmread(str(self.path_rtdose))

    def nifti(self):
        pass

    def __repr__(self):
        """
        Returns a developer-friendly string representation of the RtdoseModality object.

        Returns
        -------
        str
            The string representation of the RtdoseModality object.

        """

        return (f"RtdoseModality(series_instance_uid={self.series_instance_uid!r}, "
                f"series_description={self.series_description!r}, "
                f"path_rtdose={self.path_rtdose!r})")

    def is_primary_dose(self) -> bool:
        """
        Method to determine if the RTDOSE modality is a primary RTDOSE modality

        Returns
        -------
        bool
            True if the RTDOSE modality is a primary RTDOSE modality, False otherwise
        """

        return self.dicom().get("DoseSummationType") == "PLAN"

    def get_referenced_rtplan_uid(self) -> str:
        """
        Method to get the corresponding RTPLAN Series Instance UID of the RTDOSE modality

        Returns
        -------
        str
            The UID of the corresponding RTPLAN modality
        """

        referenced_rtplan_sequence = self.dicom().get("ReferencedRTPlanSequence", None)

        if not referenced_rtplan_sequence:
            raise ValueError(f"RTDOSE {self.series_instance_uid} doesn't reference any RTPLAN !")

        return referenced_rtplan_sequence[0].get("ReferencedSOPInstanceUID")
