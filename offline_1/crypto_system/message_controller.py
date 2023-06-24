# controller layer of the message system


# the message controller of the crypto system

from message_model import MessageModel
from user_model import UserModel


class MessageController:

    # model
    message_model = None
    user_model = None

    def __init__(self):
        """
        this is the constructor of the MessageController class
        """
        self.message_model = MessageModel()
        self.user_model = UserModel()

    def get_all_messages(self):
        """
        this method returns all messages
        """
        # get the messages
        messages = self.message_model.read_csv()
        return messages

    def get_user_message(self, username):
        """
        this method returns a message
        """
        # ensure that the user exists
        user = self.user_model.get_record_by_username(username)
        if user == -1:
            return {
                "message": "user does not exist"
            }

        # get the messages
        messages = self.message_model.get_record_by_sender_or_receiver(
            username, username)
        return messages

    def send_message(self, sender, receiver, message):
        """
        this method sends a message
        """
        # check if both sender and receiver exist
        sender = self.user_model.get_record_by_username(sender)
        receiver = self.user_model.get_record_by_username(receiver)

        if sender == -1 or receiver == -1:
            return {
                "message": "sender or receiver does not exist",
            }

        # create the message
        message = {
            "sender": sender["username"],
            "receiver": receiver["username"],
            "message": message
        }

        # add the message to the message database
        self.message_model.insert_record(message)

        # return the response
        return {
            "message": "message sent successfully",
            "record": message
        }
