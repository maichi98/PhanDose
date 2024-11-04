from .modality import Modality

from pathlib import Path
import pydicom as dcm
import shutil


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

        list_possible_rtplans = [path_dicom
                                 for path_dicom in self._dir_dicom.glob("*.dcm")
                                 if dcm.dcmread(path_dicom).SOPInstanceUID == self.modality_id]

        if len(list_possible_rtplans) != 1:
            raise ValueError(f"Number of RP files for {self.modality_id} is {len(list_possible_rtplans)} !")

        self._path_rtplan = list_possible_rtplans[0]

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

    def store_dicom(self, dir_patient: Path):

        dir_rtplan = dir_patient / "RP"
        dir_rtplan.mkdir(exist_ok=True, parents=True)

        shutil.copy2(src=str(self.path_rtplan),
                     dst=str(dir_rtplan / self.path_rtplan.name))
