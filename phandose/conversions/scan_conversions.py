from phandose import exceptions

import nibabel as nib
from typing import Iterable
import dask.dataframe as dd
from dask import delayed
import pydicom as dcm
import pandas as pd
import numpy as np


def convert_scan_to_nifti(dicom_slices: Iterable[dcm.dataset.FileDataset]) -> nib.Nifti1Image:
    pass


def convert_scan_to_dataframe(dicom_slices: Iterable[dcm.dataset.FileDataset]) -> pd.DataFrame:
    """
    Converts an iterable of DICOM slices to a DataFrame with coordinates and intensity values.

    Parameters
    ----------
    dicom_slices : (Iterable[dcm.dataset.FileDataset])
        An iterable containing DICOM slices of the scan, they should be sorted by

    Returns
    -------
    pd.DataFrame,
        DataFrame with columns ['x', 'y', 'z', 'intensity'], where each row represents a voxel
        with its 3D coordinates and intensity value.
    """
    @delayed
    def compute_voxel_coords(n_rows, n_cols, spacing):

        if not spacing or len(spacing) != 2:
            raise exceptions.DicomMetadataError("Invalid PixelSpacing !")

        # Create the meshgrid of the voxel coordinates :
        row_indices = np.arange(n_rows) * spacing[0]
        col_indices = np.arange(n_cols) * spacing[1]

        x_grid, y_grid = np.meshgrid(row_indices, col_indices, indexing='ij')
        z_grid = np.zeros_like(x_grid)
        voxel_coords = np.stack([x_grid, y_grid, z_grid], axis=-1).reshape(-1, 3)

        return voxel_coords

    @delayed
    def compute_orientation(image_orientation):

        if not image_orientation or len(image_orientation) != 6:
            raise exceptions.DicomMetadataError("Invalid ImageOrientationPatient !")

        x_vector, y_vector = np.array(image_orientation).reshape(2, 3)
        z_vector = np.cross(x_vector, y_vector)
        orientation = np.array([x_vector, y_vector, z_vector])
        return orientation

    @delayed
    def process_slice(dicom_slice, cached_orientation, cached_voxel_coords):

        # Extract and rescale the pixel intensities :
        pixel_array = np.array(dicom_slice.pixel_array)
        slope = dicom_slice.get('RescaleSlope', 1)
        intercept = dicom_slice.get('RescaleIntercept', 0)
        intensities = (pixel_array.ravel() * slope) + intercept

        # Transform the voxel coordinates to world coordinates :
        origin = dicom_slice.ImagePositionPatient
        if not origin or len(origin) != 3:
            raise exceptions.DicomMetadataError("Invalid ImagePositionPatient !")

        origin = np.array(origin)

        world_coords = (cached_voxel_coords @ cached_orientation.T) + origin

        return pd.DataFrame({'x': world_coords[:, 0],
                             'y': world_coords[:, 1],
                             'z': world_coords[:, 2],
                             'intensity': intensities})

    cached_orientation = {}
    cached_voxel_coords = {}
    results = []

    for dicom_slice in dicom_slices:

        # extract metadata :
        try:
            n_rows, n_cols = dicom_slice.pixel_array.shape
            spacing = dicom_slice.PixelSpacing
            image_orientation = tuple(dicom_slice.ImageOrientationPatient)
        except AttributeError as e:
            raise exceptions.DicomMetadataError("Missing metadata in DICOM slice !") from e

        # compute or retrieve voxel coordinates :
        if image_orientation not in cached_orientation:
            cached_orientation[image_orientation] = compute_orientation(image_orientation)

        # compute or retrieve orientation :
        voxel_key = (n_rows, n_cols, tuple(spacing))
        if voxel_key not in cached_voxel_coords:
            cached_voxel_coords[voxel_key] = compute_voxel_coords(n_rows, n_cols, spacing)

        # process the slice :
        results.append(process_slice(dicom_slice,
                                     cached_orientation[image_orientation],
                                     cached_voxel_coords[voxel_key]))

    # Convert the delayed objects to a Dask DataFrame :
    df_data = dd.from_delayed(results)

    return df_data.compute()
