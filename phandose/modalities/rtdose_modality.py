from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtdoseModality(Modality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 path_rtdose: Path = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id, modality_type="RD", series_description=series_description)

        self._dir_dicom = dir_dicom
        self._path_rtdose = path_rtdose

    @property
    def path_rtdose(self) -> Path:

        if not self._path_rtdose:
            self.path_rtdose = self.fetch_path_rtdose()

        return self._path_rtdose

    @path_rtdose.setter
    def path_rtdose(self, path_rtdose: Path):
        self._path_rtdose = path_rtdose

    def fetch_path_rtdose(self):
        list_possible_rtdose = [path_dicom
                                for path_dicom in self._dir_dicom.glob("*.dcm")
                                if dcm.dcmread(path_dicom).SOPInstanceUID == self.modality_id]

        if len(list_possible_rtdose) != 1:
            raise ValueError(f"Number of RD files for {self.modality_id} is {len(list_possible_rtdose)} !")

        return list_possible_rtdose[0]

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        return dcm.dcmread(str(self.path_rtdose))

    def is_primary_dose(self) -> bool:

        return self.dicom().get("DoseSummationType") == "PLAN"

    def get_referenced_rtplan_uid(self) -> str:

        referenced_rtplan_sequence = self.dicom().get("ReferencedRTPlanSequence", None)

        if not referenced_rtplan_sequence:
            raise ValueError(f"RTDOSE {self.modality_id} doesn't reference any RTPLAN !")

        return referenced_rtplan_sequence[0].get("ReferencedSOPInstanceUID")

    def store(self, storage_handler):
        storage_handler.store_rtdose(self)
