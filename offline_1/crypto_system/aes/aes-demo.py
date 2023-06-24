# time module
import time

# import the encryption module
from encrypt import encrypt, decrypt

# take the input from the user as ascii text
text = input()
# convert the text to integer
text_bytes = int(text.encode("ascii").hex(), 16)

# take the key from the user as ascii text
key = input()
# convert the key to integer
key_bytes = int(key.encode("ascii").hex(), 16)

# print the text as hex and in ascii
print("plain text:")
print("\tin Hex:", hex(text_bytes))
print("\tin ASCII:", text)

# print the key as hex and in ascii
print("key:")
print("\tin Hex:", hex(key_bytes))
print("\tin ASCII:", key)

# start the timer here
current_time = time.time_ns()

# check of the key is 128 bits
# if not, pad it with 0s or truncate it
if len(key) > 16:
    key_bytes = key_bytes & 0xffffffffffffffffffffffffffffffff
elif len(key) < 16:
    key_bytes = key_bytes << (16 - len(key)) * 8


# check of the text is 128 bits
# if not, pad it with 0s
# or divide it into blocks last block is padded with 0s
text_blocks = []
if len(text) > 16:
    while len(text) > 16:
        text_blocks.append(text[:16])
        text = text[16:]
    text_blocks.append(text)
elif len(text) < 16:
    text_bytes = text_bytes << (16 - len(text)) * 8
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
    cipher, key_expansion_time = encrypt(block_bytes, key_bytes)
    # # append the cipher to the ciphertext
    ciphertext.append(cipher)

# stop the timer here
current_time = time.time_ns() - current_time        # in nanoseconds
encryption_time = current_time / 1000000            # in milliseconds

# concatenate the ciphertext blocks
ciphertext_int = 0
# reverse the ciphertext blocks
ciphertext.reverse()
for cipher in ciphertext:
    ciphertext_int <<= 128
    ciphertext_int += cipher

# print the ciphertext as hex and in ascii
print("Ciphertext:")
print("\tin Hex:", hex(ciphertext_int))
# take the 2 hex digits at a time and convert them to ascii
cipher_text_ascii = ""
while ciphertext_int > 0:
    cipher_text_ascii = chr(ciphertext_int & 0xff) + cipher_text_ascii
    ciphertext_int >>= 8
print("\tin ASCII:", cipher_text_ascii)


# start the timer here
current_time = time.time_ns()
# decrypt each block
plaintext_block = []
for cipher in ciphertext:
    # decrypt the block
    plain = decrypt(cipher, key_bytes)
    # append the plain to the plaintext
    plaintext_block.append(plain)

# concatenate the plaintext blocks
plaintext = ""
for plain in plaintext_block:
    # take the 2 hex digits at a time and convert them to ascii
    # also keep the values in a integer
    while plain > 0:
        plaintext = chr(plain & 0xff) + plaintext
        plain >>= 8

# reverse the plaintext_int to get the original value taking 2 hex digits at a time
plaintext_int = int(plaintext.encode("ascii").hex(), 16)


# stop the timer here
current_time = time.time_ns() - current_time        # in nanoseconds
decryption_time = current_time / 1000000            # in milliseconds

# print the plaintext
print("Deciphered Text:")
print("\tin Hex:", hex(plaintext_int))
print("\tin ASCII:", plaintext)

# print the time taken
print("Key Expansiton time", key_expansion_time, "ms")
print("Encryption Time", encryption_time, "ms")
print("Decryption Time", decryption_time, "ms")
