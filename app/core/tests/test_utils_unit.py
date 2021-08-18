import hashlib
import logging
from unittest.mock import patch

import pandas as pd
from ddt import data, ddt, unpack
from django.test import tag

from core.management.utils.xsr_client import (get_list_table_names,
                                              get_source_metadata_key_value,
                                              read_source_file)

from .test_setup import TestSetUp

logger = logging.getLogger('dict_config_logger')


@tag('unit')
@ddt
class UtilsTests(TestSetUp):
    """Unit Test cases for utils """

    # Test cases for XSR_CLIENT

    def test_read_source_file(self):
        """test to check if data is present for extraction """
        with patch('core.management.utils.xsr_client.get_etca_bci',
                   return_value=pd.DataFrame.from_dict(self.test_data)), \
                patch('core.management.utils.xsr_client.get_etca_bci_aetc',
                      return_value=pd.DataFrame.from_dict(self.test_data1)):
            result_data = read_source_file()
            self.assertIsInstance(result_data, list)

    def test_get_list_table_names(self):
        """test Function to return table names for preprocessing extraction """
        table_list = get_list_table_names()
        self.assertTrue(table_list)

    @data(('key_field1', 'key_field2'), ('key_field11', 'key_field22'))
    @unpack
    def test_get_source_metadata_key_value(self, first_value, second_value):
        """Test key dictionary creation for source"""
        test_dict = {
            'Course ID': first_value,
            'SUB_SOURCESYSTEM': second_value
        }

        expected_key = first_value + '_' + second_value
        expected_key_hash = hashlib.md5(expected_key.encode('utf-8')). \
            hexdigest()

        result_key_dict = get_source_metadata_key_value(test_dict)
        self.assertEqual(result_key_dict['key_value'], expected_key)
        self.assertEqual(result_key_dict['key_value_hash'], expected_key_hash)
