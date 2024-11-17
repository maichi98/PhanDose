class DicomMetadataError(Exception):
    """Raised when DICOM metadata is not as expected."""


class ModalityNotFoundError(Exception):
    """Raised when modality is not found."""
