---
layout: post
title:  "How Does RSA Key Generation Work?"
date:   2021-07-26 21:17:46 +0200
categories: linux tools experiments
---


# How does `ssh-keygen` work?
* And then, the next question is: "Why is the RSA key generation, especially finding the primes, is so fast?"


# Setting up VS Code to Look Deeper Under the Hood

We first need to setup VS Code to work with C++. [This Microsoft tutorial](https://code.visualstudio.com/docs/cpp/config-linux) describes how to use C++ on Linux in VS Code including how to install `g++` and other things. 

Important to know: when you open VS Code in the current working directory 

The code . command opens VS Code in the current working folder, which becomes your "workspace". As you go through the tutorial, you will create three files in a .vscode folder in the workspace:

* tasks.json (compiler build settings)
* launch.json (debugger settings)
* c_cpp_properties.json (compiler path and IntelliSense settings


: https://code.visualstudio.com/docs/cpp/customize-default-settings-cpp

https://code.visualstudio.com/docs/cpp/c-cpp-properties-schema-reference





You first need to setup VSCode: https://code.visualstudio.com/docs/cpp/customize-default-settings-cpp

https://code.visualstudio.com/docs/cpp/c-cpp-properties-schema-reference



# What's below the surface?
* ssh-keygen uses OpenSSH
* what does OpenSSH use to generate the keys, which function?
* which OpenSSL function is used???

# Getting OpenSSL
Go to https://github.com/openssl/openssl, go to "tags" and download tar.gz for 3.0.1

On the command line:

```bash
$ tar -xvzf lasfjsdlfk.tar.gz
$ cd <openssl-openssl-3.0.1>
$ ./Configure
$ make
$ make test
```

Nothing more, because we don't want to install the lib, just debug.


```bash

$ make test
make depend && make _tests
make[1]: Entering directory '/home/paul/Temp/openssl-openssl-3.0.1'
make[1]: Leaving directory '/home/paul/Temp/openssl-openssl-3.0.1'
make[1]: Entering directory '/home/paul/Temp/openssl-openssl-3.0.1'
( SRCTOP=. \
  BLDTOP=. \
  PERL="/usr/bin/perl" \
  FIPSKEY="f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813" \
  EXE_EXT= \
  /usr/bin/perl ./test/run_tests.pl  )
00-prep_fipsmodule_cnf.t .. skipped: FIPS module config file only supported in a fips build
Files=1, Tests=0,  0 wallclock secs ( 0.01 usr  0.00 sys +  0.09 cusr  0.01 csys =  0.11 CPU)
Result: NOTESTS
01-test_abort.t .................... ok   
01-test_fipsmodule_cnf.t ........... skipped: Test only supported in a fips build
01-test_sanity.t ................... ok   
01-test_symbol_presence.t .......... ok   
01-test_test.t ..................... ok   
02-test_errstr.t ................... ok  

...

99-test_fuzz_ct.t .................. ok   
99-test_fuzz_server.t .............. ok   
99-test_fuzz_x509.t ................ ok   
All tests successful.
Files=242, Tests=3281, 277 wallclock secs ( 6.34 usr  0.35 sys + 242.27 cusr 27.63 csys = 276.59 CPU)
Result: PASS

```





