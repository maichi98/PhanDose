from .patient_builder import PatientBuilder
from .patient import Patient
from phandose import utils

from pathlib import Path
import pydicom as dcm


class PatientDirector:
    """
    Director class to construct a Patient object using the PatientBuilder.

    """

    def __init__(self, builder: PatientBuilder):
        """
        Initialize the PatientDirector with a PatientBuilder

        Parameters:
        -----------
        builder : (PatientBuilder)
        The builder instance to use to construct the Patient object.

        """

        self._builder = builder

    def construct_patient_from_dicom_directory(self,
                                               patient_id: str,
                                               dir_dicom: Path):
        """
        Construct a Patient object from a patient's DICOM directory.

        Parameters:
        -----------
        patient_id : (str)
            Patient ID.

        dir_dicom : (Path)
            The patient's directory containing all the DICOM files.

        Returns:
        --------
        Patient
            The constructed Patient object.

        """

        self._builder.set_patient_id(patient_id)

        for path_dicom in dir_dicom.rglob("*.dcm"):
            try:
                dicom_slice = dcm.read_file(str(path_dicom))
                modality_type = utils.get_modality_from_dicom_slice(dicom_slice)

                if modality_type in ['CT', 'PET']:
                    modality_id = dicom_slice.SeriesInstanceUID

                elif modality_type in ['RD', 'RP', 'RS']:
                    modality_id = dicom_slice.SeriesInstanceUID

                else:
                    raise ValueError(f"Unknown modality type {modality_type} !")

                series_description = dicom_slice.SeriesDescription

                self._builder.add_modality(modality_id=modality_id,
                                           modality_type=modality_type,
                                           dir_dicom=dir_dicom,
                                           series_description=series_description)
            except Exception as e:
                print(f"Error reading DICOM file {path_dicom} : {e}")

        return self._builder.build()

    def construct_patient_from_separate_modality_directories(self,
                                                             patient_id: str,
                                                             dir_ct: Path,
                                                             path_rtdose: Path,
                                                             path_rtplan: Path,
                                                             path_rtstruct: Path) -> Patient:
        """
        Construct a Patient object from separate directories for each modality.

        Parameters:
        -----------
        patient_id: (str)
            Patient ID.

        dir_ct: (Path)
            The directory containing the CT DICOM files.

        path_rtdose: (Path)
            The path to the RTDOSE DICOM file.

        path_rtplan: (Path)
            The path to the RTPLAN DICOM file.

        path_rtstruct: (Path)
            The path to the RTSTRUCT DICOM file.

        Returns:
        --------
        Patient
            The constructed Patient object.

        """

        self._builder.set_patient_id(patient_id)

        # Add the CT modality :
        ct_uid = utils.get_series_instance_uid_from_directory(dir_ct)
        self._builder.add_modality(modality_id=ct_uid, modality_type='CT', dir_dicom=dir_ct)

        # Add the Rtdose modality :
        rtdose_uid = dcm.dcmread(str(path_rtdose)).SeriesInstanceUID
        self._builder.add_modality(modality_id=rtdose_uid, modality_type='RD', dir_dicom=None, path_rtdose=path_rtdose)

        # Add the Rtplan modality :
        rtplan_uid = dcm.dcmread(str(path_rtplan)).SeriesInstanceUID
        self._builder.add_modality(modality_id=rtplan_uid, modality_type='RP', dir_dicom=None, path_rtplan=path_rtplan)

        # Add the Rtstruct modality :
        rtstruct_uid = dcm.dcmread(str(path_rtstruct)).SeriesInstanceUID
        self._builder.add_modality(modality_id=rtstruct_uid, modality_type='RS',
                                   dir_dicom=None, path_rtstruct=path_rtstruct)

        self._builder.build()
