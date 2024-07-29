from phandose.modalities import Modality

import unittest


class ExampleModality(Modality):
    """
    A concrete implementation of the abstract Modality class for testing purposes.
    """

    def set_series_description(self):
        """
        Sets the series description for a test value.
        """

        self._series_description = "Test Series Description"

    def dicom(self):
        """
        Returns a test string representing the DICOM format for testing purposes.
        """

        return "DICOM format"

    def nifti(self):
        """
        Returns a test string representing the NIfTI format for testing purposes.
        """

        return "NIfTI format"


class TestModalityModule(unittest.TestCase):
    """
    Unit test class for test the Modality abstract class and an example of a concrete implementation.
    """

    def setUp(self):
        """
        Sets up the test case with a test modality, and initial values for the Series Instance UID, Series Description,
        and modality type.
        """

        self.series_instance_uid = '1.2.840.10008.1.2.3.4'
        self.series_description = 'Test Description'
        self.modality = 'example'
        self.test_modality = ExampleModality(self.series_instance_uid, self.series_description, self.modality)

    def test_series_instance_uid(self):
        """
        Tests that the Series Instance UID is set correctly.
        """

        self.assertEqual(self.test_modality.series_instance_uid, self.series_instance_uid)

    def test_series_description_with_series_description_provided(self):
        """
        Tests that the Series Description is set correctly, when a Series Description is provided.
        """

        self.assertEqual(self.test_modality.series_description, self.series_description)

    def test_series_description_when_no_series_description_provided(self):
        """
        Tests that the Series Description is set correctly, when a Series Description is not provided
        """

        test_modality_no_description = ExampleModality(self.series_instance_uid)
        self.assertEqual(test_modality_no_description.series_description, "Test Series Description")

    def test_modality(self):
        """
        Tests that the modality is set correctly.
        """

        self.assertEqual(self.test_modality.modality, self.modality)

    def test_dicom(self):
        """
        Test that the dicom method returns the correct data.
        """

        self.assertEqual(self.test_modality.dicom(), "DICOM format")

    def test_nifti(self):
        """
        Test that the nifti method returns the correct data.
        """

        self.assertEqual(self.test_modality.nifti(), "NIfTI format")


if __name__ == '__main__':
    unittest.main()
