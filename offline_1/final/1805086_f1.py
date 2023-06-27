# this file opens a server and waits for a connection from bob
# once bob connects, alice sends generates p,g, and g ^ a mod p
# and sends it to bob. Then alice waits for bob to send g ^ b mod p
# and then alice calculates the shared secret and encrypts a message
# and sends it to bob

import socket
import random

from diff_hellman import generate_prime_number, generate_generator_for_prime, bin_power

from encrypt import encrypt

from file_process import file_to_binary

# take the file name as input from the user
file_name = input("Enter the file name to send: ")

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


port = 5086

# bind to the port
serversocket.bind(('localhost', port))

# queue up to 5 requests
serversocket.listen(5)

# generate a random integer between 1 and 50
# this will be the length of the secret key

k = random.randint(1, 50)


# establish a connection
clientsocket, addr = serversocket.accept()

print("Got a connection from %s" % str(addr))

# generate p,g, and g ^ a mod p
p, prime_factors, loop_count = generate_prime_number(128)
print("p = " + str(p))
g = generate_generator_for_prime(p, prime_factors)
print("g = " + str(g))
a, prime_factors, loop_count = generate_prime_number(64 + k)

print("The length of the secret key is: " + str(k + 64))

A = bin_power(g, a, p)
print("g ^ a mod p = " + str(A))
# send p, g, and g ^ a mod p to bob

# encode file name in an integer
file_name_int = int(file_name.encode("utf-8").hex(), 16)

# concate p, g, and g ^ a mod p with commas
# and send it to bob
message = str(p) + "," + str(g) + "," + str(A) + "," + str(file_name_int)
clientsocket.send(bytes(message, 'utf-8'))


# receive g ^ b mod p from bob
B = int(clientsocket.recv(1024).decode('utf-8'))

# calculate the shared secret
shared_secret = bin_power(B, a, p)

print("The shared secret is: " + str(shared_secret))

# data is an integer
data = file_to_binary(file_name)

# print("The data is: ")
# print(hex(data))


# divide the data into blocks of 16 bytes
data_blocks = []
if data > 128:
    while data > 128:
        data_blocks.append(data & 0xffffffffffffffffffffffffffffffff)
        data >>= 128

    # pad the data with 0s
    data = data << (128 - data.bit_length())
    data_blocks.append(data)
elif data < 128:
    # pad the data with 0s
    data = data << (128 - data.bit_length())
    data_blocks.append(data)
else:
    data_blocks.append(data)

# reverse the data blocks
data_blocks.reverse()
# print("The data blocks are: ")
# for block in data_blocks:
#     print(hex(block))
# encrypt each block
ciphertext = []
key_expansion_time = 0
for block in data_blocks:
    # convert the block to integer
    # block_bytes = int(block.encode("utf-8").hex(), 16)
    block_bytes = block
    # encrypt the block
    cipher, key_expansion_time = encrypt(block_bytes, shared_secret)
    # # append the cipher to the ciphertext
    ciphertext.append(cipher)


# concatenate the ciphertext blocks
ciphertext_int = 0
# reverse the ciphertext blocks
ciphertext.reverse()
for cipher in ciphertext:
    ciphertext_int <<= 128
    ciphertext_int += cipher

print("the encrypted message is generated")

# send the encrypted message to bob
clientsocket.sendall(bytes(str(ciphertext_int), 'utf-8'))
print("the encrypted message is sent")

# close the socket
serversocket.close()
print("the connection is closed")
