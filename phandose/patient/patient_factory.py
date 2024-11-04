from phandose.patient.patient import Patient
from phandose import utils

from pathlib import Path
import pydicom as dcm


def create_patient_from_dicom_directory(patient_id: str, dir_dicom: Path):

    # Initialize the patient object :
    patient = Patient(patient_id=patient_id)

    # Loop over all the DICOM files in the directory :
    for path_dicom in dir_dicom.rglob("*.dcm"):
        try:
            dicom_slice = dcm.read_file(str(path_dicom))
            modality_type = utils.get_modality_from_dicom_slice(dicom_slice)

            if modality_type in ['CT', 'PET']:
                modality_id = dicom_slice.SeriesInstanceUID
                kwargs = {}

            elif modality_type in ['RD', 'RP', 'RS']:
                modality_id = dicom_slice.SOPInstanceUID
                kwargs = {"RD": {"path_rtdose": path_dicom},
                          "RP": {"path_rtplan": path_dicom},
                          "RS": {"path_rtstruct": path_dicom}}[modality_type]

            else:
                raise ValueError(f"Unknown modality type {modality_type} !")

            series_description = dicom_slice.SeriesDescription

            # Add the modality to the patient object :
            patient.add_modality(modality_id=modality_id,
                                 modality_type=modality_type,
                                 dir_dicom=path_dicom.parent,
                                 series_description=series_description,
                                 **kwargs)

        except Exception as e:
            print(f"Error reading DICOM file {path_dicom} : {e}")

    return patient
