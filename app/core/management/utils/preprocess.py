import logging
import boto3
import pandas as pd
import io
import numpy as np
from django.core.management.base import BaseCommand

logger = logging.getLogger('dict_config_logger')


def get_aws_details():
    """Get table data from the s3 bucket"""
    # get object and file (key) from bucket
    bucket = 'xsraetc'
    file_name = 'AFCS_ETCA_Data.xlsx'
    client = boto3.client('s3')
    csv_obj = client.get_object(Bucket=bucket, Key=file_name)
    table_data = csv_obj['Body'].read()
    return table_data


def get_list_table_names():
    """Function to return table names"""
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
    table_data = get_aws_details()
    # Ingesting as dataframe values
    ETCA_BCI_df = pd.read_excel(io.BytesIO(table_data), sheet_name='ETCA_BCI',
                                engine='openpyxl')

    ETCA_BCI_df = get_paragraph_data(ETCA_BCI_df)
    ETCA_BCI_df['Resp_Org_ID'] = 'ETCA_BCI'
    return ETCA_BCI_df
    # df.to_csv('etca_bci.csv')


def get_etca_bci_aetc():
    """ Extracting raw metadata from tables for further process"""
    table_data = get_aws_details()
    # Ingesting as dataframe values
    ETCA_BCI_AETC_df = pd.read_excel(io.BytesIO(table_data),
                                     sheet_name='ETCA_BCI_AETC',
                                     engine='openpyxl')
    ETCA_BCI_AETC_df = get_paragraph_data(ETCA_BCI_AETC_df)
    ETCA_BCI_AETC_df['Resp_Org_ID'] = 'ETCA_BCI_AETC'
    return ETCA_BCI_AETC_df
    # df.to_csv('etca_bci_aetc.csv')


def get_paragraph_data(core_table_df):
    table_data = get_aws_details()
    # Making a list of paragraph tables sheet names
    table_list = get_list_table_names()
    for table_name in table_list:
        ETCA_Course_Paragraph_df = pd.read_excel(io.BytesIO(table_data),
                                                 sheet_name=table_name,
                                                 engine='openpyxl',
                                                 usecols=['BCI_ID',
                                                          'Paragraph_Heading',
                                                          'Paragraph_Text'])
        ETCA_Course_Paragraph_df = ETCA_Course_Paragraph_df[
            ETCA_Course_Paragraph_df["BCI_ID"].notnull()]
        for index, row in ETCA_Course_Paragraph_df.iterrows():
            val = core_table_df.index[core_table_df['BCI_ID'] == row['BCI_ID']]
            core_table_df.loc[core_table_df.index[val],
                              row['Paragraph_Heading']] = row['Paragraph_Text']
    return core_table_df
    # core_table_df.to_csv('filename.csv')
