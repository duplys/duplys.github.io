---
layout: post
title:  "On Software Diversity as a Countermeasure Against Attacks"
date:   2019-02-17 17:18:36 +0100
categories: security software
---
In [Griffor et al][griffor], I stumbled upon the idea set forth by Tunc, Hariri, and Battou that diversity should be used to avoid the _software monoculture problem_ where one attack vector can successfully attack many instances of the same software module.

While this seems to be a reasonable proposition at first, I think the authors underestimate the effort needed to maintain the software. As an example, if I have 3 implementations of the same functionality in 3 different programming languages, my maintenance effort needs to be 3 times as high.

Without having more people to maintain the software, I will end up having much less time to review and test the code of each of the 3 code bases. As a result, while the 3 implementations will not have many identical bugs, the likelihood of bugs in each individual code base will be higher.

As a consequence, instead of having to maintain more code, it is very reasonable to have just one code base and verify this code base with the ultimate goal to remove all bugs.


Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[griffor]: Edward Griffor (Editor) "Handbook on System Safety and Security"
[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
