# the unauth controller for the crypto system
# This class handles the unauthenticated requests
# Example:
#  - register

# import the unauth model
from user_model import UserModel


class UnauthController:

    # the user model
    user_model = None

    def __init__(self):
        """
        this is the constructor of the UnauthController class
        """
        self.user_model = UserModel()

    def register(self, username, public_key):
        """
        this method registers a user
        """
        # create a record
        record = {
            "username": username,
            "public_key": public_key
        }
        response = self.user_model.insert_record(record)
        # if the response is -1
        if response == -1:
            return {
                "message": "user already exists",
            }
        # if the response is not -1
        else:
            return {
                "message": "user registered successfully",
                "user": record
            }
