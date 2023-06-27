# This file contains the code for Bob.
# Bob will be the client in this case.
# connects to the server that alice has created
# receives p, g, and g ^ a mod p from alice
# generates b and calculates g ^ b mod p
# sends g ^ b mod p to alice
# calculates the shared secret
# decrypts the message from alice
# prints the message
#


import socket

from diff_hellman import generate_prime_number, bin_power

from encrypt import decrypt
from file_process import binary_to_file


# create a socket object

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 5086

# connect to the server on local computer
s.connect(('localhost', port))

# receive data from the server
# p, g, and g ^ a mod p are seperated by commas
# split the data by commas
message = s.recv(1024).decode('utf-8')
p, g, A, file_name_int = message.split(",")

# convert p, g, and g ^ a mod p to integers
p = int(p)
g = int(g)
A = int(A)
file_name_int = int(file_name_int)

# generate b and calculate g ^ b mod p
b, prime_factors, loop_count = generate_prime_number(66)

B = bin_power(g, b, p)

# send g ^ b mod p to alice
s.send(bytes(str(B), 'utf-8'))

# calculate the shared secret
shared_secret = bin_power(A, b, p)

print("The shared secret is: " + str(shared_secret))

# convert the file name to ascii
# and print the file name
file_name = bytes.fromhex(hex(file_name_int)[2:]).decode('utf-8')
# append _copy to the file name before extension
file_name = file_name.split(".")[0] + "_copy." + file_name.split(".")[1]
print("The file name is: " + file_name)

# while there are some messages to receive
# receive the message from alice
# decrypt the message
# print the message
encrypted_message = ""
while True:
    message = s.recv(1024).decode('utf-8')
    encrypted_message += message
    if not message:
        break

# print("The encrypted message is: " + encrypted_message)

# close the connection
s.close()

# convert the message to an integer
encrypted_message = int(encrypted_message)

# print("encrypted message: ", hex(encrypted_message))
print("encrypted message is received")

# file output the encrypted message

cipher_text = []
while encrypted_message > 0:
    # take the 128 bit of the encrypted message
    # and append it to the cipher text
    cipher_text.append(encrypted_message & 0xffffffffffffffffffffffffffffffff)
    encrypted_message >>= 128

cipher_text.reverse()
# print("cipher text: ", cipher_text)


# decrypt the cipher text block by block
# convert the decrypted blocks to ascii
# and print the message
file_data = 0
shift_amount = 0
message_block = []
for block in cipher_text:
    decrypted_block = decrypt(block, shared_secret)
    file_data = (decrypted_block << shift_amount) | file_data
    shift_amount += 128
    message_block.append(decrypted_block)

# print("message block: ", message_block)

# concatenate the plaintext blocks
plaintext = ""
for plain in message_block:
    print(hex(plain))
    # take the 2 hex digits at a time and convert them to ascii
    # also keep the values in a integer
    while plain > 0:
        plaintext = chr(plain & 0xff) + plaintext
        plain >>= 8
print("-----------------------------------")
print("The decrypted message is: ")
print(plaintext)
print("-----------------------------------")
print("The file data is: ")
print(hex(file_data))

# write the decrypted message to a file
binary_to_file(file_data, file_name)
