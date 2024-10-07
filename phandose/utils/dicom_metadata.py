from pathlib import Path
import pydicom as dcm


def get_modality_from_dicom_slice(dicom_slice):
    """
    Get the modality of a DICOM slice.

    Parameters:
    -----------
    dicom_slice : (pydicom.dataset.FileDataset)
        DICOM slice.

    Returns:
    --------
    str
        Modality of the DICOM slice.
    """

    dict_modalities = {"RTDOSE": "RD", "RTPLAN": "RP", "RTSTRUCT": "RS"}
    modality = dicom_slice.Modality.upper()

    if modality in dict_modalities.keys():
        return dict_modalities[modality]

    if modality == "CT":

        code_meaning = dicom_slice.get('ProcedureCodeSequence')[0].get('CodeMeaning')

        if 'TDM' in code_meaning:
            return 'CT'
        elif 'TEP' or 'PET' in code_meaning:
            return 'PET'
        else:
            raise ValueError(fr"Not yet determined how to interpret {code_meaning} ! ")

    raise ValueError(fr"Not yet determined how to interpret {modality} !")


def get_series_instance_uid_from_directory(dir_dicom: Path) -> str:
    """
    Get the Series Instance UID of a DICOM directory.

    Parameters:
    -----------
    dir_dicom : (Path)
        Directory containing DICOM files.

    Returns:
    --------
    str
        Series Instance UID of the DICOM directory.
    """

    dicom_files = list(dir_dicom.rglob("*.dcm"))
    if not dicom_files:
        raise ValueError("No DICOM files found in the directory !")

    series_instance_uids = {dcm.dcmread(str(dicom_file)).SeriesInstanceUID for dicom_file in dicom_files}
    if len(series_instance_uids) > 1:
        raise ValueError("Series Instance UID mismatch in the directory !")

    return series_instance_uids.pop()
