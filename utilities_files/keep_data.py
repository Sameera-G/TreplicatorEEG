# settings.py

class KeepData:
    selected_role = None
    user_id = None

    @classmethod
    def set_selected_role(cls, role):
        cls.selected_role = role

    @classmethod
    def set_user_id(cls, user_id):
        cls.user_id = user_id

    def get_selected_role(self):
        return self.selected_role

    def get_user_id(self):
        return self.user_id