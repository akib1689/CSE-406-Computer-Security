# at first wee need to generate a large prime number
# and a generator for the group


def is_prime(n):
    """
    n: int (Assumes n is a positive integer)
    returns: True if n is prime, False otherwise
    uses miller rabin's primality test to check if n is prime
    Steps:
        - find n - 1 = 2 ^ k * m
        - pick a random integer a in the range [2, n - 2]
        - compute b = a ^ m mod n
        - if b = 1 or b = n - 1, return True
        - for i in range(1, k)
            - compute b = b ^ 2 mod n
            - if b = n - 1, return True
        - return False
    """


def generate_prime_number(k):
    """
    k: int (Assumes k is a positive integer)
    returns: a prime number with at least k bits and 
            the value of length of the prime number in bits
    Steps:
        - find 2 ^ k + 1
        - check if it is prime
        - if not, increase k's value by 1 and repeat
    """

    # find 2 ^ k + 1
    n = 2 ** k + 1
    # check if it is prime
    while not is_prime(n):
        # if not, increase k's value by 1 and repeat
        k += 1
        n = 2 ** k + 1
    return k, n


print(generate_prime_number(128))
