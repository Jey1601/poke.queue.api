import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

class ABlob:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        self.container_client = self.blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)

    def generate_sas(self, id: int):
        blob_name = f"poke_report_{id}.csv"
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=AZURE_STORAGE_CONTAINER,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        return sas_token
    
    def delete_blob(self, id: int) -> dict:
        blob_name = f"poke_report_{id}.csv"

        try:
            blob_client = self.blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
            blob_client.delete_blob()
            return {
                "success": True,
                "message": f"Blob '{blob_name}' eliminado correctamente."
            }

        except ResourceNotFoundError:
            return {
                "success": False,
                "message": f" El blob '{blob_name}' no existe."
            }

        except HttpResponseError   as e:
            return {
                "success": False,
                "message": f"Error de Azure al eliminar el blob '{blob_name}': {str(e)}"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f" Error inesperado al eliminar el blob '{blob_name}': {str(e)}"
            }
