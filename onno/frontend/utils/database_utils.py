import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
from google.oauth2 import service_account
import json
import bcrypt

class Database:
    def __init__(self, firebase_key, gcp_service_account_credentials):
        # Initialize Firebase Admin
        firebase_creds_dict = json.loads(firebase_key)
        firebase_creds = credentials.Certificate(firebase_creds_dict)
        if not firebase_admin._apps:
            firebase_app = firebase_admin.initialize_app(firebase_creds)
        else:
            firebase_app = firebase_admin.get_app()
        self.db = firestore.client(app=firebase_app)
        
        # Initialize Google Cloud Storage
        gcs_creds_dict = json.loads(gcp_service_account_credentials)
        gcs_creds = service_account.Credentials.from_service_account_info(gcs_creds_dict)
        storage_client = storage.Client(credentials=gcs_creds)
        self.client = storage_client
        self.bucket = self.client.bucket('onno')

    def save_user_info(self, username: str, user_info: dict):
        doc_ref = self.db.collection('users').document(username)
        doc_ref.set(user_info)
        
    def retrieve_user_info(self, username: str) -> dict:
        doc_ref = self.db.collection('users').document(username)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
            
    def download_blob(self, source_blob_name):
        blob = self.bucket.blob(source_blob_name)
        return blob
        
    def create_folder(self, folder_path):
        if not folder_path.endswith('/'):
            folder_path += '/'
        blob = self.bucket.blob(folder_path)
        blob.upload_from_string('')
        
    def save_uploaded_file_to_gcs(self, uploaded_file, destination_blob_name):
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_file(uploaded_file, content_type=uploaded_file.type)
        
    def does_file_exists_in_gcs(self, blob_name):
        blob = self.bucket.blob(blob_name)
        return blob.exists()

    def save_string_to_gcs(self, string_data, destination_blob_name):
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_string(string_data, content_type='text/plain')

    def get_password(self, username: str) -> str:
        doc_ref = self.db.collection('users').document(username)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()['password']
        else:
            return None

    def check_username_exists(self, username: str) -> bool:
        doc_ref = self.db.collection('users').document(username)
        doc = doc_ref.get()
        return doc.exists

    def hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()

    def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())