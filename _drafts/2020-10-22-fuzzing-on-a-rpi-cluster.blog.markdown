---
layout: post
title:  "Fuzzing on a homebrewn Raspberry Pi microk8s cluster"
date:   2020-10-22 20:50:18 +0200
categories: fuzzing security software
---

1. Make It Interesting - grab the reader's attention, but do it in an honest way
2. Make It Relevant - explain your motivation, outline your purpose
3. Make It Relatable - build on more familiar concepts in small steps
4. Make It Clear, Concise, and Consistent - remove roadblocks to understanding
5. Make It Memorable - repeat key concepts and end with a bang

To generate the date for the blog post, issue the following command:


# What I'm up to
I would like to setup an RPi `microk8s` cluster permanently running fuzzing of selected open source projects, i.e., 24/7. The fuzzers I want to use are:
* AFL
* AFL++
* hongfuzz
* libFuzzer
* ???

I want to package all these fuzzers as Docker containers. I want to run these fuzzer Docker containers as Kubernetes services. I want to have a controller -- maybe a cron job initially -- that passes the source code to the fuzzer Docker containers. 

But first let try it with plain Docker.

# Fuzzing stuff w/ Docker

## Fuzzing with hongfuzz
* ...
In the container:

```shell
root@09be76d9a4f5:/honggfuzz/examples/badcode/targets# make
root@09be76d9a4f5:/honggfuzz/examples/badcode/targets# honggfuzz -i ../inputfiles/ -x -- ./badcode1  ___FILE___
```

# Hongfuzz
Question: how do I fuzz with hongfuzz?

# Steps

```shell
paulduplys@Pauls-MBP hf % git clone https://github.com/google/honggfuzz.git
Cloning into 'honggfuzz'...
remote: Enumerating objects: 17, done.
remote: Counting objects: 100% (17/17), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 60470 (delta 6), reused 11 (delta 4), pack-reused 60453
Receiving objects: 100% (60470/60470), 187.22 MiB | 4.45 MiB/s, done.
Resolving deltas: 100% (32292/32292), done.
Checking out files: 100% (13041/13041), done.
paulduplys@Pauls-MBP hf % ls
honggfuzz
paulduplys@Pauls-MBP hf % ..
paulduplys@Pauls-MBP Temp % ls
ascii                      certics                    matthis-english            test-kubernetes-deployment weather
book-proposal-review       hf                         nginx.tar                  usenix
paulduplys@Pauls-MBP Temp % ..
paulduplys@Pauls-MBP ~ % ls
Desktop      Documents    Downloads    Library      Movies       Music        Pictures     Public       Repositories Temp         polar
paulduplys@Pauls-MBP ~ % cd Temp 
paulduplys@Pauls-MBP Temp % ls
ascii                      certics                    matthis-english            test-kubernetes-deployment weather
book-proposal-review       hf                         nginx.tar                  usenix
paulduplys@Pauls-MBP Temp % mv hf fuzzing
paulduplys@Pauls-MBP Temp % cd fuzzing 

-- snip --

paulduplys@Pauls-MBP honggfuzz % docker build -t hongfuzz .
Sending build context to Docker daemon  357.5MB
Step 1/6 : FROM ubuntu:rolling
rolling: Pulling from library/ubuntu
d72e567cc804: Pull complete 
0f3630e5ff08: Pull complete 
b6a83d81d1f4: Pull complete 
Digest: sha256:bc2f7250f69267c9c6b66d7b6a81a54d3878bb85f1ebb5f951c896d13e6ba537
Status: Downloaded newer image for ubuntu:rolling
 ---> 9140108b62dc
Step 2/6 : ENV DEBIAN_FRONTEND noninteractive
 ---> Running in b456e28a78fc
Removing intermediate container b456e28a78fc
 ---> 551174953dcf
Step 3/6 : RUN apt-get -y update && apt-get install -y     gcc     git     make     pkg-config 	libipt-dev 	libunwind8-dev 	binutils-dev && rm -rf /var/lib/apt/lists/* && rm -rf /honggfuzz
 ---> Running in a8cdbcc3a6a0
Get:1 http://archive.ubuntu.com/ubuntu focal InRelease [265 kB]
Get:2 http://security.ubuntu.com/ubuntu focal-security InRelease [107 kB]

-- snip --

cc -o hfuzz_cc/hfuzz-cc hfuzz_cc/hfuzz-cc.c libhfcommon/libhfcommon.a  -pthread -lm -L/usr/local/include -lunwind-ptrace -lunwind-generic -lunwind  -llzma -lopcodes -lbfd -lrt -ldl -lm -lipt -O3 -mtune=native -funroll-loops -std=c11 -I/usr/local/include -D_GNU_SOURCE -Wall -Wextra -Werror -Wno-format-truncation -Wno-override-init -I. -D_FILE_OFFSET_BITS=64 -D_HF_LINUX_INTEL_PT_LIB -finline-limit=4000 -D_HF_ARCH_LINUX  -D_HFUZZ_INC_PATH=/honggfuzz
cc -shared libhfuzz/fetch.o libhfuzz/instrument.o libhfuzz/linux.o libhfuzz/memorycmp.o libhfuzz/performance.o libhfuzz/persistent.o libhfcommon/files.o libhfcommon/log.o libhfcommon/ns.o libhfcommon/util.o  -pthread -lm -L/usr/local/include -lunwind-ptrace -lunwind-generic -lunwind  -llzma -lopcodes -lbfd -lrt -ldl -lm -lipt -o libhfuzz/libhfuzz.so
Removing intermediate container ab3ea4cbc4a8
 ---> 9ba2e77d1cce
Successfully built 9ba2e77d1cce
Successfully tagged hongfuzz:latest
paulduplys@Pauls-MBP honggfuzz %
```



# References
* https://github.com/google/honggfuzz/blob/master/docs/USAGE.md
* https://honggfuzz.dev
* https://twitter.com/robertswiecki/status/1085281251555192833?lang=en


You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

To add new posts, simply add a file in the `_posts` directory that follows the convention `YYYY-MM-DD-name-of-post.ext` and includes the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
