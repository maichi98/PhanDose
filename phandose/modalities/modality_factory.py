from .rtstruct import RtstructModality
from .ct_scan import CTScanModality
from .rtplan import RtplanModality
from .rtdose import RtdoseModality
from .modality import Modality

from pathlib import Path


def create_modality(modality: str,
                    series_instance_uid: str,
                    dir_dicom: Path = None,
                    **kwargs) -> Modality:

    dict_modality_classes = {
        "CT": CTScanModality,
        "RD": RtdoseModality,
        "RS": RtstructModality,
        "RP": RtplanModality
    }

    if modality not in dict_modality_classes:
        raise ValueError(f"Unknown modality : {modality}")

    modality_class = dict_modality_classes[modality]
    return modality_class(series_instance_uid=series_instance_uid,
                          dir_dicom=dir_dicom,
                          modality=modality,
                          **kwargs)
