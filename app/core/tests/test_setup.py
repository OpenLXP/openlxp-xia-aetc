import pandas as pd
from django.test import TestCase


class TestSetUp(TestCase):
    """Class with setup and teardown for tests in XIS"""

    def setUp(self):
        """Function to set up necessary data for testing"""

        # globally accessible data sets

        self.source_metadata = {
            "Test": "0",
            "Test_id": "2146",
            "Test_url": "https://example.test.com/",
            "End_date": "9999-12-31T00:00:00-05:00",
            "test_name": "test name",
            "Start_date": "2017-03-28T00:00:00-04:00",
            "Course ID": "TestData 123",
            "SOURCESYSTEM": "AETC",
            "SUB_SOURCESYSTEM": "ETCA_BCI_AETC",
            "test_description": "test description",
        }

        self.key_value = "TestData 123_ETCA_BCI_AETC"
        self.key_value_hash = "cb16a5568d8d4f3f3be700015879b527"
        self.hash_value = "717e1b165457c1f2872eb232c02c63e9"

        self.test_data = {
            "key1": ["val1"],
            "key2": ["val2"],
            "key3": ["val3"]}
        self.test_data1 = {
            "key1": ["val1"],
            "key2": ["val2"],
            "key3": ["val3"]}

        self.metadata_df = pd.DataFrame.from_dict({1: self.source_metadata},
                                                  orient='index')

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
