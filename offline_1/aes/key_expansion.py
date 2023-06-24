# this file generates the round keys for the AES algorithm

# round key generation algorithm
# input: 128-bit key
# output: 11 round keys (128-bit each)

"""
Steps:
1. given a 128-bit key, split it into 4 words of 32-bit each
   w[0], w[1], w[2], w[3] 
2. find the g(w[3])
    - circular byte left shift by 1
    - substitute bytes from the s-box
    - xor with rconst
3. find w[4] = w[0] xor g(w[3])
4. find w[5] = w[4] xor w[1]
5. find w[6] = w[5] xor w[2]
6. find w[7] = w[6] xor w[3] 
   .. and so on
"""

# s-box
from s_box import sbox

# rconst
rconst = 0x01000000

# round constants
rcon = [0x01000000, 0x02000000, 0x04000000, 0x08000000,
        0x10000000, 0x20000000, 0x40000000, 0x80000000,
        0x1b000000, 0x36000000]

# circular byte left shift by 1


def rot_word(word):
    return ((word << 8) | (word >> 24)) & 0xffffffff

# substitute bytes from the s-box


def sub_word(index):
    return sbox[index]

# xor two words


def xor_word(word1, word2):
    return word1 ^ word2

# g() function


def g(word, rconst):
    """
    word: 32-bit word
        - circular byte left shift by 1
        - divide into 4 bytes
        - substitute bytes from the s-box
        - combine into a word
        - xor with round constant
    """
    # circular byte left shift by 1
    word = rot_word(word)
    # divide into 4 bytes
    byte = [0 for i in range(4)]
    for i in range(4):
        byte[i] = (word >> (24 - i*8)) & 0xff
    # substitute bytes from the s-box
    b1 = sub_word(byte[0])
    b2 = sub_word(byte[1])
    b3 = sub_word(byte[2])
    b4 = sub_word(byte[3])
    # combine into a word
    word = (b1 << 24) | (b2 << 16) | (b3 << 8) | b4
    # xor with rconst
    word = xor_word(word, rconst)
    return word


# generate the key schedule
def key_schedule(key):
    """
    key: 128-bit key
    divided into 4 words of 32-bits each
    """
    # initialize the key schedule
    w = [0 for i in range(44)]
    # first 4 words are the key itself
    w[0] = key[0]
    w[1] = key[1]
    w[2] = key[2]
    w[3] = key[3]
    # g_3 = g(w[3])
    # print(hex(g_3))
    # generate the key schedule
    for i in range(4, 44):
        if i % 4 == 0:
            w[i] = xor_word(w[i-4], g(w[i-1], rcon[i//4 - 1]))
        else:
            w[i] = xor_word(w[i-4], w[i-1])
    return w

# round key


def get_round_key(key_to_expand):
    """
    key_to_expand: 128-bit key
    """

    # divide key into 4 words
    w = [0 for i in range(4)]

    # convert key into 32-bit bitvectors
    for i in range(4):
        w[i] = key_to_expand >> (32 * (3 - i)) & 0xffffffff

    # generate the key schedule
    generated_key = key_schedule(w)

    # group the generated key into 4 words block
    round_key = [0 for i in range(11)]
    for i in range(11):
        for j in range(4):
            round_key[i] = (round_key[i] << 32) | generated_key[i*4 + j]

    return round_key


# round_wise_key = get_round_key(0x5468617473206d79204b756e67204675)

# test round key
# print the round wise key in hex (2 hex digit then space)
# for i in range(11):
#     # format the hex string
#     hex_string = hex(round_wise_key[i])
#     hex_string = hex_string[2:]
#     hex_string = hex_string.zfill(32)

#     hex_string = hex_string[0:2] + " " + hex_string[2:4] + " " + hex_string[4:6] + " " + hex_string[6:8] + " " + hex_string[8:10] + " " + hex_string[10:12] + " " + hex_string[12:14] + " " + hex_string[14:16] + " " + hex_string[16:18] + " " + hex_string[18:20] + " " + hex_string[20:22] + " " + hex_string[22:24] + " " + hex_string[24:26] + " " + hex_string[26:28] + " " + hex_string[28:30] + " " + hex_string[30:32]
#     print("Round: ", i , "\tkey: ", hex_string)
