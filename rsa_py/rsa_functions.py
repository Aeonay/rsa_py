'''
RSA modules with a class handing the ciphers and the keys and independant
functions.
'''

import logging
import random
import itertools
import fractions

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PRIME_LIST = [int(line.rstrip('\n')) for line in open('rsa_py/prime_list_1000.txt', 'r')]

def primality_test(n, k):
    '''Return True if n is prime, using Rabin-Miller alhorithm.'''
    if n < 0:
        logger.debug("Input number for is_prime(n) should be positive.")
        return False
    # Pre-tests: is n divisible by the first p primes ?
    if n & 1 == 0 and n > 2:
        return False
    for p in PRIME_LIST[1:]:
        if n % p == 0:
            return False
    d = nl = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for i in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if not x == 1:  # No need to test further
            j = 0
            while not x == nl:
                if j == s - 1:
                    return False
                else:
                    j += 1
                    x = pow(x, 2, n)
        return True

def extended_euclid_gcd(a, b):
    '''Returns a pair (x, y) such that xa + yb = gcd(a, b)'''
    x, xl, y, yl = 0, 1, 1, 0
    while b != 0:  # This line means we will have xa = gcd(a, b) in the end
        q, r = divmod(a, b)
        a, b = b, r
        x, xl = xl - q * x, x
        y, yl = yl - q * y, y
    return xl, yl

def mod_multiplicative_inv(e, n):
    '''Compute the modulare multiplicative inverse of e (mod n)'''
    x = extended_euclid_gcd(e, n)[0]  # Results in xa = 1 (mod n)
    if x < 0:
        return n + x
    return x

def gen_prime(b):
    """Generate random prime number with n > 8 bits."""
    if len(PRIME_LIST) < 1000:
        logger.warning("PRIME_LIST variable not initiated properly. Will \
                        slow down the key generation process. Check the \
                        file integrity in rsa_py/prime_list_1000.txt")
    # Ensure leading and trailing bits are ones, making a number greater
    # than 2^(b-1)
    get_random_n = lambda: random.getrandbits(b) | 1 << b | 1
    p = get_random_n()
    for i in itertools.count(1):  # Infinite loop until we find a prime
        if primality_test(p, 40):
            return p
        else:
            # Get a new random number, for probabilites are against us here
            if i % (b * 2) == 0:
                p = get_random_n()
            else:
                p += 2  # Add 2 since we are only interested in odd numbers


class RSAPy(object):
    '''A class that generates the keys and represents the RSA cipher.'''
    key_strength = 1024
    key = ''
    pubkey = []

    def __init__(self, key_strength=1024):
        self.key_strength = key_strength
        keys = self.key_generation()
        self.pubkey = keys[0:2]
        self.key = keys[2]

    def encrypt(self, message):
        '''Encrypt the message'''
        return pow(message, self.pubkey[1], self.pubkey[0])

    def decrypt(self, cipher):
        '''Decrypt cipher text'''
        return pow(cipher, self.key, self.pubkey[0])

    def key_generation(self):
        '''Generate the public key pair (e, n) and the private key d'''
        p = gen_prime(self.key_strength / 2)
        q = gen_prime(self.key_strength / 2)
        # Very unlikely, yet:
        while q == p:
            q = gen_prime(self.key_strength / 2)
        n = p * q
        x = (p - 1) * (q - 1)
        while True:
            e = random.randint(3, x - 1)
            if fractions.gcd(e, x) == 1:
                break
        d = mod_multiplicative_inv(e, x)
        return (n, e, d)
