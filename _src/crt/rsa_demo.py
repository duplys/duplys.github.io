#!/usr/bin/env python
# encoding: utf-8
"""
rsa_crt_demo.py

This worked example is based upon:
  1. Ferguson and Schneier "Practical Cryptography" (https://www.schneier.com/books/practical_cryptography/)
  2. http://www.cs.virginia.edu/~kam6zx/rsa/a-worked-example/

Created by Paul Duplys on 2016-12-02.
Copyright (c) 2016 . All rights reserved.
"""
import sys
import os
import time
import timeit
import sys

sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)



# The first step of RSA encryption is to generate two primes, p and q. Assume we generated these p and q:
p = 691 #7879 # 21013
q = 701 #7883 # 23981
print("[*] p = %d" % (p))
print("[*] q = %d" % (q))

# The second step is to compute the product of p and q is n, in our case:
n = p*q 
print("[*] n = p * q = %d" % (n))

# Next, we need to compute the Euler totient function \phi(n) which is defined as \phi(n) = (p-1)*(q-1):
phi = (p-1)*(q-1)
print("[*] phi = %d" % (phi)) 

# Now we have to chose an exponent e that is relatively prime to \phi(n) = (p-1)*(q-1). The pair (e, n) is our public key that is used to encrypt messages. In this example, we choose the number 5323 as our exponent. 5323 is relatively prime to \phi(n) because they share no factors. How do we know this? Well, we know this because 5323 itself is a prime number, so its only factors are 1 and 5323, so the numbers are relatively prime.
e = 17 #5323
print("[*] e = %d" % (e))

# The next step is to calculate a value for d. If you recall from the RSA algorithm, d must be chosen so that it is the inverse of e, modulo n. We will compute this using the extended Euclidean algorithm


def egcd(a, b):
	"""
	Compute the Extended Euclidean Algorithm (EEA) and return (g, x, y) a*x + b*y = gcd(x, y)
	"""
	if a == 0:
		return (b, 0, 1)
	else:
		g, x, y = egcd(b % a, a)
		return (g, y - (b // a) * x, x)


def mulinv(b, n):
	"""
	Return the multiplicative inverse of b modulo n
	"""
	g, x, _ = egcd(b, n)
	if g == 1:
		return x % n

d = mulinv(e, phi)
print("[*] d = %d" % (d))


m = 72345
print("[*] m = %d" % (m))

# d is our private key and is used to decrypt our messages. Now that we have both a public key and a private key, we can encrypt and decrypt messages.
pub_k = (e, n)
priv_k = (d, n)

# Let's perform encryption of a message m using the public key (e,n)
c = (m**e) % n
print("[*] c = %d" % (c))
m_d = (c**d) % n
print("[*] test: c = %d**e %% n = %d**d %% n = m_d = %d" % (m, c, m_d))
print("[*] enc expr:\n python -m timeit -s 'm = %d; e = %d; n = %d'  'c = (m**e) %% n' -n 100" % (m, e, n))
print("[*] dec expr:\n python -m timeit -s 'c = %d; d = %d; n = %d'  'm = (c**d) %% n' -n 100" % (c, d, n))


# If we run the 'enc expr' and 'dec expr' to measure the execution time of these computations, we clearly have to do something to improve their performance. Let's play with the Chinese Remainder Theorem. As a first step, let's do a simple test:
a1 = c**d % p
a2 = c**d % q
print("[*] a1= %d, a2 = %d" % (a1, a2))
print("[*] expr a1:\n python -m timeit -s 'c = %d; d = %d; p = %d'  '(c**d) %% p'" % (c, d, p))
print("[*] expr a2:\n python -m timeit -s 'c = %d; d = %d; q = %d'  '(q**d) %% q'" % (c, d, q))


# As a more advanced/more clever solution, let's reduce both bases c by their respective moduli:
a1 = ((c%p)**d) % p
a2 = ((c%q)**d) % q
print("[*] a1= %d, a2 = %d" % (a1, a2))
print("[*] expr a1 w/ reduction of c:\n python -m timeit -s 'c = %d; d = %d; p = %d'  '((c%%p)**d) %% p'" % (c, d, p))
print("[*] expr a2 w/ reduction of c:\n python -m timeit -s 'c = %d; d = %d; q = %d'  '((c%%q)**d) %% q'" % (c, d, q))


# Furthermore, since p and q are primes (and we are computing modulo p and modulo q, respectively), we can reduce the exponents:
dP = d % (p-1)
dQ = d % (q-1)
a1 = ((c%p)**dP) % p
a2 = ((c%q)**dQ) % q
print("[*] a1= %d, a2 = %d" % (a1, a2))
print("[*] expr a1 w/ reduction of c:\n python -m timeit -s 'c = %d; dP = %d; p = %d'  '((c%%p)**dP) %% p'" % (c, dP, p))
print("[*] expr a2 w/ reduction of c:\n python -m timeit -s 'c = %d; dQ = %d; q = %d'  '((c%%q)**dQ) %% q'" % (c, dQ, q))

# Finally, we are going to apply the Garner's formula to reconstruct the actual message from a1 and a2. Hopefully, the calculations using all the shortcuts are correct ...
qInv = mulinv(q, p)
print("[*] qInv = %d" % (qInv))

m_g = ( ( ( (a1-a2)*qInv ) % p) * q ) + a2

print("[*] m = %d, m_d = %d, m_g = %d" % (m, m_d, m_g))
