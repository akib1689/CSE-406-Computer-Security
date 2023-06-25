# file to connect to the server to send a message

# steps:
# 1. connect to the server
# 2. query the p, g parameters and minimum length of the private key
# 3. generate the private key ( a random number between min length and min length * 2)

# 4. generate the public key ( g ^ private key mod p)
# 5. send the public key to the server

# 6. receive the public key from the server to whom we want to send the message
# 7. generate the shared key ( public key ^ private key mod p)
# 8. encrypt the message using the shared key

# 9. send the encrypted message to the server

# -----------------------------
# 10. receive the encrypted message from the server

# 11. decrypt the message using the shared key
# 12. print the decrypted message


import requests

from aes.encrypt import *

from diffie_hellman.diff_hellman import generate_prime_number, bin_power


# base url of the server
BASE_URL = 'http://localhost:5086'


def give_options():
    print("1. register to the server")
    print("2. get available users")
    print("3. send a message to a user")
    print("4. get messages")
    print("5. exit")


headers = {'host': 'example.com'}

# get the p, g parameters and minimum length of the private key
request_url = BASE_URL + '/public/get_parameters'
response = requests.get(request_url, headers=headers)

# print the response
print(response)

# extract the p, g parameters and minimum length of the private key
body = response.json()
p = body['p']
g = body['g']
min_length = body['min_len']

print("p: ", p)
print("g: ", g)
print("min_length: ", min_length)

# listen for the username
username = input("Enter your username: ")


while True:
    # give options
    give_options()

    # listen for the user input
    option = input("Enter your option: ")

    # depending on the option
    if option == "1":
        # register to the server

        # listen for the username
        username = input("Enter your username: ")

        # listen for the private key length
        private_key_length = int(input("Enter your private key length: "))

        # generate the private key
        private_key, prime_factors, loop_count = generate_prime_number(
            private_key_length)

        # generate the public key
        # calculate g ^ private key mod p
        public_key = bin_power(g, private_key, p)

        # send the public key to the server
        request_url = BASE_URL + '/unauth/register'

        # send the username and public key
        response = requests.post(request_url, json={
            "username": username,
            "public_key": public_key
        }, headers=headers)

        # print the response
        print(response)

        # extract the response
        body = response.json()

        print(body)

    elif option == "2":
        # get available users

        # listen for the username
        user_response = requests.get(
            BASE_URL + '/users/get_all_users', headers=headers)

        # print the response
        print(user_response)

        # extract the response
        body = user_response.json()

        # the body is in the form of
        # {
        #     "users": [
        #         {
        #             "username": "user1",
        #             "public_key": 123
        #         },
        #         {
        #             "username": "user2",
        #             "public_key": 123
        #         }
        #     ]
        # }

        # extract the users
        users = body['users']

        # print the username of the users
        print("Available users: ")
        for user in users:
            print("\t", user['username'])

    elif option == "3":
        # send a message to a user

        # listen for the receiver
        receiver = input("Enter the receiver: ")

        # listen for the message
        message = input("Enter the message: ")

        # encode the message in to bytes
        message = int(message.encode('ascii').hex(), 16)

        # listen for the private key length
        private_key_length = int(input("Enter your private key length: "))
        # generate the private key
        private_key, prime_factors, loop_count = generate_prime_number(
            private_key_length)

        # generate the public key

        # get the public key of the receiver
        request_url = BASE_URL + '/users/get_user'
        response = requests.get(request_url, json={
            "username": receiver
        }, headers=headers)

        # print the response
        print(response)

        # extract the response
        body = response.json()

        # extract the public key
        public_key = body['public_key']

        # convert the public key to int
        public_key = int(public_key)

        # generate the shared key
        # calculate public key ^ private key mod p
        shared_key = bin_power(public_key, private_key, p)

        # encrypt the message using the shared key
        encrypted_message, _ = encrypt(message, shared_key)

        # send the encrypted message to the server
        request_url = BASE_URL + '/users/send_message'

        # send the username and public key
        response = requests.post(request_url, json={
            "sender": username,
            "receiver": receiver,
            "message": encrypted_message
        }, headers=headers)

        # print the response
        print(response)

        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print("Message sending failed")

    elif option == "4":
        # get messages

        # request the messages
        request_url = BASE_URL + '/users/get_messages'
        response = requests.get(request_url, json={
            "username": username
        }, headers=headers)

        # print the response
        print(response)

        # extract the response
        body = response.json()

        # extract the messages
        messages = body['messages']

        # print the messages
        print("Messages: ")
        for message in messages:
            # print the sender and receiver
            print("\t", message['sender'], "-> ", end="")
            print(message['receiver'], ": ", end="")
            # print the message
            print(message['message'])

    elif option == "5":
        # exit
        break
