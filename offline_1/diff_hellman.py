# at first wee need to generate a large prime number
# and a generator for the group

# bases to check in miller rabin's primality test
bases = [2, 3, 5, 13, 19, 73, 193, 407521, 299210837, 3749873355]


def bin_power(base, power, mod):
    """
    base: base of the exponent
    power: power of the exponent
    mod: modulo value
    returns: base ^ power mod mod
    """
    result = 1
    base %= mod
    while power > 0:
        if power & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        power >>= 1
    return result


def check_composit(n, a, d, s):
    """
    n: the number to check if it is prime
    a: random integer in the range [2, n - 2]
    d: n - 1 = 2 ^ k * d
    s: k
    returns: True if n is probably prime, False otherwise
    Steps:
        - compute b = a ^ m mod n
        - if b = 1 or b = n - 1, return True
        - for i in range(1, k)
            - compute b = b ^ 2 mod n
            - if b = n - 1, return True
        - return False
    """
    x = bin_power(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for i in range(1, s):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False


def is_prime(n):
    """
    n: int (Assumes n is a positive integer)
    returns: True if n is prime, False otherwise
    uses miller rabin's primality test to check if n is prime
    Steps:
        - if n < 2, return False
        - if n is even, return False
        - find d and s such that n - 1 = 2 ^ s * d
        - for b in bases
            - if not check_composit(n, b, d, s), return False
        - return True    
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1
    for b in bases:
        if n == b:
            return True
        if not check_composit(n, b, d, s):
            return False
    return True


def generate_prime_number(k):
    """
    k: int (Assumes k is a positive integer)
    returns: a prime number with at least k bits and 
            the value of length of the prime number in bits
    Steps:
        - find 2 ^ k + 1
        - check if it is prime
        - if not, increase n's value by 1 and repeat
    """

    # find 2 ^ k + 1
    n = 2 ** k + 1
    # check if it is prime
    while not is_prime(n):
        # if not, increase n's value by 1 and repeat
        n += 1
    return k, n


print(generate_prime_number(128))
