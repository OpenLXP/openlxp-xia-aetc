import json
import logging
import os

import pandas as pd
import requests
from core.management.utils.preprocess import get_etca_bci, get_etca_bci_aetc

logger = logging.getLogger('dict_config_logger')


def extract_source():
    """Extracting raw metadata from tables"""
    logger.info('Extracting raw metadata from tables for further process')

    ETCA_BCI_df = get_etca_bci()
    ETCA_BCI_AETC_df = get_etca_bci_aetc()
    return ETCA_BCI_df


def read_source_file():
    """Sending source data in dataframe format"""
    logger.info("Retrieving data from XSR")
    # Function call to extract data from source repository
    source_df = extract_source()

    # # Changing null values to None for source dataframe
    std_source_df = source_df.where(pd.notnull(source_df), None)

    # std_source_df.to_csv('etca_bci.csv')
    # logger.debug("Sending source data in dataframe format for EVTVL")
    return std_source_df
