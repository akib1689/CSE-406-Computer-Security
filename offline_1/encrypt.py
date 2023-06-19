# this file is used to encrypt the text 
# input: 
#   1. text: the text to be encrypted
#   2. key: the key to be used for encryption
# output:
#   1. cipher: the encrypted text

# import the key expansion file
from key_expansion import get_round_key

# s-box
from s_box import sbox

# round 0: add round key
def add_round_key(state, round_key):
    """
    state: 128-bit state
    round_key: 128-bit round key
    """
    return state ^ round_key


# test add_round_key
# state = 0x54776F204F6E65204E696E652054776F
# round_key = 0x5468617473206D79204B756E67204675