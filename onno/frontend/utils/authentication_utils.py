import bcrypt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from onno.frontend.constants.keys import path_to_firebase_credentials

# Initialize Firestore
if not firebase_admin._apps:
    cred = credentials.Certificate(path_to_firebase_credentials)
    firebase_admin.initialize_app(cred)
db = firestore.client()

def save_user_info(username: str, user_info: dict):
    doc_ref = db.collection('users').document(username)
    doc_ref.set(user_info)

def get_password(username: str) -> str:
    doc_ref = db.collection('users').document(username)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()['password']
    else:
        return None

def check_username_exists(username: str) -> bool:
    doc_ref = db.collection('users').document(username)
    doc = doc_ref.get()
    return doc.exists

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())