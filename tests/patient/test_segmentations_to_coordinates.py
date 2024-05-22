from phandose.patient.segmentations_to_coordinates import convert_nifti_segmentation_directory_to_contours_dataframe
from phandose.patient.segmentations_to_coordinates import convert_nifti_segmentation_file_to_contours_dataframe

from pathlib import Path
import nibabel as nib
import pandas as pd
import numpy as np
import unittest


class TestSegmentationsToCoordinates(unittest.TestCase):

    def setUp(self):
        self.dir_sample_patient_data = Path(__file__).parent.parent.parent / 'sample_data' / "AGORL_P33"
        self.dir_nifti_segmentations = self.dir_sample_patient_data / "NIFTI_FROM_CT"
        self.path_nifti_brain_segmentation = self.dir_nifti_segmentations / "brain.nii.gz"

    def test_convert_nifti_segmentation_file_to_contours_dataframe(self):

        # Create a dummy organ NIFTI segmentation file :
        # --- First, let's create a header for out dummy NIFTI segmentation file :
        header = nib.Nifti1Header()
        header['dim'] = np.array([3, 512, 512, 512, 1, 1, 1, 1], dtype="int16")
        header['pixdim'] = np.array([-1, 1.0, 1.5, 4.0, 1.0, 1.0, 1.0, 1.0], dtype="float32")

        header["qoffset_x"] = np.array(250, dtype='float32')
        header["qoffset_y"] = np.array(-30, dtype='float32')
        header["qoffset_z"] = np.array(-456, dtype='float32')
        # --- Now, let's create a dummy 3D matrix for the segmentation :
        data = np.zeros((512, 512, 512), dtype="int16")
        data[200:300, 200:300, 200:300] = 1  # Create a cube in the middle of the 3D matrix
        mask_half_sphere = x ** 2 + y ** 2 + z ** 2 > # add a half-sphere on top of the cube :

    def test_convert_nifti_segmentation_directory_to_contours_dataframe(self):
        pass


if __name__ == '__main__':
    unittest.main()
