class KeepData:
    def __init__(self):
        self.selected_role = None
        self.user_id = None
    
    def set_data(self, selected_role, user_id):
        self.selected_role = selected_role
        self.user_id = user_id

    def get_data(self):
        return {'selected_role': self.selected_role, 'user_id': self.user_id}
