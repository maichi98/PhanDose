from multiprocessing import Pool
from skimage import measure
from pathlib import Path
import nibabel as nib
import pandas as pd
import numpy as np


def convert_nifti_segmentation_directory_to_contours_dataframe(dir_segmentations: Path | str) -> pd.DataFrame:
    """
    Convert all NIFTI segmentation files in a given directory to a dataframe of contours
    described with x, y, z coordinates.

    The function extracts contours from all NIFTI segmentation files generated by TotalSegmentator,
     excluding "skin.nii.gz" and "body.nii.gz".

    Parameters
    ----------
    dir_segmentations: (Path or str)
        Path to the directory containing the NIFTI segmentation files.

    Returns
    -------
    df_contours: pd.DataFrame
        the contours DataFrame with the following columns:
        - ROIName: Name of the ROI, derived from the filename of the NIFTI segmentation file.
        - ROINumber: Number of the ROI, starting from 1, based on the order of the NIFTI segmentation files.
        - ROIContourNumber: Number of the contour
        - ROIContourPointNumber: Number of the point in the contour
        - x, y, z : Adjusted coordinates of the contour point.


    """
    dir_segmentations = Path(dir_segmentations)

    # List of all segmentation files in the directory, excluding "skin.nii.gz" and "body.nii.gz"
    segmentation_files = [f for f in dir_segmentations.glob('*.nii.gz') if f.name not in ["skin.nii.gz", "body.nii.gz"]]

    # Pool of workers to convert each segmentation file to a DataFrame of contours :
    with Pool() as pool:
        list_df_contours = pool.starmap(convert_nifti_segmentation_file_to_contours_dataframe,
                                        [(f, i + 1) for i, f in enumerate(segmentation_files)])

    # Concatenate and reorder the columns :
    dict_cols = {
        "ROIName": str,
        "ROINumber": int,
        "ROIContourNumber": int,
        "ROIContourPointNumber": int,
        "x": float,
        "y": float,
        "z": float
    }
    cols = list(dict_cols.keys())

    if len(list_df_contours) == 0:
        df_contours = pd.DataFrame(columns=cols)
    else:
        df_contours = pd.concat(list_df_contours, ignore_index=True)[cols]

    return df_contours.astype(dict_cols)


# TODO: Can be optimized further using multi-threading
def convert_nifti_segmentation_file_to_contours_dataframe(path_segmentation_file: Path,
                                                          roi_number: int = 1) -> pd.DataFrame:
    """
    Convert a NIFTI segmentation file to a dataframe of contours described with x, y, z coordinates.

    Parameters
    ----------
    path_segmentation_file: (Path)
        Path to the NIFTI segmentation file, of a single organ, or a single ROI.

    roi_number: (int)
        Number of the ROI, default is 1.

    Returns
    -------
    df_contours: pd.DataFrame
        the contours DataFrame with the following columns:
        - ROIName: Name of the ROI, derived from the filename of the NIFTI segmentation file.
        - ROINumber: Number of the ROI.
        - ROIContourNumber: Number of the contour, starting from 1, based on the order of the contours.
        - ROIContourPointNumber: Number of the point in the contour
        - x, y, z : Adjusted coordinates of the contour point.

    """

    # Initialize the contours dataframe list to be concatenated :
    list_df_contours = []

    # Load the header, and the 3D matrix of the segmentation :
    nii_segmentation = nib.load(path_segmentation_file)
    affine_segmentation = nii_segmentation.affine
    data_segmentation = nii_segmentation.get_fdata()

    # Initialize a counter for the number of contours :
    contour_number = 0

    # loop over each slice in the 3D matrix :
    for slice_number in range(data_segmentation.shape[2]):

        # Find the contours in the current slice :
        slice_segmentation = data_segmentation[:, :, slice_number]
        contours = measure.find_contours(slice_segmentation, 0.5)

        # Loop over every contour :
        for contour in contours:
            contour_number += 1

            df_contour = pd.DataFrame(contour, columns=["x", "y"])
            df_contour["z"] = slice_number

            # Adjust the x, y and z coordinates based on the header information :
            df_contour["ones"] = 1
            df_contour[["x", "y", "z", "ones"]] = np.dot(affine_segmentation, df_contour[["x", "y", "z", "ones"]].T).T
            df_contour.drop(columns=["ones"], inplace=True)

            # Add additional information about the ROI :
            df_contour["ROIContourPointNumber"] = 1 + np.arange(len(df_contour))
            df_contour["ROIContourNumber"] = contour_number
            df_contour["ROIName"] = path_segmentation_file.name.removesuffix(".nii.gz").replace("_", " ")
            df_contour["ROINumber"] = roi_number

            list_df_contours.append(df_contour)

    # Concatenate and reorder the columns :
    dict_cols = {
        "ROIName": str,
        "ROINumber": int,
        "ROIContourNumber": int,
        "ROIContourPointNumber": int,
        "x": float,
        "y": float,
        "z": float
    }
    cols = list(dict_cols.keys())

    if len(list_df_contours) == 0:
        df_contours = pd.DataFrame(columns=cols)
    else:
        df_contours = pd.concat(list_df_contours, ignore_index=True)[cols]

    return df_contours.astype(dict_cols)


# TODO: Implement this function
def convert_dicom_segmentation_file_to_contours_dataframe(dir_segmentations: Path | str) -> pd.DataFrame:
    pass
