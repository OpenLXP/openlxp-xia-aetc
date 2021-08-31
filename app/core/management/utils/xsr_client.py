import hashlib
import io
import logging
import os

import boto3
import pandas as pd
from openlxp_xia.management.utils.xia_internal import get_key_dict

logger = logging.getLogger('dict_config_logger')


def get_aws_details():
    """Get table data from the s3 bucket"""

    # get object and file (key) from bucket
    bucket = os.environ.get('BUCKET_NAME')
    file_name = 'AFCS_ETCA_Data.xlsx'
    client = boto3.client('s3')
    csv_obj = client.get_object(Bucket=bucket, Key=file_name)
    table_data = csv_obj['Body'].read()
    return table_data


def get_list_table_names():
    """Function to return table names for preprocessing extraction"""

    table_list = ['ETCA_Course_Paragraph', 'ETCA_Course_Paragraph_711HPW',
                  'ETCA_Course_Paragraph_ACC', 'ETCA_Course_Paragraph_AETC',
                  'ETCA_Course_Paragraph_AETC2', 'ETCA_Course_Paragraph_AETC3',
                  'ETCA_Course_Paragraph_AETC4', 'ETCA_Course_Paragraph_AFIT',
                  'ETCA_Course_Paragraph_AFSOC', 'ETCA_Course_Paragraph_ANG',
                  'ETCA_Course_Paragraph_AU', 'ETCA_Course_Paragraph_FT',
                  'ETCA_Course_Paragraph_LT1K', 'ETCA_Course_Paragraph_Org_1K',
                  'ETCA_Course_Paragraph_SAFIG',
                  'ETCA_Course_Paragraph_USAFEC']

    return table_list


def get_etca_bci():
    """ Extracting raw metadata from tables for further process"""

    # Get table data from the s3 bucket
    table_data = get_aws_details()

    # Ingesting as dataframe values
    etca_bci_df = pd.read_excel(io.BytesIO(table_data), sheet_name='ETCA_BCI',
                                engine='openpyxl')

    # Adding fields from tables to core table to enrich data
    etca_bci_df = get_paragraph_data(etca_bci_df)

    # Adding Resp_Org_ID to metadata
    etca_bci_df['SUB_SOURCESYSTEM'] = 'ETCA_BCI'

    return etca_bci_df


def get_etca_bci_aetc():
    """ Extracting raw metadata from tables for further process"""

    # Get table data from the s3 bucket
    table_data = get_aws_details()

    # Ingesting as dataframe values
    etca_bci_aetc_df = pd.read_excel(io.BytesIO(table_data),
                                     sheet_name='ETCA_BCI_AETC',
                                     engine='openpyxl')

    # Adding fields from tables to core table to enrich data
    etca_bci_aetc_df = get_paragraph_data(etca_bci_aetc_df)

    # Adding Resp_Org_ID to metadata
    etca_bci_aetc_df['SUB_SOURCESYSTEM'] = 'ETCA_BCI_AETC'

    return etca_bci_aetc_df


def get_paragraph_data(core_table_df):
    """Adding fields from tables to enrich data in core tables"""

    # Get table data from the s3 bucket
    table_data = get_aws_details()

    # Making a list of paragraph tables sheet names
    table_list = get_list_table_names()
    for table_name in table_list:
        etca_course_paragraph_df = pd.read_excel(io.BytesIO(table_data),
                                                 sheet_name=table_name,
                                                 engine='openpyxl',
                                                 usecols=['BCI_ID',
                                                          'Paragraph_Heading',
                                                          'Paragraph_Text'])
        #  Retrieving rows from Dataframe with BCI_ID
        etca_course_paragraph_df = etca_course_paragraph_df[
            etca_course_paragraph_df["BCI_ID"].notnull()]

        # Iterating over rows in Tables to find fields to add to the core table
        for index, row in etca_course_paragraph_df.iterrows():
            # Finding index for row in core table to be updated
            index_val = core_table_df.index[core_table_df['BCI_ID'] ==
                                            row['BCI_ID']]
            # Adding updated to row with new field data
            core_table_df.loc[core_table_df.index[index_val],
                              row['Paragraph_Heading']] = row['Paragraph_Text']

    return core_table_df


def read_source_file():
    """Sending source data in dataframe format"""
    logger.info("Retrieving data from XSR for Extraction")

    # Function call to extract data from source repository
    etca_bci_df = get_etca_bci()
    etca_bci_aetc_df = get_etca_bci_aetc()

    #  Creating list of dataframes of sources
    source_list = [etca_bci_df, etca_bci_aetc_df]

    logger.debug("Sending source data in dataframe format for EVTVL")

    return source_list


def get_source_metadata_key_value(data_dict):
    """Function to create key value for source metadata """
    # field names depend on source data and SOURCESYSTEM is system generated
    field = ['Course ID', 'SUB_SOURCESYSTEM']
    field_values = []

    for item in field:
        if not data_dict.get(item):
            logger.error('Field name ' + item + ' is missing for '
                                                'key creation')
            return None
        field_values.append(data_dict.get(item))

    # Key value creation for source metadata
    key_value = '_'.join(field_values)

    # Key value hash creation for source metadata
    key_value_hash = hashlib.md5(key_value.encode('utf-8')).hexdigest()

    # Key dictionary creation for source metadata
    key = get_key_dict(key_value, key_value_hash)

    return key
