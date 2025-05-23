import firebase_admin
from firebase_admin import credentials, firestore

class Firebase:
    def __init__(self):
        cred = credentials.Certificate("firebase/bci-research-77b3d-02a9edb61fd4.json") # Replace with your service account key path
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_data(self, selected_role, user_id, data):
        doc_ref = self.db.collection(selected_role).document(user_id)
        doc_ref.set(data)

    def update_data(self, selected_role, user_id, data):
        doc_ref = self.db.collection(selected_role).document(user_id)
        doc_ref.update(data)

    def add_time_data(self, selected_role, user_id, time_data):
        times_collection_path = f"{selected_role}/{user_id}/times"
        doc_ref = self.db.collection(times_collection_path).document(user_id)  # Set doc ID to user_id
        doc_ref.set(time_data, merge=True)  # Merge to avoid overwriting existing data

    def get_latest_user_id(self, selected_role, user_id):
        # Query Firestore for the documents in the specified collection
        docs = self.db.collection(selected_role).order_by(user_id, direction=firestore.Query.DESCENDING).limit(1).get()
        # Check if any documents exist
        if not docs:
            return None  # If no documents found, return None
        # Iterate over the documents and retrieve the user_id field
        for doc in docs:
            user_id = doc.id  # Use doc.id to get the document ID
            return user_id
        # If no documents found, return None
        return None

    def retrieve_data(self, selected_role, user_id):
        doc_ref = self.db.collection(selected_role).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"No such document with user_id: {user_id} in collection {selected_role}.")
            return None