from . import Modality, MODALITY_REGISTRY

from pathlib import Path


def create_modality(modality_id: str,
                    modality_type: str,
                    dir_dicom: Path = None,
                    **kwargs) -> Modality:

    """
    Factory function to create a modality instance based on the modality type.

    Parameters
    ----------
    modality_id : (str)
        Unique identifier for the modality.

    modality_type : (str)
        Type of the modality (e.g., "CT", "PET", "RD", "RS", "RP").

    dir_dicom : (Path, Optional)
        Directory containing the DICOM files for the modality, Defaults to None.

    **kwargs : (dict)
        Additional keyword arguments specific to the modality type, to be passed to the modality constructor.

    Returns
    -------
    modality : Modality
        An instance of the modality class corresponding to the modality type

    Raises
    ------
    ValueError
        If the modality type is not supported

    """

    modality_class = MODALITY_REGISTRY.get(modality_type)

    if not modality_class:
        supported_types = ", ".join(MODALITY_REGISTRY.keys())
        raise ValueError(f"Unsupported modality type '{modality_type}'."
                         f" Supported types are: {supported_types}")

    return modality_class(modality_id=modality_id,
                          dir_dicom=dir_dicom,
                          **kwargs)
