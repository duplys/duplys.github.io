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

sys.setrecursionlimit(1000000)  


# The first step of RSA encryption is to generate two primes, p and q. 
# Assume that we generated these p and q:
p = 691 
q = 701 
print("[*] p = %d" % (p))
print("[*] q = %d" % (q))

# The second step is to compute n, the product of p and q. In our case:
n = p*q 
print("[*] n = p * q = %d" % (n))

# Next, we need to compute the Euler totient function \phi(n) which is 
# defined as \phi(n) = (p-1)*(q-1):
phi = (p-1)*(q-1)
print("[*] phi = %d" % (phi)) 

# Now we have to chose an exponent e that is relatively prime to 
# \phi(n) = (p-1)*(q-1). The pair (e, n) becomes our public key that we use 
# to encrypt messages. In this example, we choose e = 17 which is relatively 
# prime to \phi(n) because they share no factors. How do we know this? 
# Well, we know this because 17 itself is a prime number, so its only factors 
# are 1 and 17, and hence the numbers are relatively prime.
e = 17 
print("[*] e = %d" % (e))

# The next step is to calculate the value d for our private key. If you recall 
# from the RSA algorithm, d must be chosen such that it is the inverse of e, 
# modulo n. We will compute this using the extended Euclidean algorithm
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

# (d, n) is our private key and we can use it to decrypt messages that were 
# encrypted using our public key (e, n). Now that we have both a public key 
# and a private key, we can encrypt and decrypt messages.
pub_k = (e, n)
priv_k = (d, n)

# Let's perform encryption of a message m using the public key (e,n)
c = (m**e) % n
print("[*] c = %d" % (c))
m_d = (c**d) % n
print("[*] test: c = %d**e %% n = %d**d %% n = m_d = %d" % (m, c, m_d))
print("[*] enc expr:\n python -m timeit -s 'm = %d; e = %d; n = %d'  'c = (m**e) %% n' -n 100" % (m, e, n))
print("[*] dec expr:\n python -m timeit -s 'c = %d; d = %d; n = %d'  'm = (c**d) %% n' -n 100" % (c, d, n))


# We can execute the 'enc expr' and 'dec expr' on the command line to measure 
# the execution time of the expressions 'c = (m**e) % n' and 'm = (c**d) % n',
# respectively.
# Can we do something to speed up these computations? Well, maybe we can apply
# the Chinese Remainder Theorem? As a first step, let's do a simple test:
a1 = c**d % p
a2 = c**d % q
print("[*] a1= %d, a2 = %d" % (a1, a2))
print("[*] expr a1:\n python -m timeit -s 'c = %d; d = %d; p = %d'  '(c**d) %% p'" % (c, d, p))
print("[*] expr a2:\n python -m timeit -s 'c = %d; d = %d; q = %d'  '(q**d) %% q'" % (c, d, q))


# Next, let's reduce both bases c by their respective moduli:
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


# Print the code for timing the execution of the Garner's formula to reconstruct the actual message m from a1 and a2.
print("[*] expr a1 w/ reduction of c:\n python -m timeit -s '\ndef egcd(a, b):\n    if a == 0:\n        return (b, 0, 1)\n    else:\n        g, x, y = egcd(b %% a, a)\n        return (g, y - (b // a) * x, x)\n\n\ndef mulinv(b, n):\n    g, x, _ = egcd(b, n)\n    if g == 1:\n        return x %% n\n\nqInv = mulinv(%d, %d)\nm_g = ( ( ( (%d-%d)*qInv ) %% %d) * %d ) + %d'" % (q, p, a1, a2, p, q, a2))
