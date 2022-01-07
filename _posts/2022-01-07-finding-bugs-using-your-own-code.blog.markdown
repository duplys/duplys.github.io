---
layout: post
title:  "Finding Bugs Using Your Own Code"
date:   2022-01-07 22:04:24 +0100
categories: security programming
---

<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

Recent [USENIX paper "Finding Bugs Using Your Own Code: Detecting Functionally-similar yet Inconsistent Code"](https://www.usenix.org/conference/usenixsecurity21/presentation/ahmadi) by Ahmadi, Fakhani, Williams and Lu describes a interesting machine learning-based method for detecting sofware bugs. 

Unlike similar approaches, the method does not require external datasets or code samples for training, i.e., no other code containing known bugs. Instead, it learns from the very codebase on which the bug detection is to be performed and therefore does not require cumbersome gathering and cleansing of training samples. 

The method is based on the idea of _code inconsistencies_. A set of code snippets is called inconsistent if the snippets implement similar logic, but some parts of their implementation differ in significant ways. As an example, absent bounds checks or use-after-free bugs can be found if the codebase contains non-buggy code snippets that are functionally similar as shown in the picture below (taken from the paper).

!["Code inconsistency"](/_img/code-inconsistency.png "Code inconsistency")

["Finding Bugs Using Your Own Code"](https://www.usenix.org/conference/usenixsecurity21/presentation/ahmadi) can be seen as a special case of anomaly detection. Anomaly detection has been successfully applied in the past for automated discovery of specific security vulnerabilities in software, e.g., for discovering missing checks by Fabian Yamaguchi et al in ["Chucky: Exposing Missing Checks in Source Code for Vulnerability Discovery"](https://www.researchgate.net/publication/258903333_Chucky_Exposing_Missing_Checks_in_Source_Code_for_Vulnerability_Discovery).

While the new method is bug-agnostic and doesn't need training data, its use nevertheless requires some effort on the part of the software developer as shown in the figure below (taken from the paper). First, you need to compile the C code into LLVM bitcode. You then need to perform intra-procedural data-flow analysis to extract code fragments that represent basic computations within a function. You then need to extract the program dependency graphs (PDGs) and simplify them&mdash;by omitting control dependency edges&mdash;to data dependency graphs (DDGs). Next, you need to perform two clustering steps: bag-of-nodes embedding for grouping functionally-similar code fragments and graph2vec embedding for finding fragments that are inconsistent with the rest of the same group. Finally, you need to perform the deviation analysis to identify inconsistencies that likely point to bugs.

!["FICS method"](/_img/fics_method.png "FICS method")

I'm wondering whether there is a simpler way to leverage the idea of code inconsistencies being a good proxy for bugs. One option would be to use the [Cobra (interactive) fast static code analyzer](https://github.com/nimble-code/Cobra). 

!["Cobra"](/_img/cobra_principle.png "Cobra")

[Cobra](https://github.com/nimble-code/Cobra) is a fast code analyzer that can be used to interactively probe and query up to millions of lines of code. The basic design of the tool is language-neutral, though a lot of query and rule libraries have been developed, and are included in the distribution, that target C or C-like languages. The original version of the tool (version 1.0) was developed at NASA/JPL and cleared for public release in April 2016. The current version (3.0) is a significantly extended version of the tool, released under the same license in June 2019.

!["Cobra use"](/_img/cobra_use.png "Cobra use")

[Cobra](https://github.com/nimble-code/Cobra) is fast because it only performs a lexical analysis. It builds a linked list of lexical tokens with annotations. The developer can then issue interactive queries and pattern matching commands. 

!["Cobra grep"](/_img/cobra_grep.png "Cobra grep")

Maybe a simpler alternative to ["Finding Bugs Using Your Own Code"](https://www.usenix.org/conference/usenixsecurity21/presentation/ahmadi) would be to:
1. list all the functions in a given code base
2. for every function, list all code snippets where it's used
3. (visually?) compare whether there are inconsistencies in how the function is called, e.g., whether an argument check is missing 
