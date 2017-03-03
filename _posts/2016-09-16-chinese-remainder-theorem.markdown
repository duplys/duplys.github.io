---
layout: post
title:  "Chinese Remainder Theorem for Fun and Profit"
date:   2016-12-31 19:32:55 +0100
categories: public-key crypto math
---

<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

In this post, we'll look at the Chinese Remainder Theorem (CRT), an interesting mathematical tool in its own right and a 'work-horse' in the context of public-key cryptography. We'll look at what CRT exactly is, how it is used in modern cryptography, and what benefits it offers. If you are a professional cryptographer, you obviously know these things very well---stop reading here. To explain the CRT, I will make some simplifying assumptions and use some 'school book' crypto. 

In their 2003 book "Practical Cryptography", Ferguson and Schneier open the RSA Chapter by claiming RSA to be probably the most widely used, and certainly the best known, public-key crypto system in the world. Trying to check whether this proposition is still valid in 2016, I could only find one reliable reference of a newer date. In the 2009 book "Understanding Cryptography: A Textbook for Students and Practitioners", Paar and Pelzl postulate that RSA is---even at that point in time---still the most widely used asymmetric cryptography scheme, even though elliptic curves are gaining ground for good reasons (see e.g. this [nice discussion on elliptic curve advantages over RSA](http://crypto.stackexchange.com/questions/1190/why-is-elliptic-curve-cryptography-not-widely-used-compared-to-rsa) on Cryptography Stack Exchange). 

While elliptic curves offer many advantages, in particular performance related ones, the RSA crypto system [introduced by Riverst, Shamir, and Adleman in 1977](http://people.csail.mit.edu/rivest/Rsapaper.pdf) has stood the test of almost 40 years of attacks, and while I wouldn't go as far as to claim that RSA is here to stay, I think it is reasonable to assume---especially considering the (then) legacy systems---that RSA will remain widely used in real-world cryptographic applications and appliances for at least the next decade or so.

Nevertheless, as the title of this post implies, we want to talk about CRT and not RSA. So why this lengthy introduction? Well, to understand why (and where) CRT is relevant in public-key cryptography, it is necessary to discuss the fundamentals of the RSA crypto system first. To make things a bit simpler, we will only look at the number theoretical basics of RSA. For a real world use, you'd have to do a number of additional things like padding that I will not cover in this post. The calculations shown here are just 'school book' examples to elaborate the working principle and the advantages of CRT when used in combination with RSA.

Modern textbooks on cryptography contain well formalized definitions of the RSA crypto system and its properties. But since we want to keep things simple, we're going to refrain to the more straightforward definition from the original paper.

The RSA crypto system is based on a [trapdoor one-way function](https://en.wikipedia.org/wiki/Trapdoor_function). It is a function that is easy to compute in one direction, but difficult to compute in the opposite direction---in mathematical parlance: difficult to invert---without special information (the "trapdoor"). Roughly speaking, RSA encrypts a message by: 

1. representing the message as a number $$m$$,
2. raising $$m$$ to a publicly specified power $$e$$,
3. taking the _remainder_ when the result is divided by the publicly specified number $$n=p\cdot q$$ that is a product of two large secret prime numbers $$p$$ and $$q$$. 

In other words, the message $$m$$ is encrypted to the ciphertext $$c$$ by computing:

$$
c = m^e \pmod{n}
$$

where the pair $$(e,n)$$ is the public key. The decryption procedure is similar to the encryption, the only difference being that the private key---the secret power $$d$$---is used to decrypt the ciphertext. To decrypt the message, the recipient computes:

$$
m = c^d \pmod{n}
$$ 

where $$d$$ is such that $$e\cdot d \equiv 1 \pmod{mod(p−1)\cdot (q−1)}$$.
 
Security of the RSA system rests on the difficulty of factoring the published divisor $$n$$. This computational problem---which also happens to be a (trap-door) one-way function---is known as the _integer factorization problem_. The integer factorization problem states that it is computationally easy to multiply two large primes (in fact, this can be done with paper and pencil), but it is computationally very hard to factor the resulting product into the original primes (assuming you don't know these primes beforehand). 

Nevertheless, in **practice** computing RSA in a straight forward manner, i.e. doing computations modulo the composite number $$n$$, is computationally expensive even for the legitimate party. For this reason, most real-world RSA implementations use a mathematical tool called the _Chinese Remainder Theorem_ (CRT) to speed up the RSA calculation. CRT is named so because [the earliest known statement of the theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem#History) appears in a book "The Mathematical Classic of Sunzi"  written by Sunzi during the 5th century in China. While Sunzi's actual identity is unknown, it is an [established fact](https://en.wikipedia.org/wiki/The_Mathematical_Classic_of_Sunzi) that he lived much later than the author of _The Art of War_ Sun Tzu.

Most textbooks on cryptography introduce CRT as a theorem which states that for any integer $$n$$, if you know the remainders of the division of $$n$$ by several integers $$n_0,n_1,\ldots ,n_k$$, you can uniquely determine the remainder of the division of $$n$$ by the **product** of these integers---if the divisors  $$n_0,n_1,\ldots, n_k$$ are pairwise co-prime, that is. "Pairwise co-prime" is just another way of saying that any pair of integers from that set $$\{n_0,n_1,\ldots, n_k\}$$ doesn't have any greatest common divisor other than 1. That is---more formally expressed---if the $$n_i$$ are pairwise co-prime and $$a_1, \ldots , a_k$$ are any integers, then there exists an integer $$x$$ such that:

$$
\begin{aligned}
x\equiv a_{1}&{\pmod {n_{1}}}\\
\quad \vdots \\
x\equiv a_{k}&{\pmod {n_{k}}} \\
\end{aligned}
$$

As an example, if a number $$x$$ is congruent to the number $$a$$ modulo the product $$pq$$ --- i.e. $$x \equiv a {\pmod {pq}}$$ --- then $$x$$ is congruent both to $$a$$ modulo $$p$$ as well as to $$a$$ modulo $$q$$, i.e. it holds that $$x \equiv a \pmod q$$ and $$x \equiv a \pmod p$$.

At this point you can already start to see the connection between CRT and the RSA crypto system. All you have to do is to consider that in RSA, the computations for both encryption and decryption are performed modulo the composite integer $$N=p \cdot q$$. By definition of RSA, $$N$$ is nothing but a product of two primes $$p$$ and $$q$$ so that these two numbers are naturally also pairwise co-prime and, hence, meet the "requirements" for CRT.

Thus, instead of thinking about CRT as a theorem about a specific property of integers, you can think of CRT simply as a different representation of a number $$x$$, or more precisely, a representation of $$x$$ modulo a composite integer $$n=p\cdot q$$. For each number $$x$$ modulo such $$n=p\cdot q$$, you can represent $$x$$ by the pair $$(x\pmod{p}, x\pmod{q})$$. CRT states that you can reconstruct $$x$$ if you know $$(x\pmod{p}, x\pmod{q})$$, because for any given pair $$(x\pmod{p}, x\pmod{q})$$ there is at most one solution for $$x$$.

To convince ourselves that CRT is indeed capable of speeding up the computations modulo $$n$$ (where $$n=p\cdot q$$ and $$p$$, $$q$$ are co-prime integers), we can experiment with some toy RSA parameters. I wrote a small Python script and uploaded it to [GitHub's gist](https://gist.github.com/duplys/c8d816802acc9e46eb4a5c5f1aba60e6) in case you want to reproduce the experiment on your machine:

```
$ python rsa_demo.py
[*] p = 691
[*] q = 701
[*] n = p * q = 484391
[*] phi = 483000
[*] e = 17
[*] d = 369353
[*] m = 1853
[*] c = 396097
[*] test: c = 1853**e % n = 396097**d % n = m_d = 1853
```

To see the merits of using CRT, we will now focus on RSA's decryption operation (since it has a higher execution time than encryption). With RSA, the naive way to decrypt a ciphertext is to compute $$c=e^d {\pmod{n}}$$. We can measure the execution time of the corresponding code using the command line interface of the Python's `timeit` module. On my machine with 4 GB memory and an Intel Core i7 CPU running at 2.2 GHz (OS X 10.11.6 operating system), the naive calculation needs around 1.1 seconds:

```
$ python -m timeit -s 'c = 396097; d = 369353; n = 484391'  'm = (c**d) % n'
10 loops, best of 3: 1.11 sec per loop
``` 

What happens if we apply CRT to our calculations? Can we gain anything---in terms of the execution time---if we compute $$c^d{\pmod{p}}$$ and $$c^d{\pmod{q}}$$ instead of computing $$c=e^d {\pmod{n}}$$? It turns out that the resulting execution time is almost identical, amounting to slightly less than 1.2 seconds:

```
$ python -m timeit -s 'c = 396097; d = 369353; p = 691'  '(c**d) % p'
10 loops, best of 3: 1.11 sec per loop
$ python -m timeit -s 'c = 396097; d = 369353; q = 701'  '(q**d) % q'
10 loops, best of 3: 381 msec per loop
```

Hmmm, that obviously didn't help much. Can we somehow speed this up, in particular by leveraging the CRT properties and some basic number theory? Luckily, the answer is "yes". Before performing the exponentiation, we can reduce the base $$c$$ by $$p$$ and $$q$$, respectively. Using this reduction already gives us a speedup of about a factor of 4, as it turns out:

```
$ python -m timeit -s 'c = 396097; d = 369353; p = 691'  '((c%p)**d) % p'
10 loops, best of 3: 230 msec per loop
$ python -m timeit -s 'c = 396097; d = 369353; q = 701'  '((c%q)**d) % q'
100 loops, best of 3: 9.94 msec per loop
```

But we can do even better than that! Since $$p$$ and $$q$$ are primes and we know that $$c^{p-1}\equiv 1 {\pmod{p}}$$ and $$c^{q-1}\equiv 1 {\pmod{q}}$$, we can reduce the exponents. For instance, if we have $$x\equiv c^d {\pmod{p}}$$, then we can express this as $$x\equiv c^{(p-1)\times t + r=d} {\pmod{p}}$$ or $$x\equiv c^{(p-1)\times t}c^r {\pmod{p}}$$ because $$c^{(p-1)\times t} {\pmod{p}}$$ is 1. Likewise, we can apply the same mathematical trick for $$x\equiv c^d {\pmod{q}}$$ to reduce the exponent here. Reducing the exponents (which are now denoted by `dP` and `dQ`, respectively) gives us even more speed up (note the difference 'usec' (microseconds) vs 'msec' (milliseconds)):

```
$ python -m timeit -s 'c = 396097; dP = 203; p = 691'  '((c%p)**dP) % p'
100000 loops, best of 3: 3.56 usec per loop
$ python -m timeit -s 'c = 396097; dQ = 453; q = 701'  '((c%q)**dQ) % q'
100000 loops, best of 3: 4.89 usec per loop
```

So in total, rather than spending 1.2 seconds to compute $$m=c^d {\pmod{n}}$$ in a naive way, we need only roughly 9 **micro**seconds (!) to compute the above expressions $$(c {\pmod{p}})^{dP} {\pmod{p}}$$ and $$(c {\pmod{q}})^{dQ} {\pmod{q}}$$. We get $$a_1 = (c {\pmod{p}})^{dP} {\pmod{p}} = 471$$ and $$a_2 = (c {\pmod{q}})^{dQ} {\pmod{q}} = 451$$.

The last step for actually calculating the message $$m$$ is to reconstruct it from the values $$a_1, a_2$$. Without going into gory details (and explaining why this is the case), the easiest way to do this is based on the so-called _Garner's formula_:

$$
x = (((a_1-a_2)(q^{-1}\pmod{p})) \pmod{p})\cdot q + b
$$

or, expressed in Python code, by computing:

```
dP = d % (p-1)
dQ = d % (q-1)
a1 = ((c%p)**dP) % p
a2 = ((c%q)**dQ) % q
print("[*] a1= %d, a2 = %d" % (a1, a2))

qInv = mulinv(q, p)
print("[*] qInv = %d" % (qInv))

m_g = ( ( ( (a1-a2)*qInv ) % p) * q ) + a2

print("[*] m = %d, m_d = %d, m_g = %d" % (m, m_d, m_g))
```

This gives us:

```
[*] a1= 471, a2 = 451
[*] qInv = 622
[*] m = 1853, m_d = 1853, m_g = 1853
```

where the CRT-based decryption `m_g` is identical to our initial message 1853. And that should convince you that our CRT-based computation is mathematically correct, i.e. that it yields the same result as the naive calculation $$m = c^d \pmod{n}$$. 

The only cost of using the CRT---besides the additional software complexity---is the execution time for the necessary conversions, in particular the conversion of $$a_1,a_2$$ into the original message $$m$$ (denoted as `m_g` in our Python code). So let's perform one last measurement to determine the execution time for the conversion:

```
$ python -m timeit -s '
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


qInv = mulinv(701, 691); m_g = ( ( ( (481-142)*qInv ) % 691) * 701 ) + 142'
100000000 loops, best of 3: 0.0179 usec per loop
```

As you can see, the conversion overhead is only about 0.02 microseconds. So thanks to CRT, we were able to speed up the computation of our particular example (i.e. our toy RSA parameters) from 1.2 seconds to less than 10 microseconds. So our speed up (for _this_ example) turns out to be $$1.2 \textrm{ sec} / 1 * 10^{-5} \textrm{ sec} = 1.2 * 10^{5} = 120,000$$.

While the above speed up looks very impressive, it very much depends on the specific parameters we chose. For larger values of $$p, q, d, m, \ldots$$ the speed up will be significantly smaller. Yet, as a rule of thumb, if you do more than a few multiplications in one computation, the overhead of these conversions is worthwhile.


# References
* [Youtube Video on RSA and CRT by Jeff Suzuki](https://www.youtube.com/watch?v=6ytuvahX1tQ)
* [Niels Ferguson and Bruce Schneier "Practical Cryptography"](https://www.schneier.com/books/practical_cryptography/)
* [Wikipedia article on CRT](https://en.wikipedia.org/wiki/Chinese_remainder_theorem)
* [Useful explanation of RSA](http://www.di-mgt.com.au/crt_rsa.html)
* [Python documentation on `timeit`](https://docs.python.org/2/library/timeit.html)
* [Wikipedia's list of prime numbers](https://en.wikipedia.org/wiki/List_of_prime_numbers)
