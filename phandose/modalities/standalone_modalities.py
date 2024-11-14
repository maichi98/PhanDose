from phandose.utils import dicom_utils
from phandose import conversions
from .modality import Modality

from abc import ABC
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

            if not self.dir_dicom:
                raise ValueError("DICOM directory is not set. Please provide a valid directory containing DICOM files !")
            self.path_dicom = dicom_utils.find_dicom_path(dir_dicom=self.dir_dicom, sop_instance_uid=self.modality_id)

        return self._path_dicom

    @path_dicom.setter
    def path_dicom(self, path_dicom: Path):
        self._path_dicom = path_dicom

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

    def dataframe(self):
        return conversions.convert_rtdose_to_dataframe(self.dicom())

    def is_primary_dose(self) -> bool:
        return self.dicom().get("DoseSummationType") == "PLAN"

    def get_referenced_rtplan_uid(self) -> str:
        referenced_rtplan_sequence = self.dicom().get("ReferencedRTPlanSequence", None)

        if not referenced_rtplan_sequence:
            raise ValueError(f"RTDOSE {self.modality_id} doesn't reference any RTPLAN !")

        return referenced_rtplan_sequence[0].get("ReferencedSOPInstanceUID")


class RtstructModality(StandAloneModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 path_rtstruct: Path = None,
                 series_description: str = None,
                 dir_nifti: Path = None):

        super().__init__(modality_id=modality_id,
                         modality_type="RS",
                         dir_dicom=dir_dicom,
                         path_dicom=path_rtstruct,
                         series_description=series_description)

        self._dir_nifti = dir_nifti

    @property
    def path_rtstruct(self) -> Path:
        return self.path_dicom

    @path_rtstruct.setter
    def path_rtstruct(self, path_rtstruct: Path):
        self.path_dicom = path_rtstruct

    def dataframe(self):
        pass

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


class RtplanModality(StandAloneModality):

    def __init__(self,
                 modality_id: str,
                 dir_dicom: Path = None,
                 path_rtplan: Path = None,
                 series_description: str = None):

        super().__init__(modality_id=modality_id,
                         modality_type="RP",
                         dir_dicom=dir_dicom,
                         path_dicom=path_rtplan,
                         series_description=series_description)

    @property
    def path_rtplan(self) -> Path:
        return self.path_dicom

    def dataframe(self):
        raise NotImplementedError("RT Plan files do not contain volumetric data and cannot be converted to DataFrame !")

    @path_rtplan.setter
    def path_rtplan(self, path_rtplan: Path):
        self.path_dicom = path_rtplan

    def get_referenced_rtstruct_uid(self) -> str:

        referenced_rtstruct_sequence = self.dicom().get("ReferencedStructureSetSequence", None)

        if not referenced_rtstruct_sequence:
            raise ValueError(f"RTPLAN {self.modality_id} doesn't reference any RTSTRUCT !")

        return referenced_rtstruct_sequence[0].get("ReferencedSOPInstanceUID")

