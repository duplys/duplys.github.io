---
layout: post
title:  "Mixed Content (In)Security"
date:   2020-01-20 20:28:00 +0100
categories: security, tls, https, web
---

<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

# Things to cover
* What is the problem? Show a minimal web site example with something like this (but WITHOUT `https`, rather `http`) in an HTTPS connection

```html
<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
```
and see what the Firefox console shows (like Blocked mixed content). Add a screenshot & explain what it shows.

* What is mixed content? Explain!
* Why am I getting this error?
* What should I do about it? How can I fix it?
* How can I fix it in OpenCart?

# A Practical Example
* You have a reverse proxy passing the traffic to a backend service

# Reverse Proxy
* What is a reverse proxy?

# Reverse Proxy Using Apache
