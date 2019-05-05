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