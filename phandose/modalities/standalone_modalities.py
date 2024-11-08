from .modality import Modality

from abc import ABC, abstractmethod
from pathlib import Path
import pydicom as dcm


class StandAloneModality(Modality, ABC):

    def __init__(self,
                 modality_id: str,
                 modality_type: str,
                 dir_dicom: Path = None,
                 path_dicom: Path = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id, modality_type=modality_type, series_description=series_description)

        self._dir_dicom = dir_dicom
        self._path_dicom = path_dicom

    @property
    def path_dicom(self) -> Path:

        if not self._path_dicom:
            self.path_dicom = self.fetch_path_dicom()

        return self._path_dicom

    @path_dicom.setter
    def path_dicom(self, path_dicom: Path):
        self._path_dicom = path_dicom

    def fetch_path_dicom(self):
        list_possible_rtdose = [path_dicom
                                for path_dicom in self._dir_dicom.glob("*.dcm")
                                if dcm.dcmread(path_dicom).SOPInstanceUID == self.modality_id]

        if len(list_possible_rtdose) != 1:
            raise ValueError(f"Number of {self.modality_id} DICOM files is {len(list_possible_rtdose)} !")

        return list_possible_rtdose[0]

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        return dcm.dcmread(str(self.path_dicom))

    def store(self, storage_handler):
        storage_handler.store_standalone(self)


class RtdoseModality(StandAloneModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 path_rtdose: Path = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="RD",
                         dir_dicom=dir_dicom,
                         path_dicom=path_rtdose,
                         series_description=series_description)

    @property
    def path_rtdose(self) -> Path:
        return self.path_dicom

    @path_rtdose.setter
    def path_rtdose(self, path_rtdose: Path):
        self.path_dicom = path_rtdose

    def is_primary_dose(self) -> bool:
        return self.dicom().get("DoseSummationType") == "PLAN"

    def get_referenced_rtplan_uid(self) -> str:
        referenced_rtplan_sequence = self.dicom().get("ReferencedRTPlanSequence", None)

        if not referenced_rtplan_sequence:
            raise ValueError(f"RTDOSE {self.modality_id} doesn't reference any RTPLAN !")

        return referenced_rtplan_sequence[0].get("ReferencedSOPInstanceUID")