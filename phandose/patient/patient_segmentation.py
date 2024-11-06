from totalsegmentator.python_api import totalsegmentator
from pathlib import Path
import nibabel as nib
import tempfile

# Se


def segment_patient_scan(scan: nib.Nifti1Image, dir_output: Path | str):

    dir_output = Path(dir_output)
    dir_output.mkdir(exist_ok=True, parents=True)

    # First, apply run the TotalSegmentator task=total :
    try:
        totalsegmentator(input=scan, output=dir_output, task="total", body_seg=False, output_type="nifti")

    except Exception as e:
        raise ValueError(f"Failed to run TotalSegmentator task=total !") from e

    # Second, apply run the TotalSegmentator task=body :
    dir_temp = Path(tempfile.mkdtemp())
    try:
        totalsegmentator(input=scan, output=dir_temp, task="body", body_seg=False, output_type="nifti")

    except Exception as e:
        raise ValueError(f"Failed to run TotalSegmentator task=body !") from e


