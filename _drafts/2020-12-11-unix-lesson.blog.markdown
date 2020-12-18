---
layout: post
title:  "Unix Lessons Learned"
date:   2020-12-11 20:02:35 +0100
categories: unix business
---

1. Make It Interesting - grab the reader's attention, but do it in an honest way
2. Make It Relevant - explain your motivation, outline your purpose
3. Make It Relatable - build on more familiar concepts in small steps
4. Make It Clear, Concise, and Consistent - remove roadblocks to understanding
5. Make It Memorable - repeat key concepts and end with a bang

Observations and, more important, questions while reading the book:
* what also sticks out (see page 20, Figure 1.11) is that there is a rather large number of small groups and departments. As an example, the Computing Techniques Research Department where people like Al Aho und Ken Thompson are employed consists of only 14 people, and the Computer Systems Research Department where Dennis Ritchie and Brian Kernighan are employed of only 6 (!) people. So the question is: does the size of the departments and groups have any impact on the research results/research outcomes?
* Bell Labs (BL) produced an incredible innovation with Unix -- how many servers are running Unix or Unix descendents?!
* While many many descendents stand on the shoulders of the Unix Giant, Unix itself stands on the shoulders of MULTICS. (so this might be interpreted as: the first system never gets to the stars; the first system is too progressive and it is therefore inevitably a fail)
* AT&T was not able to commercialize Unix -- why?
* Connected to the above: people across various universities (most notably Berkeley) recreated Unix at the interface level. But interface level is generic enough to not be patentable. So it seems like the really big inventions are so generic, i.e., so fundamental, that they cannot be patented and, as a result, are essentially a public good.
* Question related to the above: if you invent something really groundbraking, can you keep it to yourself? Or is it so generic that essentially everyone can replicate or copy it?
* ...
* Maybe the better way for BL would have been to base their services on the Unix OS?

# Definitions needed
1. Industrial research: a dedicated division within a large company
2. Peter Drucker's knowledge worker `=>` then derive knowledge business
3. Machine Learning and the problem of non-convex optimization

# Thought No 2
The Bell Labs story actually poses the question whether industrial research as such has a future. Is it reasonable -- from the economic point of view -- for a large company to have a dedicated research division?

My thesis is that, whatever knowledge business you take, the assets produced by its employees or its divisions have two kinds of value. They can have _sell value_ (which includes both direct and enables sales) or they can have _use value_ in the sense that they are useful for the business in the process or creating, manufacturing, maintaining products and business operations. 

My hypothesis: industrial research is not well suited for generating sell value. This is because to understand the needs of today's customer, dedicated research divisions are too far from the customers and from the market. The fancy ideas/the long shots, on the other hand, that dedicated research divisions like Bell Labs produce, are too far into the future, i.e., at that point in time, there are not really many customers (or maybe no customers at all) who have this specific need. On the other hand, dedicated industrial research is great at producing use value: at picking up new ideas from the outside and spreading them across their "mother" organization -- whatever the specific vehicle (report, consulting, MVPs, implementation, software, etc.). Without this, it is very easy to get blind-sided, also because the individual product divisions will naturally tend to optimize towards local minima. In other words, these highly specified divisions will incrementally improve the technologies they are working with, but they might completely miss a new technology or paradigm that can make their technology stack obsolete (Kodak is such an example).