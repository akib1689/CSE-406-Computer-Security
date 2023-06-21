# import the encryption module
from encrypt import encrypt, decrypt

# take the input from the user as ascii text
text = input("Enter the text to encrypt: ")
# convert the text to integer
text_bytes = int(text.encode("ascii").hex(), 16)

# take the key from the user as ascii text
key = input("Enter the key: ")
# convert the key to integer
key_bytes = int(key.encode("ascii").hex(), 16)

# print the text as hex and in ascii
print("plain text:")
print("\tin ascii:", text)
print("\tin hex:", hex(text_bytes))

# print the key as hex and in ascii
print("key:")
print("\tin ascii:", key)
print("\tin hex:", hex(key_bytes))

# check of the key is 128 bits
# if not, pad it with 0s or truncate it
if len(key) > 16:
    print("key is too long, truncating to 128 bits")
    key_bytes = key_bytes & 0xffffffffffffffffffffffffffffffff
elif len(key) < 16:
    print("key is too short, padding with 0s")
    key_bytes = key_bytes << (16 - len(key)) * 8

# check of the text is 128 bits
# if not, pad it with 0s
# or divide it into blocks last block is padded with 0s
text_blocks = []
if len(text) > 16:
    print("text is too long, dividing into blocks")
    while len(text) > 16:
        text_blocks.append(text[:16])
        text = text[16:]
    text_blocks.append(text)
elif len(text) < 16:
    print("text is too short, padding with 0s")
    text_bytes = text_bytes << (16 - len(text)) * 8
    text = text + "\x00" * (16 - len(text))
    text_blocks.append(text)
else:
    text_blocks.append(text)

# print("blocks:", text_blocks)
# encrypt each block
ciphertext = []

for block in text_blocks:
    # convert the block to integer
    block_bytes = int(block.encode("ascii").hex(), 16)
    # encrypt the block
    cipher = encrypt(block_bytes, key_bytes)
    # print("test")
    # # append the cipher to the ciphertext
    ciphertext.append(cipher)


# print the ciphertext
print("ciphertext:")
for cipher in ciphertext:
    print("\tin hex:", hex(cipher))
    # take the 2 hex digits at a time and convert them to ascii
    cipher_text = ""
    while cipher > 0:
        cipher_text = chr(cipher & 0xff) + cipher_text
        cipher >>= 8
    print("\tin ascii:", cipher_text)


# decrypt each block
plaintext_block = []
for cipher in ciphertext:
    # decrypt the block
    plain = decrypt(cipher, key_bytes)
    # append the plain to the plaintext
    plaintext_block.append(plain)

# concatenate the plaintext blocks
plaintext = ""
plaintext_int = 0
# reverse the plaintext blocks
plaintext_block.reverse()
for plain in plaintext_block:
    # take the 2 hex digits at a time and convert them to ascii
    # also keep the values in a integer
    while plain > 0:
        plaintext = chr(plain & 0xff) + plaintext
        plain >>= 8
        plaintext_int <<= 8
        plaintext_int += ord(plaintext[0])

# convert the plaintext to ascii


# print the plaintext
print("plaintext:")
print("\tin ascii:", plaintext)
print("\tin hex:", hex(plaintext_int))
