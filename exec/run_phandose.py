from phandose import convert_nifti_segmentations_to_xyz
from phandose import get_patient_characteristics
from phandose import filter_phantoms
from pathlib import Path
import platform


def main():

    if platform.system() == "Windows":
        dir_patient = Path(fr"C:/Users/maichi/work/My Projects/PhanDose/sample_data") / "AGORL_P33"
        dir_save = Path(fr"C:/Users/maichi/work/My Projects/PhanDose/test")
    else:
        dir_patient = Path("/home/maichi/work/My Projects/PhanDose/sample_data") / "AGORL_P33"
        dir_save = Path("/home/maichi/work/My Projects/PhanDose/test")
    assert dir_patient.exists(), "The patient directory does not exist."
    if not dir_save.exists():
        dir_save.mkdir()

    dir_ct = dir_patient / "CT_TO_TOTALSEGMENTATOR"
    dir_petct = dir_patient / "PET_TO_TOTALSEGMENTATOR"

    print("Create patient characteristics...")
    df_patient_characteristics = get_patient_characteristics(dir_ct, dir_petct)
    df_patient_characteristics.to_csv(dir_save / "patient_characteristics.csv", sep=";", index=False)

    print("Convert NIFTI segmentations to XYZ...")
    dir_nifti_segmentations = dir_patient / "NIFTI_FROM_CT"
    df_contours = convert_nifti_segmentations_to_xyz(dir_nifti_segmentations)
    df_contours.to_csv(dir_save / "contours.csv", sep=";", index=False)

    print("Filter phantoms...")
    # df_full_vertebrae = filter_phantoms(dir_patient / "phantom_lib", df_patient_characteristics, df_contours)


if __name__ == '__main__':
    main()
