# this file opens a server and waits for a connection from bob
# once bob connects, alice sends generates p,g, and g ^ a mod p
# and sends it to bob. Then alice waits for bob to send g ^ b mod p
# and then alice calculates the shared secret and encrypts a message
# and sends it to bob

import socket
import random

from diff_hellman import generate_prime_number, generate_generator_for_prime, bin_power

from encrypt import encrypt, decrypt


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

# concate p, g, and g ^ a mod p with commas
# and send it to bob

message = str(p) + "," + str(g) + "," + str(A)
clientsocket.send(bytes(message, 'utf-8'))


# receive g ^ b mod p from bob
B = int(clientsocket.recv(1024).decode('utf-8'))

# calculate the shared secret

shared_secret = bin_power(B, a, p)

print("The shared secret is: " + str(shared_secret))


# encrypt the message in the story.txt file

# open the file and read the contents
file = open('story.txt', 'r')
text = file.read()
file.close()

text_blocks = []
if len(text) > 16:
    while len(text) > 16:
        text_blocks.append(text[:16])
        text = text[16:]
    text_blocks.append(text)
elif len(text) < 16:
    text = text + "\x00" * (16 - len(text))
    text_blocks.append(text)
else:
    text_blocks.append(text)

# print("blocks:", text_blocks)
# encrypt each block
ciphertext = []
key_expansion_time = 0
for block in text_blocks:
    # convert the block to integer
    block_bytes = int(block.encode("ascii").hex(), 16)
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

encrypted_message = ciphertext_int

# print the ciphertext as hex and in ascii
# print("Ciphertext:")
# print("\tin Hex:", hex(ciphertext_int))
# # take the 2 hex digits at a time and convert them to ascii
# cipher_text_ascii = ""
# while ciphertext_int > 0:
#     cipher_text_ascii = chr(ciphertext_int & 0xff) + cipher_text_ascii
#     ciphertext_int >>= 8
# print("\tin ASCII:", cipher_text_ascii)


# print the encrypted message
print("The encrypted message is: ", hex(encrypted_message))

# send the encrypted message to bob
clientsocket.sendall(bytes(str(encrypted_message), 'ascii'))

# close the socket
serversocket.close()
