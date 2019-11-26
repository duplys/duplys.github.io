---
layout: post
title:  "Negligible Thou Shalt Be"
date:   2017-04-25 21:59:47 +0100
categories: crypto math
---

<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

## Politics and Probability
In an [article covering the 2017 French presidential elections](http://www.cherwell.org/2017/04/23/le-pen-macron-and-melenchon-mark-a-turning-point-in-french-politics/), journalist Romain Civalleri predicted Jean-Luc Melechon, one of the underdog candidates, to have a _non-negligible_ probability of reaching the second round of the presidential elections. That's how we typically use the term 'non-negligible probability' in everyday life---it denotes something that is quite unlikely, yet not unthinkable.

While we (think we) are able to intuitively grasp the semantics of the term, it is actually still pretty fuzzy. To start with, how do we exactly define a _negligible_ probability? A probability of, say, 50% to win an election is certainly far from being negligible. Most of us would probably say the same of a 10% probability; after all, being the lucky winner 1 out of 10 times (on average) doesn't feel like something negligible (read: almost impossible). On the other hand, most of us would probably agree to consider a probability of 0.000001 % as negligible, at least for most everyday situations.

But then, where do we exactly draw the line? As an example, if we---based on our intuition---agree that a 10% probability is _non_-negligible (i.e. something that is _not_ unlikely), is a probability of 1% negligible since it is only one tenth of the former? Or do we have to go down to, say, 0.001%? And then again, what about a probability of 0.002% or 0.005% or 0.01%? Shall we still consider them to be negligible since they are so small (in everyday, intuitive terms) or should we consider them as non-negligible because they are (much) larger than, say, 0.001%? In the end, our intuitive interpretation of the term 'negligible probability' turns out to be very fuzzy...   

## Cryptography to the Rescue!
Cryptographers, it turns out, have a much more rigorous definition of negligible probability. However&mdash;as we will see in a minute&mdash;there's a little twist to the interpretation of the probability itself, at least compared to the everyday use of the term. Actually, it is not so much a twist, but rather the distinction we need to make between the terms _probability_ and _relative frequency_. 

[Relative frequency](http://mathworld.wolfram.com/RelativeFrequency.html) of an event is the ratio of its absolute frequency, i.e. the number of times the event occurred in an experiment, to the total number of possible events in that experiment. In other words, it is a very practice-oriented concept describing the fraction of time an event actually occurred.

As an example, assume we perform an experiment by rolling a six-sided dice. Possible events in this experiment&mdash;i.e. the data points in the frequency distribution&mdash;are 1, 2, 3, 4, 5, and 6. If we roll the dice $$n$$ times and throw a 6 $$n_6$$ times, then the relative frequency $$h_6$$ of throwing a 6 is:

$$
\frac{n_6}{n} = h_6
$$

For the above formula, you can immediately see that the relative frequency is a _number_ (more precisely, a real number $$h_6 \in \mathbb{R}$$). Relative frequency of an event describes what fraction of the time that event actually occurred. In the long run, the relative frequency will be close to the (theoretical) probability.

In contrast, the term probability [is actually defined](https://en.wikipedia.org/wiki/Bronshtein_and_Semendyayev) as a real-valued _function_ over the set $$A$$ of all possible outcomes $$A_i$$. As a result &mdash; based on the notion of a function&mdash;we can view probability as a function of some input parameter $$n$$.

For example, we can talk not only about the probability of throwing a 6 using a six-sided dice, but also about the probability of throwing a 6 using an $$n$$-sided dice. That, in fact, makes a huge difference: while we can approximate the former by determining its relative frequency, we cannot express the later as a _number_, i.e. we cannot express it using the concept of the relative frequency; the latter can only be expressed using the notion of a function as:

$$
P_6(n) = \frac{1}{n}
$$

It turns out that the notion of a function is needed to come up with a meaningful definition of a negligible probability. 

A _negligible_ function is a function that approaches zero faster than the reciprocal of any polynomial. In other words, a positive function is negligible if and only if it grows asymptotically no faster than the reciprocal of any positive polynomial [(University of Tartu MathWiki)](http://mathwiki.cs.ut.ee/asymptotics/06_the_negligible_the_noticeable_and_the_overwhelming). We can put this more formally by saying that a function _f_ is negligible if for _every_ polynomial $$p(\cdot)$$ there exists an $$N$$ such that for all integers $$n > N$$ it holds that 

$$
f(n) < \frac{1}{p(n)}.
$$

Since the definition above might by confusing at a first glance, let's visualise a couple of selected functions to see how these behave.

_**TODO: include a figure showing selected functions' behaviour**_  

Analogous to negligible functions, cryptographers call a probability _negligible_ if it is asymptotically smaller than the term $$1/p(n)$$ for _every_ polynomial $$p$$ [(Katz & Lindell,2008)](https://www.amazon.de/Introduction-Modern-Cryptography-Principles-Protocols/dp/1584885513/ref=sr_1_fkmr0_2?s=books-intl-de&ie=UTF8&qid=1497467070&sr=1-2-fkmr0&keywords=Introduction+to+Modern+Cryptography+first+edition). Cryptographers typically consider probability being negligible in the _security parameter_ of a given scheme. As an example, a symmetric encryption scheme is considered to be (computationally) secure if the probability that any efficient attack&mdash;i.e., any attack better than brute-force&mdash;succeeds, is negligible in the size (typically in bits) of the secret key used by that scheme.

_**TODO: refer to the example from the introduction and compare the intuitive meaning of negligible probability with it's actual mathematical definition**_ _**EDIT FROM HERE**_: So if you compare the math with the example from the introduction, then the probability to win the election should be defined w.r.t. to the number of /votes/ ...  



# Getting Specific
_**REVIEW FROM HERE ON !!!**_ So, based on the definition of the negligible probability above, what does that definition actually mean or imply? For instance, is the probability of throwing a 6 using an $$n$$-sided dice negligible or not? Well, that is easy to verify. To prove that it is non-negligible it is sufficient to find a polynomial that approaches zero faster than $$1/n$$ for every $$n$$. And this can be trivially accomplished by choosing the polynomial $$p(n) = n^2 + 1$$. Obviously, $$1/p(n) = n^2 + 1$$ will approach zero faster than $$1/n$$. _**PLOT A GRAPH!!!!!!!!!**_

**Continue on the line above**
  
To come up with a meaningful definition, This is needed in order to come up with a meaningful definition. it, which we will cover in a minute. 

* The main thing to spot here is the asymptotic notion; 
* A more formal definition (given in [(Katz & Lindell, 2008)](https://www.amazon.de/Introduction-Modern-Cryptography-Principles-Protocols/dp/1584885513/ref=sr_1_fkmr0_2?s=books-intl-de&ie=UTF8&qid=1497467070&sr=1-2-fkmr0&keywords=Introduction+to+Modern+Cryptography+first+edition)) is:

A function

* [Jonathan Katz, Yahuda Lindell "Introduction to Modern Cryptography"](https://www.amazon.de/Introduction-Modern-Cryptography-Principles-Protocols/dp/1584885513/ref=sr_1_fkmr0_2?s=books-intl-de&ie=UTF8&qid=1497467070&sr=1-2-fkmr0&keywords=Introduction+to+Modern+Cryptography+first+edition)
* What is the definition?
* Who was the first to define negligible probability? Why did they do that? Why did they need this notion?

* /when does it came/ However, it was not until xxxx that Mihir Belare introduced a rigorous mathematical definition for that [reference to the paper].

* [K&L] we equate the notion of 'small probability of success' with success probabilities _smaller than any inverse polynomial in $$n$$_, meaning that for every constant $$c$$ the adversary's success probability is smaller than $$n^{-c}$$ for large enough values of $$n$$. 
* [K&L] In the same way that we consider polynomial running times to be feasible, we consider inverse-polynomial probabilities to be significant. Thus, if an adversary could succeed in breaking a cryptographic scheme with the probability of $$1/p(n)$$ for some (positive) polynomial $$p$$, the scheme would not be considered secure.
* However, if the probability that the scheme can be broken is asymptotically smaller than $$1/p(n)$$ for _every_ polynomial $$p$$, then we consider the scheme to be secure. This is due to the fact that the probability of adversarial success is so small that it is considered uninteresting.
* We call such probabilities of success _negligible_, and have the following definition:
* A function $$f$$ is negligible if for every polynomial $$p(\cdot )$$ there exists an $$N$$ such that for all integers $$n > N$$ it holds that $$f(n) < \frac{1}{p(n)}$$. 
* An equivalent formulation of the above is to require that for all constants $$c$$ there exists an $$N$$ such that for all $$n > N$$ it holds that $$f(n) < n^{-c}$$.\\

## Learning by Example
* the functions $$2^{-n}$$, $$2^{-\sqrt{n}}$$, $$n^{-\log{n}}$$ are all negligible. 
* however, these three functions approach zero at very different rates
* To demonstrate this, we will show for what values of $$n$$ each function is smaller than $$10^{-6}$$
* $$2^{20} = 1...$$ and thus for $$n > 20$$ we have that $$2^{-n} < 10^{-6}$$
* $$2^{\sqrt{400}} = 1...$$ and thus for $$n \geq 400$$ we have that $$2^{-\sqrt{n}} < 10^{-6}$$
* $$32^{5} = 33...$$ and thus for $$n \geq 32$$ we have that $$n^{-\log{n}} < 10^{-6}$$
* insert the Python code snippets and the graphs of the above functions!

## So What's the Trick? (Reflecting on what has been said)
* you don't have a fixed number; rather, it's a function of a parameter $$n$$
* if I only make $$n$$ large enough, the probability $$p(n)$$ will be smaller than $$1/p(n)$$ for any polynomial $$p$$
* asymptotic behaviour!!! Big O notation [Wikipedia: Big O notation is a mathematical notation that describes the limiting behavior of a function when the argument tends towards a particular value or infinity. It is a member of a family of notations invented by Paul Bachmann,[1] Edmund Landau,[2] and others, collectively called Bachmann–Landau notation or asymptotic notation.](https://en.wikipedia.org/wiki/Big_O_notation#Related_asymptotic_notations)
* in cryptographer's view, negligible probability is not a number, it is a function.
* on a more abstract level, it says something about the behaviour of the probability depending on some parameter $$n$$ 

## Bird's View on Negligible Probability
* what is somewhat funny is that the two classic approaches to probability (before Chebychev introduced an axiomatic definition) are actually quite /funny/...
  * in the frequentist approach, the probability is basically the expected value (mittlere haeufigkeit) when you repeat the experiment for a (very) large number of times. On the technical side, you could say that according to the frequentists interpretation of probability, it is an approximation to the law of large numbers.
  * however, the Bayesian approach to probability is to interpret it as the degree of belief. More precisely, the probability in the Bayesian concept is adjusted based on the evidence that is presented to the observer (or a mathematician ;-) Hence, in a certain (very?) abstract sense, the Bayesian interpretation of what is probability is actually a function rather than a number.
* one of the things interesting enough to discuss here is this: the frequentist approach seems to fit well to continuous functions because the frequentist approach essentially favours /stetige Funktionen/. On the other hand, the Bayes approach allows the likelihood of an event to behave /unstetig/---the probability due to Bayes could jump up and down based on the evidence presented to the observer. 

## So What?
* Q. what do we need the notion of negligible probability for? A ([K&L]): computational security -> ... -> modern cryptography allows schemes that can be broken with a very small probability to still be considered 'secure'. If the probability that the scheme can be broken is asymptotically smaller than $$1/p(n)$$ for _every_ polynomial _p_, then the scheme is considered to be secure.

$$
c = m^e \pmod{n}
$$

where $$d$$ is such that $$e\cdot d \equiv 1 \pmod{mod(p−1)\cdot (q−1)}$$.
 
```
$ python -m timeit -s 'c = 396097; d = 369353; n = 484391'  'm = (c**d) % n'
10 loops, best of 3: 1.11 sec per loop
``` 

# References
* [Mihir Bellare "A Note on Negligible Functions"](https://eprint.iacr.org/1997/004.pdf)
* [Jonathan Katz, Yahuda Lindell "Introduction to Modern Cryptography"](https://www.amazon.de/Introduction-Modern-Cryptography-Principles-Protocols/dp/1584885513/ref=sr_1_fkmr0_2?s=books-intl-de&ie=UTF8&qid=1497467070&sr=1-2-fkmr0&keywords=Introduction+to+Modern+Cryptography+first+edition)
* [A turning point in French politics](http://www.cherwell.org/2017/04/23/le-pen-macron-and-melenchon-mark-a-turning-point-in-french-politics/)
* [Answer on Cryptography Stack Exchange](https://crypto.stackexchange.com/a/25460/5131)
* [Comparing relative frequency and probability](http://www.casio.edu.shriro.com.au/products/fx9860gau/pdf/relfrequency.pdf)
* [Weisstein, Eric W. "Relative Frequency." From MathWorld--A Wolfram Web Resource.](http://mathworld.wolfram.com/RelativeFrequency.html)
* [The negligible, the noticeable and the overwhelming](http://mathwiki.cs.ut.ee/asymptotics/06_the_negligible_the_noticeable_and_the_overwhelming?s[]=negligible)
* [Cryptography StackExchange "How to calculate if probability is negligible or not"](https://crypto.stackexchange.com/questions/25440/how-to-calculate-if-probability-is-negligible-or-not)
