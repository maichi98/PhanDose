from phandose.modalities import Modality


class Patient:
    """
    Class that represents a patient.

    Attributes:
    -----------
    patient_id : (str)
        Patient ID.

    dict_modalities : (dict[str: Modality])
        Dictionary containing the modalities of the patient.

    Methods:
    --------
    add_modality(modality)
        Add a modality to the patient.

    remove_modality(series_instance_uid)
        Remove a modality from the patient.

    get_modality(series_instance_uid)
        Get a modality from the patient.

    """

    def __init__(self,
                 patient_id: str,
                 list_modalities: list[Modality] = None):
        """
        Constructor of the class Patient.

        Parameters:
        -----------
        patient_id : (str)
            Patient ID.

        list_modalities : (list[Modality]), optional
            List of modalities of the patient.

        """

        self._patient_id = patient_id
        self._dict_modalities = {modality.series_instance_uid: modality
                                 for modality in list_modalities} if list_modalities is not None else {}

    @property
    def patient_id(self):
        """
        Getter method for the Patient ID.

        """
        return self._patient_id

    @property
    def dict_modalities(self):
        """
        Getter method for the Dictionary containing the modalities of the patient.

        """
        return self._dict_modalities

    def add_modality(self, modality: Modality):
        """
        Add a modality to the patient.

        Parameters:
        -----------
        modality : (Modality)
            Modality to be added to the patient.

        """
        self._dict_modalities[modality.series_instance_uid] = modality

    def remove_modality(self, series_instance_uid: str):
        """
        Remove a modality from the patient.

        Parameters:
        -----------
        series_instance_uid : (str)
            Series Instance UID.

        """
        self._dict_modalities.pop(series_instance_uid)

    def get_modality(self, series_instance_uid: str):
        """
        Get a modality from the patient.

        Parameters:
        -----------
        series_instance_uid : (str)
            Series Instance UID.

        """

        return self._dict_modalities.get(series_instance_uid)
