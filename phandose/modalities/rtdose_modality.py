from .modality import Modality

from pathlib import Path
import pydicom as dcm
import shutil


class RtdoseModality(Modality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 path_rtdose: Path = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id, modality_type="RD", series_description=series_description)

        self._dir_dicom = dir_dicom
        self._path_rtdose = path_rtdose

    def set_path_rtdose(self):

        list_possible_rtdose = [path_dicom
                                for path_dicom in self._dir_dicom.glob("*.dcm")
                                if dcm.dcmread(path_dicom).SOPInstanceUID == self.modality_id]

        if len(list_possible_rtdose) != 1:
            raise ValueError(f"Number of RD files for {self.modality_id} is {len(list_possible_rtdose)} !")

        self._path_rtdose = list_possible_rtdose[0]

    @property
    def path_rtdose(self) -> Path:

        if not self._path_rtdose:
            self.set_path_rtdose()

        return self._path_rtdose

    def set_series_description(self):
        self._series_description = self.dicom().SeriesDescription

    def dicom(self) -> dcm.dataset.FileDataset:
        return dcm.dcmread(str(self.path_rtdose))

    def nifti(self):
        pass

    def is_primary_dose(self) -> bool:

        return self.dicom().get("DoseSummationType") == "PLAN"

    def get_referenced_rtplan_uid(self) -> str:

        referenced_rtplan_sequence = self.dicom().get("ReferencedRTPlanSequence", None)

        if not referenced_rtplan_sequence:
            raise ValueError(f"RTDOSE {self.modality_id} doesn't reference any RTPLAN !")

        return referenced_rtplan_sequence[0].get("ReferencedSOPInstanceUID")

    def store_dicom(self, dir_patient: Path):

        dir_rtdose = dir_patient / "RD"
        dir_rtdose.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src=str(self.path_rtdose),
                     dst=str(dir_rtdose / self.path_rtdose.name))