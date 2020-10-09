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

# Benchmark, anyone?
Let's say you came up with a shiny new method for finding security vulnerabilities in software. To convince yourself, you now want to test how well your method actually performs. Your method is, however, not a fuzzer. Can you still use Magma for your experiments? You bet! That's because the front-ported bugs in Magma are available as Git patches. Git patches allow you to precisely see where the corresponding bugs are in the source code and, in turn, whether your method is able to find them. You only need to know a few basics about Git patches. 

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

# Examples, please!
Let's take a look at [CVE-2018-13785](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-13785), an  integer overflow that leads to a divide by zero and, thus, a potential denial of service. The corresponding Git patch in Magma is located in `targets/libpng/patches/bugs/AAH001.patch` file. (Appendix A of the [Magma preprint paper](https://arxiv.org/pdf/2009.01120.pdf) contains a mapping of patches to CVE IDs).

The `AAH001.patch` file looks like this:

```bash
$ cat bugs/AAH001.patch 
diff --git a/pngrutil.c b/pngrutil.c
index 4db3de990..01c97dc37 100644
--- a/pngrutil.c
+++ b/pngrutil.c
@@ -3163,12 +3163,27 @@ png_check_chunk_length(png_const_structrp png_ptr, png_uint_32 length)
    if (png_ptr->chunk_name == png_IDAT)
    {
       png_alloc_size_t idat_limit = PNG_UINT_31_MAX;
+#ifdef MAGMA_ENABLE_FIXES
       size_t row_factor =
          (size_t)png_ptr->width
          * (size_t)png_ptr->channels
          * (png_ptr->bit_depth > 8? 2: 1)
          + 1
          + (png_ptr->interlaced? 6: 0);
+#else
+      size_t row_factor_l =
+         (size_t)png_ptr->width
+         * (size_t)png_ptr->channels
+         * (png_ptr->bit_depth > 8? 2: 1)
+         + 1
+         + (png_ptr->interlaced? 6: 0);
+
+#ifdef MAGMA_ENABLE_CANARIES
+      MAGMA_LOG("AAH001", row_factor_l == ((size_t)1 << (sizeof(png_uint_32) * 8)));
+#endif
+
+      size_t row_factor = (png_uint_32)row_factor_l;
+#endif
       if (png_ptr->height > PNG_UINT_32_MAX/row_factor)
          idat_limit = PNG_UINT_31_MAX;
       else
```

The patch shows that a bug is located in the `pngrutil.c` file, in function `png_check_chunk_length` starting at line 3163. The lines starting with `+` constitute the bug. Indeed, according to the [CVE-2018-13785](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-13785) which corresponds to this patch, _"a wrong calculation of `row_factor` in the `png_check_chunk_length` function (pngrutil.c) may trigger an integer overflow and resultant divide-by-zero while processing a crafted PNG file, leading to a denial of service"_. Hence, using the Magma `*.patch` files you can easily locate the corresponding bugs. 

# TLDR; (Summary)
[Magma ground-truth fuzzing benchmark](https://hexhive.epfl.ch/magma/) is a collection of popular and diverse open-source libraries with 118 real-world *front-ported* bugs available in the form of Git patch files under `targets/<target_name>/patches/bugs/*.patch`. While the EPFL [HexHive team](http://hexhive.epfl.ch/#people) originally designed Magma for benchmarking fuzzer performance, it can be used to evaluate the effectiveness of any method for discovering security vulnerabilities in software.


[wikipedia-magma]: https://en.wikipedia.org/wiki/Magma
[arxiv-paper]: https://arxiv.org/abs/2009.01120
[orreily-git-patch]: https://www.oreilly.com/library/view/git-pocket-guide/9781449327507/ch11.html
