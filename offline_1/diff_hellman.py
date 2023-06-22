# at first wee need to generate a large prime number
# and a generator for the group

# bases to check in miller rabin's primality test
bases = [2, 3, 5, 13, 19, 73, 193, 407521, 299210837, 3749873355]

# primes to multiply with n in generate_prime_number
# it contains primes up to 100
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
          31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


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
            and the set of prime factor of p-1
    Steps:
        - find 2 ^ k + 1
        - check if it is prime
        - if not, decrease n by 1 
                multiply n by one of the primes in bases
                add 1 and repeat
    """
    # set of prime factors of p - 1
    prime_factors = set()
    # 2 is always a prime factor as we are starting from 2 ^ k + 1
    prime_factors.add(2)
    # find 2 ^ k + 1
    n = 2 ** k + 1
    # check if it is prime
    loop_count = 0
    while not is_prime(n):
        loop_count += 1
        n -= 1
        n *= primes[loop_count % len(primes)]
        prime_factors.add(primes[loop_count % len(primes)])
        n += 1
    return n, prime_factors, loop_count


def generate_generator_for_prime(p, set_of_prime_factors):
    """
    p: prime number
    set_of_prime_factors: set of prime factors of p - 1
    returns: a generator for the group of p
    Steps:
        - find euler's totient function of p
        - if p is prime, so phi(p) = p - 1
        - now find the set of all prime factors of p - 1
        - here this set is given as a parameter
        - for a g in range [2, p - 1]
        if for all prime factors of p - 1, g ^ (p - 1) / prime_factor != 1
        then g is a generator

    Note: this might seem like a brute force approach
        but the generator for a prime is very common and usually small
    """
    # find euler's totient function of p
    phi_p = p - 1
    # for a g in range [2, p - 1]
    for g in range(2, p):
        # if for all prime factors of p - 1, g ^ (p - 1) / prime_factor != 1
        if all(bin_power(g, phi_p // prime_factor, p) != 1 for prime_factor in set_of_prime_factors):
            # then g is a generator
            return g

    return None


# max_loop_count = -1
# for i in range(1, 256):
#     p, prime_factors, loop_count = generate_prime_number(i)
#     if loop_count > max_loop_count:
#         max_loop_count = loop_count
#     print(prime_factors, p)
# print(max_loop_count)

# take the number of digits as input
n = int(input("Enter the minimum length of p in binary digits: "))

p, prime_factors, loop_count = generate_prime_number(n)
g = generate_generator_for_prime(p, prime_factors)
print(p, g)

# generate 2 primes a, b with n / 2 bits
a, prime_factors, loop_count = generate_prime_number(n // 2)
b, prime_factors, loop_count = generate_prime_number(n // 2)

print(a, b)

# compute A = g ^ a mod p
A = bin_power(g, a, p)
# compute B = g ^ b mod p
B = bin_power(g, b, p)

print(A, B)

# compute fact_1 = B ^ a mod p
fact_1 = bin_power(B, a, p)

# compute fact_2 = A ^ b mod p
fact_2 = bin_power(A, b, p)

print(fact_1, fact_2)           # both are equal to g ^ (a * b) mod p
