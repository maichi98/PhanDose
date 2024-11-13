from phandose import exceptions

import nibabel as nib
import pydicom as dcm
import pandas as pd
import numpy as np


def compute_orientation(image_orientation):
    """
    Computes the orientation matrix from the image orientation vector.

    Parameters
    ----------
    image_orientation : (np.ndarray)
        Image orientation vector (6 elements)

    Returns
    -------
    np.ndarray,
        The orientation matrix (3x3) computed from the image orientation vector.

    Raises
    ------
    exceptions.DicomMetadataError
        If the image orientation vector is invalid.

    """
    if not image_orientation or len(image_orientation) != 6:
        raise exceptions.DicomMetadataError("Invalid ImageOrientationPatient !")

    x_vector, y_vector = np.array(image_orientation).reshape(2, 3)
    z_vector = np.cross(x_vector, y_vector)
    orientation = np.array([x_vector, y_vector, z_vector])
    return orientation


def extract_dose_grid(rtdose: dcm.dataset.Dataset) -> np.ndarray:

    # Extract the dose grid and apply scaling :
    dose_grid = rtdose.pixel_array.astype(np.float32)
    try:
        dose_grid *= rtdose.DoseGridScaling
    except AttributeError as e:
        raise exceptions.DicomMetadataError("Missing DoseScaling attribute !") from e

    return dose_grid


def convert_rtdose_to_nifti(rtdose: dcm.dataset.Dataset) -> nib.Nifti1Image:

    # Extract the dose grid :
    dose_grid = extract_dose_grid(rtdose)

    # Transpose the dose grid to match the NIfTI convention :
    dose_grid = dose_grid.transpose(1, 0, 2)

    # Extract spatial metadata :
    try:
        pixel_spacing = rtdose.PixelSpacing
        slice_thickness = rtdose.SliceThickness
        origin = np.array(rtdose.ImagePositionPatient)
        image_orientation = np.array(rtdose.ImageOrientationPatient).reshape(2, 3)

    except AttributeError as e:
        raise exceptions.DicomMetadataError("Missing spatial metadata !") from e

    # Compute the orientation matrix :
    orientation = compute_orientation(image_orientation)

    # construct the transformation matrix :
    affine = np.eye(4)
    affine[:3, :3] = orientation * np.array(pixel_spacing + [slice_thickness])
    affine[:3, 3] = origin

    return nib.Nifti1Image(dose_grid, affine)


def convert_rtdose_to_dataframe(rtdose: dcm.dataset.Dataset) -> pd.DataFrame:

    # Extract the dose grid :
    dose_grid = extract_dose_grid(rtdose)

    # Extract spatial metadata :
    try:
        pixel_spacing = rtdose.PixelSpacing
        slice_thickness = rtdose.SliceThickness
        origin = np.array(rtdose.ImagePositionPatient)
        image_orientation = np.array(rtdose.ImageOrientationPatient).reshape(2, 3)

    except AttributeError as e:
        raise exceptions.DicomMetadataError("Missing spatial metadata !") from e

    # Compute the orientation matrix :
    orientation = compute_orientation(image_orientation)

    # Compute the voxel coordinates :
    n_slices, n_rows, n_cols = dose_grid.shape
    row_indices = np.arange(n_rows) * pixel_spacing[0]
    col_indices = np.arange(n_cols) * pixel_spacing[1]
    slice_indices = np.arange(n_slices) * slice_thickness

    x_grid, y_grid, z_grid = np.meshgrid(row_indices, col_indices, slice_indices, indexing='ij')
    voxel_coords = np.stack([x_grid, y_grid, z_grid], axis=-1).reshape(-1, 3)

    # Compute the world coordinates :
    world_coords = (voxel_coords @ orientation.T) + origin

    # Flatten the dose grid :
    dose_values = dose_grid.ravel()

    # Construct the DataFrame :
    df_dose = pd.DataFrame({
        'x': world_coords[:, 0],
        'y': world_coords[:, 1],
        'z': world_coords[:, 2],
        'dose': dose_values
    })

    return df_dose
