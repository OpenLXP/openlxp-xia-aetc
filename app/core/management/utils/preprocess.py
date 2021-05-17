import logging
import boto3
import pandas as pd
import io

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


def get_etca_bci():
    """ Extracting raw metadata from tables for further process"""
    table_data = get_aws_details()
    # Ingesting as dataframe values
    ETCA_BCI_df = pd.read_excel(io.BytesIO(table_data), sheet_name='ETCA_BCI',
                                engine='openpyxl')

    # Getting rows only when organization is AETC
    ETCA_BCI_df = ETCA_BCI_df[ETCA_BCI_df['Organization'] == 'AETC']

    # Getting null and not null dataframes
    ETCA_BCI_df_is_null = ETCA_BCI_df[ETCA_BCI_df["BCI_ID"].isnull()]
    ETCA_BCI_df_not_null = ETCA_BCI_df[ETCA_BCI_df["BCI_ID"].notnull()]

    # Setting up index to 'BCI_ID'
    ETCA_BCI_df_not_null = ETCA_BCI_df_not_null.set_index('BCI_ID')

    # Converting both dataframe into json
    ETCA_BCI_df_is_null_dict = ETCA_BCI_df_is_null.to_dict(orient='index')
    ETCA_BCI_df_not_null_dict = ETCA_BCI_df_not_null.to_dict(orient='index')

    # print(ETCA_BCI_df_not_null_dict)

    return ETCA_BCI_df_not_null_dict


def get_paragraph_data():
    table_data = get_aws_details()
    ETCA_BCI_df_not_null_dict = get_etca_bci()
    ETCA_Course_Paragraph_df = pd.read_excel(io.BytesIO(table_data),
                                             sheet_name='ETCA_Course_Paragraph',
                                             engine='openpyxl',
                                             usecols=['BCI_ID',
                                                      'Paragraph_Heading',
                                                      'Paragraph_Text'])
    dict_ETCA_BCI = ETCA_Course_Paragraph_df.to_dict(orient='index')
    logger.info(ETCA_Course_Paragraph_df)
    #
    # for i in ETCA_BCI_df_not_null_dict:
    #     print(ETCA_BCI_df_not_null_dict(14223.0))
    for index, row in ETCA_Course_Paragraph_df.iterrows():
        key =float(row['BCI_ID'])
        #print(type(key))
        print((ETCA_BCI_df_not_null_dict[key]))
        temp_dict = {row['Paragraph_Heading']: row['Paragraph_Text']}
