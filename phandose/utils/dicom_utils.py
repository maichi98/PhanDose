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


def find_dicom_path(dir_dicom: Path, sop_instance_uid: str) -> Path:

    """
    Fetch the path of a DICOM file with a specific SOP Instance UID.

    Parameters:
    -----------
    dir_dicom : (Path)
        Directory containing DICOM files.

    sop_instance_uid : (str)
        SOP Instance UID of the DICOM file.

    Returns:
    --------
    Path
        The Path of the DICOM file with the specified SOP Instance UID.
    """

    list_possible_dicoms = [path_dicom
                            for path_dicom in dir_dicom.rglob("*.dcm")
                            if dcm.dcmread(path_dicom).SOPInstanceUID == sop_instance_uid]

    if len(list_possible_dicoms) != 1:
        raise ValueError(f"Number of {sop_instance_uid} DICOM files is {len(list_possible_dicoms)} !")

    return list_possible_dicoms[0]


def find_dicom_paths_of_scan(dir_dicom: Path, series_instance_uid: str) -> list[Path]:

    """
    Filter DICOM slices of a scan.

    Parameters:
    -----------
    dir_dicom : (Path)
        Directory containing DICOM files.

    series_instance_uid : (str)
        Series Instance UID of the scan.

    Returns:
    --------
    list[dcm.dataset.FileDataset]
        List of DICOM slices of the scan.
    """

    # DICOM slices' paths with their Instance Number:
    list_dicom_paths = []

    for path_dicom in dir_dicom.rglob("*.dcm"):

        try:
            dcm_slice = dcm.dcmread(str(path_dicom), stop_before_pixels=True)

            if dcm_slice.SeriesInstanceUID == series_instance_uid:
                slice_position = dcm_slice.get("ImagePositionPatient", None)
                if slice_position and len(slice_position) == 3:
                    z_coordinate = slice_position[2]
                    list_dicom_paths.append((path_dicom, z_coordinate))

        except dcm.errors.InvalidDicomError:
            # Skip files that are not valid DICOM files
            continue

    return [path_dicom for path_dicom, _ in sorted(list_dicom_paths, key=lambda x: x[1])]
