from azure.storage.blob import BlockBlobService
import os
from app import appvar
from werkzeug.utils import secure_filename
import azure.storage.blob as azureblob
import azure.storage.blob.sharedaccesssignature as sasblob
from datetime import datetime, timedelta
import uuid

def save_image(request, filefield):

    blob_client = BlockBlobService(account_name = appvar.config["BLOB_ACCT_NAME"],account_key = appvar.config["BLOB_KEY"])
    
    filestorage = request.files.get(filefield)

    if filestorage is None:
        raise FileNotFoundError("File storage")

    if filestorage.filename == "":
        raise FileNotFoundError("File blank")
    
    file_name, ext = os.path.splitext(filestorage.filename)
    file_name_rand = file_name + str(uuid.uuid4()) + ext
    
    file_name_secure = secure_filename(file_name_rand)

    content = filestorage.read()
    blob_client.create_blob_from_bytes(container_name=appvar.config["BLOB_OCR_RAW_CONTAINER"], blob_name=file_name_secure, blob=content)
    
    return file_name_secure

def generate_img_url(blob_name):
    # Blob SAS Signature setup
    read_write = azureblob.models.BlobPermissions(read=True, add=True,create=True,write=True)

    sas_sig = sasblob.BlobSharedAccessSignature(
        account_name=appvar.config["BLOB_ACCT_NAME"],
        account_key=appvar.config["BLOB_KEY"]
    )

    sas_sig_param = sas_sig.generate_blob(
            container_name = appvar.config["BLOB_OCR_RAW_CONTAINER"],
            blob_name = blob_name, permission=read_write, 
            expiry=datetime.utcnow()+timedelta(0,60*30,0), 
            start=datetime.utcnow(), id=None
    )

    return "https://{}.blob.core.windows.net/{}/{}?{}".format(appvar.config["BLOB_OCR_RAW_CONTAINER"], appvar.config["BLOB_ACCT_NAME"], blob_name, sas_sig_param)
