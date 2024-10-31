from .rtstruct import RtstructModality
from .rtplan import RtplanModality
from .rtdose import RtdoseModality
from .pet import PETScanModality
from .ct import CTScanModality
from .modality import Modality

from pathlib import Path


def create_modality(modality_id: str,
                    modality_type: str,
                    dir_dicom: Path = None,
                    **kwargs) -> Modality:

    # Dictionary mapping modality types to modality classes :
    dict_modality_classes = {
        "CT": CTScanModality,
        "PET": PETScanModality,
        "RD": RtdoseModality,
        "RS": RtstructModality,
        "RP": RtplanModality
    }

    if modality_type not in dict_modality_classes:
        raise ValueError(f"Unknown modality : {modality_type}")

    modality_class = dict_modality_classes[modality_type]

    return modality_class(modality_id=modality_id,
                          dir_dicom=dir_dicom,
                          **kwargs)
