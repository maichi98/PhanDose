from .modality import Modality

from pathlib import Path
import pydicom as dcm


class RtstructModality(Modality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 path_rtstruct: Path = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id, modality_type="RS", series_description=series_description)

        self._dir_dicom = dir_dicom
        self._path_rtstruct = path_rtstruct

    @property
    def path_rtstruct(self) -> Path:

        if not self._path_rtstruct:
            self.path_rtstruct = self.fetch_path_rtstruct()

        return self._path_rtstruct

    @path_rtstruct.setter
    def path_rtstruct(self, path_rtstruct: Path):
        self._path_rtstruct = path_rtstruct

    def fetch_path_rtstruct(self):

        list_possible_rtstruct = [path_dicom
                                  for path_dicom in self._dir_dicom.glob("*.dcm")
                                  if dcm.dcmread(path_dicom).SOPInstanceUID == self.modality_id]

        if len(list_possible_rtstruct) != 1:
            raise ValueError(f"Number of RS files for {self.modality_id} is {len(list_possible_rtstruct)} !")

        return list_possible_rtstruct[0]

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        return dcm.dcmread(str(self.path_rtstruct))

    def get_referenced_scan_uid(self) -> str:

        referenced_frame_sequence = self.dicom().get("ReferencedFrameOfReferenceSequence", None)
        if not referenced_frame_sequence:
            raise ValueError(f"RTSTRUCT {self.modality_id} doesn't reference any Scan, issue at Frame of reference !")

        referenced_study_sequence = referenced_frame_sequence[0].get("RTReferencedStudySequence", None)
        if not referenced_study_sequence:
            raise ValueError(f"RTSTRUCT {self.modality_id} doesn't reference any Scan, issue at study !")

        referenced_ct = referenced_study_sequence[0].get("RTReferencedSeriesSequence", None)
        if not referenced_ct:
            raise ValueError(f"RTSTRUCT {self.modality_id} doesn't reference any Scan, issue at series !")

        return referenced_ct[0].get("SeriesInstanceUID")

    def store(self, storage_handler):
        storage_handler.store_rtstruct(self)
