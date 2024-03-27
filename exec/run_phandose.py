from phandose import convert_nifti_segmentations_to_xyz
from phandose import get_patient_characteristics
from pathlib import Path


def main():

    dir_patient = Path("/home/maichi/work/My Projects/PhanDose/sample_data") / "AGORL_P33"

    dir_ct = dir_patient / "CT_TO_TOTALSEGMENTATOR"
    dir_petct = dir_patient / "PET_TO_TOTALSEGMENTATOR"

    df_patient_characteristics = get_patient_characteristics(dir_ct, dir_petct)
    print(df_patient_characteristics)

    dir_nifti_segmentations = dir_patient / "NIFTI_FROM_CT"
    path_output = dir_patient / "output.txt"
    convert_nifti_segmentations_to_xyz(dir_nifti_segmentations).to_csv("/home/maichi/work/test.csv")


if __name__ == '__main__':
    main()
