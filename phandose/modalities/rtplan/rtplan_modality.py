from phandose.modalities.modality import Modality

from pathlib import Path
import pydicom as dcm


class RtplanModality(Modality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 path_rtplan: Path = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id, modality_type="RP", series_description=series_description)

        self._dir_dicom = dir_dicom
        self._path_rtplan = path_rtplan

    def set_path_rtplan(self):
        self._path_rtplan = next(path_dicom
                                 for path_dicom in self._dir_dicom.glob("*.dcm")
                                 if dcm.dcmread(path_dicom).SeriesInstanceUID == self.modality_id)

    @property
    def path_rtplan(self) -> Path:

        if not self._path_rtplan:
            self.set_path_rtplan()

        return self._path_rtplan

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        return dcm.dcmread(str(self.path_rtplan))

    def nifti(self):
        pass

    def get_referenced_rtstruct_uid(self) -> str:

        referenced_rtstruct_sequence = self.dicom().get("ReferencedStructureSetSequence", None)

        if not referenced_rtstruct_sequence:
            raise ValueError(f"RTPLAN {self.modality_id} doesn't reference any RTSTRUCT !")

        return referenced_rtstruct_sequence[0].get("ReferencedSOPInstanceUID")
