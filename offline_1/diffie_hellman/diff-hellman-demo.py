# import diff hellman module

from diff_hellman import *

import time

# generate a prime number of k bits and recort the time
# take k as input from the user

k = int(input())


# start the timer here
current_time = time.time_ns()


p, prime_factors, loop_count = generate_prime_number(k)


# stop the timer here
p_time = time.time_ns() - current_time
p_time = p_time / 1000000

# start the timer here
current_time = time.time_ns()
g = generate_generator_for_prime(p, prime_factors)

# stop the timer here
g_time = time.time_ns() - current_time
g_time = g_time / 1000000

# compute two random prime a, b with k / 2 bits and k / 2 + 5 bits


# start the timer here
current_time = time.time_ns()
a, prime_factors, loop_count = generate_prime_number(k // 2)


# stop the timer here
a_time = time.time_ns() - current_time
a_time = a_time / 1000000

# start the timer here
current_time = time.time_ns()
b, prime_factors, loop_count = generate_prime_number(k // 2 + 5)


# stop the timer here
b_time = time.time_ns() - current_time
b_time = b_time / 1000000


# compute A = g ^ a mod p
# start the timer here
current_time = time.time_ns()
A = bin_power(g, a, p)

# stop the timer here
A_time = time.time_ns() - current_time
A_time = A_time / 1000000

# compute B = g ^ b mod p
# start the timer here
current_time = time.time_ns()
B = bin_power(g, b, p)

# stop the timer here
B_time = time.time_ns() - current_time
B_time = B_time / 1000000


# Shared secret key generation time
# start the timer here
current_time = time.time_ns()
s1 = bin_power(B, a, p)

# stop the timer here
s1_time = time.time_ns() - current_time
s1_time = s1_time / 1000000

# start the timer here
current_time = time.time_ns()
s2 = bin_power(A, b, p)

# stop the timer here
s2_time = time.time_ns() - current_time
s2_time = s2_time / 1000000


# print the times
print(p_time, "ms,", g_time, "ms,", a_time, "ms,", b_time, "ms,",
      A_time, "ms,", B_time, "ms,", s1_time, "ms,", s2_time, "ms")
