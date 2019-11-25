# Topics for Future Posts
* Automotive Grade Linux (UCB 7.0)
* GHIDRA (NSA's reverse engineering toolkit)
* Ubuntu is Common Criteria EAL2 certified
* Linux Kernel 5.0: cipher Adiantum from/by Google for fast encryption on embedded devices
* SETI @ home
* FOSDEM 2019 videos + commentaries
* Secure Boot in Linux 5.0: Machine Owners Key (Shim boot loader)
* `mitm` proxy (test drive with a simple Docker application like having `mitm` between the host browser and the actual Docker application)
* The open source tool `tabula` for extracting csv data from pdf
* micro-project: learning a crypto-book using machine learning to classify crypto papers
* the tool `watchngo` 1.2.1 for the monitoring of files (https://github.com/Leryan/watchngo)
* `bpfilter` (https://lwn.net/Articles/747551)
* **the open source SIEM solution** `graylog` (https://www.graylog.org)
* Bundesregierung Sicherheitsgesetz 2.0 SiG2.0
* ISO 2700XX
* Any EU norm or standard for security


# Building the Blog

```shell
$ jekyll build
Configuration file: /Users/hslab/Repositories/duplys.github.io/_config.yml
            Source: /Users/hslab/Repositories/duplys.github.io
       Destination: /Users/hslab/Repositories/duplys.github.io/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
                    done in 1.197 seconds.
 Auto-regeneration: disabled. Use --watch to enable.
```

# Running locally

```shell
$ jekyll serve
Configuration file: /Users/hslab/Repositories/duplys.github.io/_config.yml
            Source: /Users/hslab/Repositories/duplys.github.io
       Destination: /Users/hslab/Repositories/duplys.github.io/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
                    done in 0.432 seconds.
 Auto-regeneration: enabled for '/Users/hslab/Repositories/duplys.github.io'
Configuration file: /Users/hslab/Repositories/duplys.github.io/_config.yml
    Server address: http://127.0.0.1:4000/
  Server running... press ctrl-c to stop.
```

# Math with Jekyll
To use math symbols in LaTeX notation in the blog posts, add the following link to the beginning of the post:

```html
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
```

Example:

```markdown
---
layout: post
title:  "Computing Square Roots"
date:   2019-01-15 19:54:49 +0100
categories: math numerical-analysis Heron Egypt Alexandria
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
The [Great Pyramid of Giza][wiki-giza], also known as the Pyramid of Cheops, is the oldest and largest of the three pyramids in the Giza pyramid complex located approximately 9 kilometres west of the Nile river at the old town of Giza, just about 13 kilometres southwest of the modern day Cairo. The pyramid is the oldest and most intact of the Seven Wonders of the Ancient World.
```