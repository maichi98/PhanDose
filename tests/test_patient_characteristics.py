from phandose.patient_characteristics import get_patient_characteristics
from pathlib import Path
import pandas as pd
import unittest


class TestPatientCharacteristics(unittest.TestCase):

    def setUp(self):

        path_patient = Path(__file__).parent.parent / "sample_data" / "AGORL_P33"
        self.list_path_imaging = [path_patient / "CT_TO_TOTALSEGMENTATOR", path_patient / "PET_TO_TOTALSEGMENTATOR"]

    def test_patient_characteristics_dataframe_creation(self):

        df_patient_data = get_patient_characteristics(*self.list_path_imaging)
        self.assertIsInstance(df_patient_data, pd.DataFrame)
        self.assertIn('PatientID', df_patient_data.columns)
        self.assertIn('CodeMeaning', df_patient_data.columns)


if __name__ == '__main__':
    unittest.main()
