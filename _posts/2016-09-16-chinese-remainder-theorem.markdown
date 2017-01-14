---
layout: post
title:  "Working Title: Chinese Remainder Theorem"
date:   2016-09-16 19:32:55 +0100
categories: public-key crypto math
---

<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

* In this post, we'll look at the Chinese Remainder Theorem, an interesting mathematical tool in its own right and a 'work-horse' in the context of modern day public-key cryptography.

* In their 2003 book "Practical Cryptography", Ferguson and Schneier open the RSA Chapter by claiming RSA to be probably the most widely used, and certainly the best known, public-key cryptosystem in the world. Trying to check whether this proposition is still valid in 2016, I could only find one reliable reference of a newer date. In the 2009 book "Understanding Cryptography: A Textbook for Students and Practitioners", Paar and Pelzl postulate that RSA is---even at that point in time---still the most widely used asymmetric cryptography scheme, even though elliptic curves are gaining ground for good reasons (see e.g. this [nice discussion on elliptic curve advantages over RSA](http://crypto.stackexchange.com/questions/1190/why-is-elliptic-curve-cryptography-not-widely-used-compared-to-rsa) on Cryptography Stack Exchange). Nevertheless, RSA, which was [first introduced by Riverst, Shamir, and Adleman in 1977](http://people.csail.mit.edu/rivest/Rsapaper.pdf), has stood the test of almost 40 years of attacks, and while I wouldn't go as far as to claim that RSA is here to stay, I think it is reasonable to assume---especially considering the (then) legacy systems---that RSA will remain widely used in real-world crypto applications at least for the next 10 years or so.

* While this post is on CRT and _not_ RSA, to understand why (and where) CRT is relevant in modern public-key cryptography, it is necessary to discuss the basics of the RSA crypto system first.

* While this will not really be important for our further discussion, I would like to emphasise that we'll only look at the mathematical/number theoretical basics of the RSA crypto system. Be aware of the fact that applying/using RSA in the real world securely implies that you have to do a number of additional things like e.g. padding. In this post, I will **not** cover these topics, so please be aware of the fact that any calculations presented in the following are just examples to elaborate the working principle and the advantages of CRT when used in combination with RSA. In particular, you should never use RSA like this (e.g. without padding, etc.). 

* Modern textbooks on cryptography contain well formalised definitions of the RSA system and it's properties. Since I would like to keep this part compact, we are going to refrain to the somewhat simpler RSA description from the original paper.

* RSA is based on a trapdoor one-way function. Roughly speaking, RSA encrypts a message by: 
1. representing the message as a number $$M$$,
2. raising $$M$$ to a publicly specified power $$e$$, and finally,
3. taking the remainder when the result is divided by the publicly specified number $$n$$ that is a product of two large secret prime numbers $$p$$ and $$q$$. 

* The decryption procedure is similar to the encryption, the only difference being that the secret power $$d$$ is used, where $$e\cdot d \equiv 1 \pmod{mod(p−1)\cdot (q−1)}$$. 

* The security of the RSA system rests on the difficulty of factoring the published divisor, $$n$$. This computational problem, which also happens to be a (trap-door) one-way function, is also known as the _integer factorization problem_: it is computationally easy to multiply two large primes (in fact, this can be done with paper and pencil), but it is computationally very hard to factor the resulting product into the original primes (assuming you don't know these primes beforehand). 

* Even for the legitimate user, computing RSA in the straight forward manner, i.e. doing computations modulo the composite number $$n$$, is computationally expensive. For this reason, most real-world RSA implementations use a mathematical tool called the _Chinese Remainder Theorem_ (CRT) to speed up the RSA computation. CRT is named so because [the earliest known statement of the theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem#History) appears in a book "The Mathematical Classic of Sunzi"  written by Sunzi during the 5th century in China. While Sunzi's actual identity is unknown, it is an [established fact](https://en.wikipedia.org/wiki/The_Mathematical_Classic_of_Sunzi) that he lived much later than the author of _The Art of War_ Sun Tzu.

* Most textbooks on cryptography introduce CRT as a theorem which states that, for any integer $$n$$, if you know the remainders of the division of $$n$$ by several integers $$n_0,n_1,\ldots ,n_k$$, you can uniquely determine the remainder of the division of $$n$$ by the **product** of these integers---if the divisors  $$n_0,n_1,\ldots, n_k$$ are pairwise co-prime, that is. "Pairwise co-prime" is just another way of saying that any pair of integers from that set $$\{n_0,n_1,\ldots, n_k\}$$ doesn't have any greatest common divisor other than 1.

* In other words, if the $$n_i$$ are pairwise co-prime, and if $$a_1, \ldots , a_k$$ are any integers, then there exists an integer $$x$$ such that

$$
\begin{aligned}
x\equiv a_{1}&{\pmod {n_{1}}}\\
\quad \vdots \\
x\equiv a_{k}&{\pmod {n_{k}}} \\
\end{aligned}
$$

and any two such $$x$$ are congruent modulo $$N$$, where $$N=n_1\cdot n_2 \cdot \ldots \cdot n_k$$ is the **product** of the $$n_i$$. As an example, if the number $$x$$ is congruent to the number $$a$$ modulo the product $$pq$$ --- i.e. $$x \equiv a {\pmod {pq}}$$ --- then $$x$$ is congruent to $$a$$ both modulo $$p$$ as well as modulo $$q$$. That is, it holds that $$x \equiv a \pmod q$$ and $$x \equiv a \pmod p$$.

At this point, you can already start to see the connection between CRT and the RSA crypto system. You only need to consider that in RSA, the computations for both encryption and decryption are performed modulo the composite integer $$N=p \cdot q$$. By definition of RSA, $$N$$ is nothing but a product of two primes $$p$$ and $$q$$, so that these two numbers are naturally also pairwise co-prime and, hence, meet the "requirements" for CRT.

* Instead of thinking about CRT as a theorem about a specific property of integers, one might think of CRT simply as a different representation of a number, specifically a representation  modulo a composite integer $$n=p\cdot q$$. 

* For each number $$x$$ modulo $$n$$ --- that is, an $$x\{\in 0,1,2,3, \ldots , n-1\}$$ --- you can compute the pair $$(x\pmod{p}, x\pmod{q})$$. The CRT states that you can reconstruct $$x$$ if you know $$(x\pmod{p}, x\pmod{q})$$ because for any given pair $$(x\pmod{p}, x\pmod{q})$$ there is at most one solution for $$x$$.


* Let's play around with some toy RSA parameters. Bla bla bla. You can find the code here. Here's the output of the code (TODO: include a link to a github gist or a git repository)

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

* Let's focus on the decryption now (since it has a higher execution time here). The naive way to decrypt the ciphertext is to compute $$c=e^d {\pmod{n}}$$. We can measure the execution time of the corresponding code using the command line interface of the Python's `timeit` module. It turns out that the naive calculation needs about 1.2 seconds:

```
$ python -m timeit -s 'c = 396097; d = 369353; n = 484391'  'm = (c**d) % n'
10 loops, best of 3: 1.12 sec per loop
``` 

* What about applying the CRT to our calculations? Can we gain anything---in terms of the execution time---if we compute $$c^d{\pmod{p}}$$ and $$c^d{\pmod{q}}$$ instead of computing $$c=e^d {\pmod{n}}$$? It turns out that the result is rather the same, amounting to only slightly less than 1.2 seconds:

```
$ python -m timeit -s 'c = 396097; d = 369353; p = 691'  '(c**d) % p'
10 loops, best of 3: 1.11 sec per loop
$ python -m timeit -s 'c = 396097; d = 369353; q = 701'  '(q**d) % q'
10 loops, best of 3: 382 msec per loop
```

* Is there a way to speed up this, in particular by leveraging the CRT properties? Well, since $$p,q$$ are prime, we know that $$c^{p-1}\equiv 1 {\pmod{p}}$$ and $$c^{q-1}\equiv 1 {\pmod{q}}$$. So **at worst** we'll have to compute $$c^{p-1},c^{q-1}$$ instead of a much higher power $$c^d$$, meaning that we can the base $$c$$ by $$p$$ and $$q$$, respectively. Using this reduction already gives us a speedup of about a factor of 4, as it turns out:

```
$ python -m timeit -s 'c = 396097; d = 369353; p = 691'  '((c%p)**d) % p'
10 loops, best of 3: 233 msec per loop
$ python -m timeit -s 'c = 396097; d = 369353; q = 701'  '((c%q)**d) % q'
100 loops, best of 3: 10.2 msec per loop
```

* But we can do even better than that! Since $$p$$ and $$q$$ are primes and we know that $$c^{p-1}\equiv 1 {\pmod{p}}$$ and $$c^{q-1}\equiv 1 {\pmod{q}}$$, we can reduce the exponents. For instance, if we have $$x\equiv c^d {\pmod{p}}$$, then we can express this as $$x\equiv c^{(p-1)\times t + r=d} {\pmod{p}}$$ or $$x\equiv c^{(p-1)\times t}c^r {\pmod{p}}$$ because $$c^{(p-1)\times t} {\pmod{p}}$$ is 1. Likewise, we can apply the same mathematical trick for $$x\equiv c^d {\pmod{q}}$$ to reduce the exponent here. Now this gives us even more speed up:

```
$ python -m timeit -s 'c = 396097; dP = 203; p = 691'  '((c%p)**dP) % p'
100000 loops, best of 3: 3.55 usec per loop
$ python -m timeit -s 'c = 396097; dQ = 453; q = 701'  '((c%q)**dQ) % q'
100000 loops, best of 3: 4.89 usec per loop
```

* So in total, rather than spending 1.2 seconds to compute $$c=e^d {\pmod{n}}$$, we need only roughly 9 **micro**seconds (!) to compute the above expressions $$c {\pmod{p}}^{dP} {\pmod{p}}$$ and $$c {\pmod{q}}^{dQ} {\pmod{q}}$$. It turns out that $$a_1 = c {\pmod{p}}^{dP} {\pmod{p}} = 471$$ and $$a_2 = c {\pmod{q}}^{dQ} {\pmod{q}} = 451$$.

* The last step for actually calculating the message $$m$$ is to reconstruct it from the values $$a_1$$ and $$a_2$. Without going in too much mathematical details (and explaining why this is the case), the easiest way to do this is based on the so-called _Garner's formula_:

$$
x = (((a_1-a_2)(q^{-1}\pmod{p})) \pmod{p})\cdot q + b.
$$

or, expressed in our Python code, as:

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

* which gives us:

```
[*] a1= 471, a2 = 451
[*] qInv = 622
[*] m = 1853, m_d = 1853, m_g = 1853
```

* To summarise, assuming we have to compute exponentiations for $$ x^s \pmod{n} $$, the exponent $$s$$ can be up to $$k$$ bits long. This requires about $$3k/2$$ multiplications modulo $$n$$. Using the CRT representation, each multiplication is less work, but there is also a second saving. We want to compute $$(x^s\pmod{p}, x^s\pmod{q})$$. When computing module $$p$$, we can reduce the exponent $$s$$ modulo $$(p-1)$$, and similarly modulo $$q$$. So we only have to compute $$(x^{s\pmod{p-1}}\pmod{p}, x^{s\pmod{q-1}}\pmod{q})$$. Each of the exponents is only $$k/2$$ bits long and requires only $$3k/4$$ multiplications. Instead of $$3k/2$$ multiplications modulo $$n$$, we now do $$2\cdot 3k/4 = 3k/2$$ multiplications modulo one of the primes. This saves a factor 3-4 in computing time in a typical implementation.

* The only cost of using the CRT is the additional software complexity and the necessary conversions. If you do more than a few multiplications in one computation, the overhead of these conversions is worthwhile. Most textbooks only talk about the CRT as an implementation technique for RSA. We find that the CRT representation makes it much easier to understand the RSA system.

# References
* [Youtube Video on RSA and CRT by Jeff Suzuki](https://www.youtube.com/watch?v=6ytuvahX1tQ)
* Practical crypto book
* wikipedia article
* http://www.di-mgt.com.au/crt_rsa.html
* https://docs.python.org/2/library/timeit.html
* https://en.wikipedia.org/wiki/List_of_prime_numbers
* 