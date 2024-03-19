from pathlib import Path
import nibabel as nib
import pandas as pd


def convert_nifti_segmentations_to_xyz(dir_segmentations: Path | str,
                                       path_output: Path | str,
                                       **kwargs) -> None:

    dir_segmentations = Path(dir_segmentations)
    segmentation_files = [f for f in dir_segmentations.glob('*.nii.gz') if f.stem not in ["skin.nii.gz", "body.nii.gz"]]

    df_segmentations = pd.DataFrame()
    for segmentation_file in segmentation_files:

        nifti_segmentation = nib.load(segmentation_file)







dir_nifti_segmentations = Path(fr"C:\Users\maichi\work\My Projects\PhanDose\AGORL_P33\NIFTI_FROM_CT")
print(dir_nifti_segmentations.exists())
