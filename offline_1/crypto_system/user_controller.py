# the user controller of the crypto system

from user_model import UserModel


class UserController:

    # the user model
    user_model = None

    def __init__(self):
        """
        this is the constructor of the UserController class
        """
        self.user_model = UserModel()

    def get_user(self, username):
        """
        this method returns a user
        """

        # get the user
        user = self.user_model.get_record_by_username(username)
        if user == -1:
            return {
                "message": "user does not exist",
            }
        else:
            return user

    def get_all_users(self):
        """
        this method returns all users
        """
        # get the users
        users = self.user_model.read_csv()
        return users
