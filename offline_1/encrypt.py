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
def add_round_key_entry(state_entry, round_key_entry):
    """
    state: 16-bit state
    round_key: 16-bit round key
    returns the corresponding state entry after the round key is added
    """
    return state_entry ^ round_key_entry

def add_round_key(state_matrix, round_key_matrix):
    """
    state_matrix: 4x4 state matrix
    round_key_matrix: 4x4 round key matrix
    returns the corresponding state matrix after the round key is added
    """
    for i in range(4):
        for j in range(4):
            state_matrix[i][j] = add_round_key_entry(state_matrix[i][j], round_key_matrix[i][j])
    return state_matrix
def make_state(text):
    """
    text: 128-bit text
    arranges the text into a 4x4 matrix
    in column major order (basically, transpose)
    """
    state = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            state[j][i] = (text >> (120 - 32*i - 8*j)) & 0xff
    return state

def sub_bytes_entry(state_entry):
    """
    state_entry: 8-bit state entry
    returns the corresponding entry after substituting from the s-box
    """
    return sbox[state_entry]

def sub_bytes(state_matrix):
    """
    state_matrix: 4x4 state matrix
    returns the corresponding state matrix after substituting from the s-box
    """
    for i in range(4):
        for j in range(4):
            state_matrix[i][j] = sub_bytes_entry(state_matrix[i][j])
    return state_matrix

def shift_rows(state_matrix):
    """
    state_matrix: 4x4 state matrix
    returns the corresponding state matrix after shifting rows
    """
    for i in range(1, 4):
        state_matrix[i] = state_matrix[i][i:] + state_matrix[i][:i]
    return state_matrix


def rounds(state, round_key, round_number):
    """
    state: 2D array of 4x4 each is a byte
    round_key: 2D array of 4x4 each is a byte
    round_number: the round number
    Each round consists of the following steps:
        1. substitute bytes
        2. shift rows
        3. mix columns
        4. add round key
    Exceptions:
        1. last round does not have mix columns
        2. round 0 only has add round key
    """
    if round_number == 0:
        # round 0: add round key
        state = add_round_key(state, round_key)
    elif round_number == 10:
        # last round: no mix columns
        state = sub_bytes(state)
        # state = shift_rows(state)
        # state = add_round_key(state, round_key)
    else:
        # normal round
        state = sub_bytes(state)
        state = shift_rows(state)
        # state = mix_columns(state)
        # state = add_round_key(state, round_key)

    return state





# def encrypt(text, key):
#     """
#     text: 128-bit text
#     key: 128-bit key
#     """
#     # generate the round keys
#     round_key = get_round_key(key)
#     # round 0: add round key



# test add_round_key
# state = 0x54776F204F6E65204E696E652054776F
# round_key = 0x5468617473206D79204B756E67204675
state = 0x54776F204F6E65204E696E652054776F
state = make_state(state)

# print the state matrix
print("State matrix:")
for i in range(4):
    for j in range(4):
        print(hex(state[i][j]), end=" ")
    print()

# round key
round_key = 0x5468617473206D79204B756E67204675
round_key = make_state(round_key)

# print the round key matrix
print("Round key matrix:")
for i in range(4):
    for j in range(4):
        print(hex(round_key[i][j]), end=" ")
    print()

round_number = 0
state = rounds(state, round_key, round_number)

# print the state matrix
print("State matrix:")
for i in range(4):
    for j in range(4):
        print(hex(state[i][j]), end=" ")
    print()

# test sub_bytes
round_number = 1
state = rounds(state, round_key, round_number)

# print the state matrix
print("State matrix:")
for i in range(4):
    for j in range(4):
        print(hex(state[i][j]), end=" ")
    print()
