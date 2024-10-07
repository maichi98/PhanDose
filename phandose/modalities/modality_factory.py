from .rtstruct import RtstructModality
from .rtplan import RtplanModality
from .rtdose import RtdoseModality
from .ct import CTScanModality
from .modality import Modality

from pathlib import Path


def create_modality(modality: str,
                    series_instance_uid: str,
                    dir_dicom: Path = None,
                    **kwargs) -> Modality:
    """
    Factory function to create a modality object based on the modality type.

    Parameters
    ----------
    modality : (str)
        Modality type.

    series_instance_uid : (str)
        SeriesInstanceUID of the modality.

    dir_dicom : (Path)
        Directory containing the DICOM files.

    **kwargs : (dict)
        Additional keyword arguments. (Optional) :

        series_description : (str)
            SeriesDescription of the modality.

        path_rtstruct : (Path)
            Path to the RTSTRUCT file. (Only for RTSTRUCT modality)

        path_rtplan : (Path)
            Path to the RTPLAN file. (Only for RTPLAN modality)

        path_rtdose : (Path)
            Path to the RTDOSE file. (Only for RTDOSE modality)

    Returns
    -------
    modality : (Modality)
        Modality object

    Raises
    ------
    ValueError
        If the modality type is unknown.
    """

    # Dictionary mapping modality types to modality classes :
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
                          **kwargs)
