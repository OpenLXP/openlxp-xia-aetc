import logging
import boto3
import pandas as pd
import io

from django.core.management.base import BaseCommand

logger = logging.getLogger('dict_config_logger')


class Command(BaseCommand):
    """Django command to extract raw metadata and process to further
    extraction in EVTVL process"""

    def handle(self, *args, **options):
        """ Extracting raw metadata from tables for further process"""

        # get object and file (key) from bucket
        bucket = 'xsraetc'
        file_name = 'AFCS_ETCA_Data.xlsx'
        client = boto3.client('s3')
        csv_obj = client.get_object(Bucket=bucket, Key=file_name)
        table_data = csv_obj['Body'].read()
        # Ingesting as dataframe values
        ETCA_BCI_df = pd.read_excel(io.BytesIO(table_data), sheet_name='ETCA_BCI', engine='openpyxl')
        ETCA_BCI_AETC_df = pd.read_excel(io.BytesIO(table_data), sheet_name='ETCA_BCI_AETC', engine='openpyxl')
        # ETCA_BCI_AETC_df.to_csv('file_name.csv')


