"""
The `modalities` submodule provides tools for handling radiotherapy-related modalities,
including CT, PET, and DICOM-based RT objects like RTSTRUCT, RTPLAN, and RTDOSE.

Features:
- Abstract base class for modalities: `Modality`.
- Specific modality types: `CTScanModality`, `PETScanModality`, `RtstructModality`, etc.
- Factory function: `create_modality` for creating modalities dynamically.
"""

# Import modality classes
from .modality import Modality
from .scan_modalities import (ScanModality,
                              CTScanModality,
                              PETScanModality)
from .standalone_modalities import (StandAloneModality,
                                    RtstructModality,
                                    RtplanModality,
                                    RtdoseModality)

# Registry for available modalities
MODALITY_REGISTRY = {
    "CT": CTScanModality,
    "PET": PETScanModality,
    "RS": RtstructModality,
    "RP": RtplanModality,
    "RD": RtdoseModality
}

# Import factory
from .modality_factory import create_modality

# Public API :
__all__ = ["Modality",
           "ScanModality",
           "CTScanModality",
           "PETScanModality",
           "StandAloneModality",
           "RtstructModality",
           "RtplanModality",
           "RtdoseModality",
           "create_modality",
           "MODALITY_REGISTRY"]

# Version of the modality submodule
__version__ = "1.0.0"
