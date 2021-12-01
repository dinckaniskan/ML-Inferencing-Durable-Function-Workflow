# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

import uuid
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from azure.storage.blob import (        
    generate_blob_sas,
    BlobSasPermissions
)

from datetime import datetime, timedelta
import base64

# # IMPORTANT: Replace connection string with your storage account connection string
# # Usually starts with DefaultEndpointsProtocol=https;...
# BLOB_CONNECTION_STRING = "REPLACE_THIS"
 
# # Replace with blob container. This should be already created in azure storage.
# IMAGE_CONTAINER = "myimages"
 
# # Replace with the local folder which contains the image files for upload
# LOCAL_IMAGE_PATH = "REPLACE_THIS"

STORAGE_ACCOUNT_NAME = os.environ.get('STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.environ.get('STORAGE_ACCOUNT_KEY')

class AzureBlobFileUploader:
    def __init__(self):
        print("Intializing AzureBlobFileUploader")
    
        # Initialize the connection to Azure storage account
        self.blob_service_client =  BlobServiceClient.from_connection_string(f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net",)        
    

    def generateSasUrl(self, blob):

        sas_token = generate_blob_sas(account_name=os.environ.get('STORAGE_ACCOUNT_NAME'),
                                        container_name=os.environ.get('IMAGE_CONTAINER'),
                                        blob_name=blob,
                                        account_key=os.environ.get('STORAGE_ACCOUNT_KEY'),
                                        permission=BlobSasPermissions(read=True),
                                        expiry=datetime.utcnow() + timedelta(hours=1))
        

        return f"https://{os.environ.get('STORAGE_ACCOUNT_NAME')}.blob.core.windows.net/{os.environ.get('IMAGE_CONTAINER')}/{blob}?{sas_token}"


    def upload_image(self, image):
        
        image_guid = uuid.uuid4()
        file_name = f'{image_guid}.jpg'

        # Create blob with same name as local file name
        blob_client = self.blob_service_client.get_blob_client(container=os.environ.get('IMAGE_CONTAINER'), blob=file_name)
        
        # Create blob on storage    
        content_settings = ContentSettings(content_type='image/jpeg')
                
        logging.info(f"Saved file to blobstorage as {image_guid}.jpg")

        blob_client.upload_blob(image, blob_type="BlockBlob", overwrite=True, content_settings=content_settings)
        sas_url = self.generateSasUrl(file_name)
        
        return sas_url
 

def main(payload: str) -> str:
    image_bytes = base64.b64decode(payload['image'])

    # Initialize class and upload file
    result = AzureBlobFileUploader().upload_image(image_bytes)
        

    return f"{result}"
