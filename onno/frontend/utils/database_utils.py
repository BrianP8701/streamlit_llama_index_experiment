import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from onno.frontend.constants.keys import path_to_firebase_credentials, path_to_onno_gcp_service_account_credentials
from google.cloud import storage
from google.oauth2 import service_account


if not firebase_admin._apps:
    cred = credentials.Certificate(path_to_firebase_credentials)
    firebase_admin.initialize_app(cred)
db = firestore.client()

def get_client():
    creds = service_account.Credentials.from_service_account_file(path_to_onno_gcp_service_account_credentials)
    storage_client = storage.Client(credentials=creds)
    return storage_client

def get_bucket():
    storage_client = get_client()
    bucket = storage_client.bucket('onno')
    return bucket

def save_user_info(username: str, user_info: dict):
    doc_ref = db.collection('users').document(username)
    doc_ref.set(user_info)
    
def retrieve_user_info(username: str) -> dict:
    doc_ref = db.collection('users').document(username)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
        
def download_blob(source_blob_name):
    bucket = get_bucket()
    blob = bucket.blob(source_blob_name)
    return blob
    
def create_folder(folder_path):
    if not folder_path.endswith('/'):
        folder_path += '/'
    bucket = get_bucket()
    blob = bucket.blob(folder_path)
    blob.upload_from_string('')
    
def save_uploaded_file_to_gcs(uploaded_file, destination_blob_name):
    bucket = get_bucket()
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(uploaded_file, content_type=uploaded_file.type)
    
def does_file_exists_in_gcs(blob_name):
    bucket = get_bucket()
    blob = bucket.blob(blob_name)
    return blob.exists()

def save_string_to_gcs(string_data, destination_blob_name):
    bucket = get_bucket()
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(string_data, content_type='text/plain')