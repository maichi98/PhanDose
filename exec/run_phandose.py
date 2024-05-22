from phandose.patient import get_patient_characteristics, convert_nifti_segmentation_directory_to_contours_dataframe


from pathlib import Path
import platform
import time


def main():

    if platform.system() == "Windows":
        dir_project = Path(fr"C:/Users/maichi/work/My Projects/PhanDose")
    else:
        dir_project = Path("/home/maichi/work/My Projects/PhanDose")

    dir_patient = dir_project / "sample_data" / "AGORL_P33"
    dir_save = dir_project / "test"
    dir_phantom_lib = dir_project / "PhantomLib"

    assert dir_patient.exists(), "The patient directory does not exist."
    if not dir_save.exists():
        dir_save.mkdir()

    dir_ct = dir_patient / "CT_TO_TOTALSEGMENTATOR"
    dir_petct = dir_patient / "PET_TO_TOTALSEGMENTATOR"

    print("Create patient characteristics...")
    start_time = time.time()
    df_patient_characteristics = get_patient_characteristics(dir_ct, dir_petct)
    df_patient_characteristics.to_csv(dir_save / "patient_characteristics.csv", sep=";", index=False)
    end_time = time.time()
    print(f"Time to create patient characteristics: {end_time - start_time:.4f} seconds")

    print("Convert NIFTI segmentations to XYZ...")
    start_time = time.time()
    dir_nifti_segmentations = dir_patient / "NIFTI_FROM_CT"
    df_contours = convert_nifti_segmentation_directory_to_contours_dataframe(dir_nifti_segmentations)
    df_contours.to_csv(dir_save / "test_df_contours.csv", sep=";", index=False)
    end_time = time.time()
    print(f"Time to convert NIFTI segmentations to XYZ: {end_time - start_time:.4f} seconds")

    # print("Filter phantoms...")
    # print("Create phantom library...")
    # df_phantom_lib = _get_phantom_lib_dataframe(dir_phantom_lib)
    # df_phantom_lib.to_csv(dir_save / "phantom_lib.csv", sep=";", index=False)
    #
    # print("Create full vertebrae...")
    # df_contours = pd.read_csv(dir_save / "test_df_contours.csv", sep=";")
    #
    # df_full_vertebrae = _get_full_vertebrae_dataframe(df_contours)
    # df_full_vertebrae.to_csv(dir_save / "test_df_full_vertebrae.csv", sep=";", index=False)


if __name__ == '__main__':
    main()
