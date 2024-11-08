import pydicom as dcm
import nibabel as nib
import pandas as pd
import numpy as np


def convert_rtdose_to_coordinates(rtdose: dcm.dataset.FileDataset) -> pd.DataFrame:
    """
    Convert a DICOM RTDOSE file to a DataFrame of coordinates.

    The function extracts the coordinates of the dose points from the DICOM RTDOSE file.

    Parameters
    ----------
    rtdose : dcm.dataset.FileDataset
        The DICOM RTDOSE file.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the following columns:
        - x, y, z : Coordinates of the dose point.
        - Dose : Dose value at the dose point.
    """
    # Extract the dose values and the coordinates of the dose points :
    dose_values = rtdose.pixel_array.flatten()
    x, y, z = np.meshgrid(np.arange(rtdose.Columns),
                          np.arange(rtdose.Rows),
                          np.arange(rtdose.NumberOfFrames))

    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    # Create the DataFrame :
    df_dose = pd.DataFrame({"x": x, "y": y, "z": z, "Dose": dose_values})

    return df_dose


def convert_rtstruct_to_coordinates(rtstruct: dcm.dataset.FileDataset) -> pd.DataFrame:

    """
    Convert a DICOM RTSTRUCT file to a DataFrame of coordinates.

    The function extracts the coordinates of the contour points from the DICOM RTSTRUCT file.

    Parameters
    ----------
    rtstruct : dcm.dataset.FileDataset
        The DICOM RTSTRUCT file.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the following columns:
        - ROIName : Name of the ROI.
        - ROINumber : Number of the ROI.
        - ROIContourNumber : Number of the contour.
        - ROIContourPointNumber : Number of the point in the contour.
        - x, y, z : Coordinates of the contour point.
    """
    # Extract the coordinates of the contour points :
    df_contours = pd.DataFrame(columns=["ROIName",
                                        "ROINumber",
                                        "ROIContourNumber",
                                        "ROIContourPointNumber",
                                        "x", "y", "z"])
    roi_number = 0
    contour_number = 0
    contour_point_number = 0

    for roi in rtstruct.StructureSetROISequence:
        roi_number += 1
        roi_name = roi.ROIName

        for contour in roi.ROIContourSequence:
            contour_number += 1
            contour_data = contour.ContourData
            contour_data = np.array(contour_data).reshape(-1, 3)

            for i, point in enumerate(contour_data):
                contour_point_number += 1
                df_contours = df_contours.append({"ROIName": roi_name,
                                                  "ROINumber": roi_number,
                                                  "ROIContourNumber": contour_number,
                                                  "ROIContourPointNumber": contour_point_number,
                                                  "x": point[0],
                                                  "y": point[1],
                                                  "z": point[2]}, ignore_index=True)

    return df_contours


def convert_scan_to_coordinates(scan: nib.Nifti1Image) -> pd.DataFrame:
    """
    Convert a NIFTI scan to a DataFrame of coordinates.

    The function extracts the coordinates of the non-zero voxels from the NIFTI scan.

    Parameters
    ----------
    scan : nib.Nifti1Image
        The NIFTI scan.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the following columns:
        - x, y, z : Coordinates of the non-zero voxel.
    """
    # Extract the coordinates of the non-zero voxels :
    scan_data = scan.get_fdata()
    x, y, z = np.where(scan_data != 0)

    # Create the DataFrame :
    df_scan = pd.DataFrame({"x": x, "y": y, "z": z})

    return df_scan
