from phandose.patient_hub.storage_handler import LocalStorageHandler
from phandose.patient import Patient
from phandose import utils

from tqdm import tqdm
from pathlib import Path
import argparse

# Create a logger object :
logger = utils.get_logger("separate_modalities")


def separate_modalities(list_patients: list[str],
                        dir_input: str | Path,
                        dir_output: str | Path,
                        ):

    # Initialize the PatientHub object :
    tqdm.write("Initializing the Storage Handler object...")
    dir_storage = Path(dir_output)

    storage_handler = LocalStorageHandler(dir_storage=dir_storage)

    progress_bar = tqdm(total=len(list_patients), desc="Starting...", ncols=100)
    for patient_id in list_patients:

        # Patient DICOM input directory
        dir_patient = Path(dir_input) / patient_id

        # Initialize the Patient object
        message = f"Initializing {patient_id} ..."
        progress_bar.set_description(message)
        patient = Patient.from_dir_dicom(patient_id=patient_id, dir_dicom=dir_patient)

        # Store the Patient object in the PatientHub
        message = f"Storing {patient_id} ..."
        progress_bar.set_description(message)
        try:
            storage_handler.save_patient(patient=patient)
            message = f"{patient_id} stored successfully !"
            tqdm.write(message)

        except ValueError as e:
            storage_handler.delete_patient(patient_id=patient_id)
            message = f"Failed to store {patient_id}, error {e}!"
            tqdm.write(message)

        # Update the progress bar
        progress_bar.update(1)

    progress_bar.close()


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
