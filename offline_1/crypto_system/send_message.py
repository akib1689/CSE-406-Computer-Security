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

    elif option == "2":
        # get available users

        # listen for the username
        user_response = requests.get(
            BASE_URL + '/users/get_users', headers=headers)

        # print the response
        print(user_response)

    elif option == "3":
        # send a message to a user

        # listen for the receiver
        receiver = input("Enter the receiver: ")

        # listen for the message
        message = input("Enter the message: ")

    elif option == "4":
        # get messages

        # listen for the sender
        sender = input("Enter the sender: ")

        # listen for the receiver
        receiver = input("Enter the receiver: ")

    elif option == "5":
        # exit
        break
