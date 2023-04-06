import json
import os

import requests
from google.cloud import storage


def get_ads_data(api_endpoint, headers):
    """
    Makes a GET request to the Microsoft Ads API and returns the response data as a Python dictionary.

    Args:
        api_endpoint (str): The URL endpoint for the API request.
        headers (dict): A dictionary containing the required authorization and content-type headers.

    Returns:
        dict: A dictionary containing the response data from the API request.
    """
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception("API request failed with status code " + str(response.status_code))


def upload_to_gcs(bucket_name, file_name, data):
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        bucket_name (str): The name of the bucket to upload the file to.
        file_name (str): The name of the file to create in the bucket.
        data (str): The data to write to the file.

    Returns:
        str: The GCS URI of the uploaded file.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(data)
    return f'gs://{bucket_name}/{file_name}'


if __name__ == '__main__':
    api_endpoint = "https://api.ads.microsoft.com/v13/accounts/{account_id}/campaigns"
    headers = {
        "Authorization": "Bearer {auth_token}".format(auth_token=os.getenv("AUTH_TOKEN")),
        "Content-Type": "application/json",
        "Customer-Id": os.getenv("CUSTOMER_ID")
    }

    ads_data = get_ads_data(api_endpoint, headers)
    print(ads_data)

    bucket_name = os.getenv("BUCKET_NAME")
    file_name = "ads_data.json"
    gcs_uri = upload_to_gcs(bucket_name, file_name, json.dumps(ads_data))
    print(f"Data uploaded to {gcs_uri}")
