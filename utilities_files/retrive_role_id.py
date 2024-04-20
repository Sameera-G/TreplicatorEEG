import json
class RetriveRoleId:
    def retrieve_data(self):
        """Retrieves user data from a temporary file."""
        try:
            with open("user_data.tmp", "r") as file:
                data = json.load(file)
            return data["selected_role"], data["user_id"]
        except FileNotFoundError:
            print("Error: User data file not found.")
            return None, None