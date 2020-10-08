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


# Git Patch 101
A Git patch encodes the line-by-line difference between two text files. It describes how to turn one file into another, and is asymmetric: the patch from `file1` to `file2` is not the same as the patch for the other direction. The patch format uses context as well as line numbers to locate differing file regions so that a patch can often be applied to a somewhat earlier or later version of the first file than the one from which it was derived, as long as the applying program can still locate the context of the change [3][orreily-git-patch]. 

Here's an example of a git patch (or git diff) after I changed the argument to the `printf` function from `"Hello World!\n"` to `"Hello There!\n"`:

```bash
$ git diff hello.c 
diff --git a/hello.c b/hello.c
index dc46521..a00b40d 100644
--- a/hello.c
+++ b/hello.c
@@ -1,6 +1,6 @@
 #include <stdio.h>
 
 int main(){
- printf("Hello World!\n");
+ printf("Hello There!\n");
  return 0;
 }
$ 
```

The first line `diff --git a/hello.c b/hello.c` shows that the file being compared is `hello.c` (it's a single file and there are actually no directories `a` and `b` - it's just a convention).

The second line `index dc46521..a00b40d 100644` is the extended header line. In the Git index, `dc46521` and `a00b40d` are the blob IDs of the corresponding versions of the `hello.c` file. Finally, `100644` are the mode bits indicating the type of the `hello.c` file (standard file in this case). 

The next two lines

```bash
--- a/hello.c
+++ b/hello.c
```

is the traditional unified diff header that shows the files being compared (`hello.c` in our case).

The line `@@ -1,6 +1,6 @@` indicates the position of the difference section (also known as a "hunk") in the respective `hello.c` versions using the line number and the length. In our example, both in version `--- a/hello.c` and in version `+++ b/hello.c` the hunk starts at line 1 and extends for 6 lines (note the `-` and `+` signs in `@@ -1,6 +1,6 @@`).

What follows is the actual difference. The minus signs show lines present in version `a/hello.c` but missing in version `b/hello.c` and plus signs show lines missing in `a/hello.c` but present in `b/hello.c`. Thus, the difference shows that the line `printf("Hello World!\n");` was replaced by the line `printf("Hello There!\n");`.


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
