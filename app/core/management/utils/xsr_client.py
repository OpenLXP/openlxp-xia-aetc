import json
import logging
import os
from core.management.utils.preprocess import get_etca_bci, get_paragraph_data
import pandas as pd
import requests

logger = logging.getLogger('dict_config_logger')


def get_xsr_api_endpoint():
    """Setting API endpoint from XIA and XIS communication """
    xsr_endpoint = os.environ.get('XSR_API_ENDPOINT')
    return xsr_endpoint


def token_generation_for_api_endpoint():
    """Function connects to edX domain using client id and secret and returns
    the access token"""

    payload = "grant_type=client_credentials&client_id=" + os.environ.get(
        'EDX_CLIENT_ID') + "&client_secret=" + os.environ.get(
        'EDX_CLIENT_SECRET') + "&token_type=JWT"
    headers = {'content-type': "application/x-www-form-urlencoded"}
    xis_response = requests.post(url=os.environ.get('TOKEN_URL'),
                                 data=payload, headers=headers)
    data = xis_response.json()
    return data['access_token']


def get_xsr_api_response():
    """Function to get api response from xsr endpoint"""
    url = get_xsr_api_endpoint()
    # creating HTTP response object from given url
    headers = {'Authorization': 'JWT '+token_generation_for_api_endpoint()}
    resp = requests.get(url, headers=headers, )
    return resp


def extract_source():
    get_paragraph_data()

def read_source_file():
    """Sending source data in dataframe format"""
    logger.info("Retrieving data from XSR")

    # Function call to extract data from source repository
    xsr_items = extract_source()

    # convert xsr dictionary list to Dataframe
    # source_df = pd.DataFrame(xsr_items)
    #
    # # Changing null values to None for source dataframe
    # std_source_df = source_df.where(pd.notnull(source_df),
    #                                 None)
    # logger.debug("Sending source data in dataframe format for EVTVL")
    # return std_source_df
