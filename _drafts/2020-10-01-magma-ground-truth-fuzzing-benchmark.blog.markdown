---
layout: post
title:  "Benchmarking at 1300 °C"
date:   2020-10-01 20:15:14 +0200
categories: infosec fuzzing vulnerability-discovery
---

# Hot, Hotter, Magma 
Molten or semi-molten natural material that all igneous rocks are made of is called Magma. It results from the melting of the Earth's mantle or crust. Most magmas are in the range of 700 °C to 1300 °C (equivalent 1300 °F to 2400 °F), some rare ones can reach temperatures as hot as 1600 °C [1][wikipedia-magma].

Magma is also [a collection of popular open-source libraries](https://hexhive.epfl.ch/magma/) created by the [EPFL's HexHive team](http://hexhive.epfl.ch/) for evaluating and comparing [fuzzer](https://www.fuzzingbook.org/html/Fuzzer.html) performance. To this end, the HexHive security researchers *front-ported* bugs from previous bug reports to the latest versions of these libraries. 

For each ported bug, the researchers added instrumentation source code to collect the ground truth information about bugs reached (i.e., cases where the buggy code is executed) and triggered (i.e., cases where the fault condition is satisfied by the input) [2][arxiv-paper]. Such an instrumentation allows to measure the *real-world* performance of a fuzzer.

# What's the problem? What am I trying to solve?
Make It Relevant - explain your motivation, outline your purpose


# Reading Git Patches

A Git patch encodes the line-by-line difference between two text files. It describes how to turn one file into another, and is asymmetric: the patch from file1 to file2 is not the same as the patch for the other direction. The patch format uses context as well as line numbers to locate differing file regions, so that a patch can often be applied to a somewhat earlier or later version of the first file than the one from which it was derived, as long as the applying program can still locate the context of the change [3][orreily-git-patch]. 

The terms “patch” and “diff” are often used interchangeably, although there is a distinction, at least historically. A diff only need show the differences between two files, and can be quite minimal in doing so. A patch is an extension of a diff, augmented with further information such as context lines and filenames, which allow it to be applied more widely. These days, the Unix diff program can produce patches of various kinds.

Here's an example:

```bash
paul@terminus:~/Temp/test-git-diff$ git diff hello.c 
diff --git a/hello.c b/hello.c
index dc46521..8a3a9a7 100644
--- a/hello.c
+++ b/hello.c
@@ -1,6 +1,6 @@
 #include <stdio.h>
 
 int main(){
- printf("Hello World!\n");
+ printf("Hello Digital Physics!\n");
  return 0;
 }
paul@terminus:~/Temp/test-git-diff$
```





# How to measure right?
3. Make It Relatable - build on more familiar concepts in small steps
4. Make It Clear, Concise, and Consistent - remove roadblocks to understanding

# Summary
5. Make It Memorable - repeat key concepts and end with a bang




Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[wikipedia-magma]: https://en.wikipedia.org/wiki/Magma
[arxiv-paper]: https://arxiv.org/abs/2009.01120
[orreily-git-patch]: https://www.oreilly.com/library/view/git-pocket-guide/9781449327507/ch11.html

[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
