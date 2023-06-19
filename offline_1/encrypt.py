# this file is used to encrypt the text 
# input: 
#   1. text: the text to be encrypted
#   2. key: the key to be used for encryption
# output:
#   1. cipher: the encrypted text

# import the key expansion file
from key_expansion import get_round_key

# import bitvector operations
from BitVector import *

# s-box
from s_box import sbox

# fixed column matrix for mix columns
mix_matrix =   [[0x02, 0x03, 0x01, 0x01],
                [0x01, 0x02, 0x03, 0x01],
                [0x01, 0x01, 0x02, 0x03],
                [0x03, 0x01, 0x01, 0x02]]

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

def mix_column_matrix(state_matrix):
    """
    state_matrix: 4x4 state matrix
    returns the corresponding state matrix after mixing columns
    steps:
    matrix multiplication:
        for each multiplication:
            - convert to bit vector
            - multiply by matrix using the function gf_multiply_moduler
            - convert back to matrix
    """
    # declare new state matrix (4x4)
    new_state_matrix = [[0 for i in range(4)] for j in range(4)]
    # matrix multiplication
    for i in range(4):
        for j in range(4):
            for k in range(4):
                a = BitVector(intVal=mix_matrix[i][k], size=8)
                b = BitVector(intVal=state_matrix[k][j], size=8)

                AES_modulus = BitVector(bitstring='100011011')

                c = a.gf_multiply_modular(b, AES_modulus, 8)
                new_state_matrix[i][j] ^= c.int_val()  
                # * this will work because XOR is addition is assosiative          
    return new_state_matrix
def rounds(state, round_key, round_number):
    """
    state: 2D array of 4x4 each is a byte (current state matrix)
    round_key: 2D array of 4x4 each is a byte (current round key matrix)
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
    #sanity check
    if round_number < 0 or round_number > 10:
        print("Invalid round number")
        return None
    if round_number == 0:
        # round 0: add round key
        state = add_round_key(state, round_key)
    elif round_number == 10:
        # last round: no mix columns
        state = sub_bytes(state)
        state = shift_rows(state)
        state = add_round_key(state, round_key)
    else:
        # normal round
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_column_matrix(state)
        state = add_round_key(state, round_key)

    return state

# runs the encryption algorithm
def encrypt(text, key):
    """
    text: 128-bit text
    key: 128-bit key
    """
    state = make_state(text) # 4x4 state matrix
    round_keys = get_round_key(key) # 11 round keys
    for i in range(11):
        round_key = round_keys[i]
        round_key = make_state(round_key)
        state = rounds(state, round_key, i)
        # debug
        # print("Round", i)
        # print("State matrix:")
        # for i in range(4):
        #     for j in range(4):
        #         print(hex(state[i][j]), end=" ")
        #     print()

    
    # after the loop ends, the state matrix is the ciphertext
    # read the state matrix in column major order
    ciphertext = 0
    for i in range(4):
        for j in range(4):
            ciphertext <<= 8
            ciphertext |= state[j][i]
    
    # print("Ciphertext:", hex(ciphertext))
    return ciphertext

# test add_round_key
# state = 0x54776F204F6E65204E696E652054776F
# round_key = 0x5468617473206D79204B756E67204675
state = 0x54776F204F6E65204E696E652054776F
round_key = 0x5468617473206D79204B756E67204675

cipher = encrypt(state, round_key)
print(hex(cipher))