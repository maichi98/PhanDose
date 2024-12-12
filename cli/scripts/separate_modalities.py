from phandose.patient_hub.storage_handler import LocalStorageHandler
from phandose.utils import (add_file_handler_to_root,
                            enable_tqdm_logging,
                            get_logger)
from phandose.patient import Patient

from tqdm import tqdm
from pathlib import Path
import argparse
import logging
import time

# Initialize the logger for this script
logger = get_logger("cli.scripts.separate_modalities")


def separate_modalities(list_patients: list[str],
                        dir_input: str | Path,
                        dir_output: str | Path,
                        verbose: bool = False,
                        log_level: str = "DEBUG",
                        dir_log: str | Path = None):

    """
    Separate modalities for a list of patients and store them in the output directory.

    Parameters
    ----------
    list_patients : (list[str])
        List of patient IDs to process.

    dir_input : (str | Path)
        Input directory containing the DICOM files.

    dir_output : (str | Path)
        Output directory where the patient hub will be stored.

    verbose : (bool, Optional)
        Enable verbose logging (per-run logging), by default False.

    log_level : (str, Optional)
        Logging level for the per-run file, by default "DEBUG".

    dir_log : (str | Path, Optional)
        Directory for per-run log files, by default dir_output.

    """

    # Initialize the logger :
    dir_log = Path(dir_log) if dir_log else Path(dir_output)

    # Enable per-run logging if verbose is enabled
    if verbose:
        log_level = getattr(logging, log_level.upper(), logging.DEBUG)
        add_file_handler_to_root(dir_log=dir_log,
                                 prefix="separate_modalities",
                                 level=log_level)

    # Enable TQDM-compatible logging
    enable_tqdm_logging()

    logger.info("Running PhanDose separate_modalities script ...")

    # Initialize the LocalStorageHandler object :
    storage_handler = LocalStorageHandler(dir_storage=Path(dir_output))

    # Iterate over the list of patients :
    start_time = time.time()
    progress_bar = tqdm(total=len(list_patients), desc="Starting...", ncols=100)
    for patient_id in list_patients:

        try:
            # Create the Patient object, for the given patient ID, and the patient's DICOM directory :
            msg = f"Processing patient ID: {patient_id} ..."
            logger.info(msg), progress_bar.set_description(msg)
            patient = Patient.from_dir_dicom(patient_id=patient_id, dir_dicom=Path(dir_input) / patient_id)

            # Store the Patient object in the LocalStorageHandler :
            storage_handler.save_patient(patient=patient)

            # Log the success message :
            msg = f"patient ID {patient_id} successfully processed !"
            logger.info(msg), progress_bar.set_description(msg)
            time.sleep(1)

        except ValueError as e:
            # Remove the patient from the storage handler if an error occurs, and log the error message :
            msg = f"Failed to process patient ID : {patient_id} ! Error : {e}"
            tqdm.write(msg), logger.error(msg)
            time.sleep(2)

            storage_handler.delete_patient(patient_id=patient_id)

        # Update the progress bar
        progress_bar.update(1)

    progress_bar.close()
    logger.info("Completed the separate_modalities process in {:.2f} seconds.".format(time.time() - start_time))


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Separate DICOM modalities for a list of patients and store the results in the specified output directory"
            " according to the Phandose patient hub structure\n\n"
            "Notes:\n"
            "  - Either --patients or --patients_file must be provided, but not both.\n"
            "  - Ensure that the input directory contains subdirectories named after patient IDs.\n"
        ),

        epilog=(
            "Examples:\n"
            "  1. Process specific patients:\n"
            "     phandose_separate_modalities -i /data/dicom -o /data/output -p AGORL_P1 AGORL_P2 AGORL_P4\n\n"
            "  2. Process patients listed in a file:\n"
            "     phandose_separate_modalities -i /data/dicom -o /data/output -pf patients.txt\n\n"
            "  3. Enable verbose logging with INFO level:\n"
            "     phandose_separate_modalities -i /data/dicom -o /data/output -p 123 456 --verbose --log_level INFO\n"
        ),

        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--dir_input', required=True, type=str,
        help="**[Required]** Input directory containing the DICOM files. Each patient must have a dedicated subfolder."
    )

    parser.add_argument(
        '-o', '--dir_output', required=True, type=str,
        help="**[Required]** Output directory where processed patient data will be stored."
    )

    parser.add_argument(
        '-p', '--patients', required=False, type=str, nargs='+',
        help=(
            "List of patient IDs to process. Use this option to specify patient IDs directly. "
            "This is mutually exclusive with --patients_file."
        )
    )

    parser.add_argument(
        '-pf', '--patients_file', required=False, type=str,
        help=(
            "File containing the list of patient IDs to process. Each line should contain one patient ID. "
            "This option cannot be used with --patients."
        )
    )

    parser.add_argument(
        '--verbose', action='store_true',
        help="Enable verbose logging, including detailed per-run logging."
    )

    parser.add_argument(
        '--log_level', type=str, default="DEBUG",
        help="Logging level for the per-run log file. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL. Defaults to DEBUG."
    )

    parser.add_argument(
        '--dir_log', type=str, required=False,
        help="Directory to store per-run log files. Defaults to the value of --dir_output."
    )

    args = parser.parse_args()

    if not args.patients and not args.patients_file:
        raise ValueError("Please provide either a list of patient IDs or a file containing the list of patient IDs.")

    if args.patients and args.patients_file:
        raise ValueError("Please provide either a list of patient IDs or a file containing the list of patient IDs, "
                         "not both.")

    list_patients = args.patients or [line.strip() for line in open(args.patients_file, 'r').readlines()]

    separate_modalities(list_patients=list_patients,
                        dir_input=args.dir_input,
                        dir_output=args.dir_output,
                        verbose=args.verbose,
                        log_level=args.log_level,
                        dir_log=args.dir_log)


if __name__ == "__main__":
    main()
