import firebase_admin
from firebase_admin import credentials, firestore

class Firebase:
    def __init__(self):
        cred = credentials.Certificate("firebase/bci-research-77b3d-02a9edb61fd4.json") # Replace with your service account key path
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_data(self, user_id, data):
        doc_ref = self.db.collection(u'users').document(user_id)
        doc_ref.set(data)

    def update_data(self, user_id, data):
        doc_ref = self.db.collection(u'users').document(user_id)
        doc_ref.update(data)
