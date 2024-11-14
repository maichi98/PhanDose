from phandose.patient_hub import PatientHub, PatientHubStorageHandler
from phandose.patient import create_patient_from_dicom_directory

from pathlib import Path
import argparse


def separate_modalities(list_patients: list[str],
                        dir_input: str | Path,
                        dir_output: str | Path,
                        ):

    # Initialize the PatientHub object :
    print("Initializing the PatientHub object...")
    dir_patient_hub = Path(dir_output)
    patient_hub = PatientHub(dir_patient_hub=dir_patient_hub)

    for patient_id in list_patients:

        # Patient DICOM input directory :
        dir_patient = Path(dir_input) / patient_id

        # Initialize the Patient object :
        print(f"Initializing the Patient object for {patient_id}...")
        patient = create_patient_from_dicom_directory(patient_id=patient_id,
                                                      dir_dicom=dir_patient)

        # Store the Patient object in the PatientHub  :
        print(f"Storing {patient_id} in the PatientHub...")
        storage_handler = PatientHubStorageHandler(patient=patient,
                                                   patient_hub=patient_hub)

        for modality in patient.list_modalities:
            modality.store(storage_handler)


def main():
    args = argparse.ArgumentParser()

    args.add_argument('-i', '--dir_input', required=True, type=str,
                      help="Input directory containing the DICOM files.")

    args.add_argument('-o', '--dir_output', required=True, type=str,
                      help="Output directory where the patient hub will be stored.")

    args.add_argument('-p', '--patients', required=False, type=str, nargs='+',
                      help="List of patient IDs to process.")

    args.add_argument('-pf', '--patients_file', required=False, type=str,
                      help="File containing the list of patient IDs to process.")

    args = args.parse_args()

    if not args.patients and not args.patients_file:
        raise ValueError("Please provide either a list of patient IDs or a file containing the list of patient IDs.")

    if args.patients and args.patients_file:
        raise ValueError("Please provide either a list of patient IDs or a file containing the list of patient IDs, "
                         "not both.")

    list_patients = args.patients or [line.strip() for line in open(args.patients_file, 'r').readlines()]

    separate_modalities(list_patients=list_patients,
                        dir_input=args.dir_input,
                        dir_output=args.dir_output)


if __name__ == "__main__":
    main()
