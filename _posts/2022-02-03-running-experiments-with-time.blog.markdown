---
layout: post
title:  "Times Like These"
date:   2021-07-26 21:17:46 +0200
categories: linux tools experiments
---

# It's Times Like These `time` and `time` Again
>  It's times like these you learn to live again  
It's times like these you give and give again  
It's times like these you learn to love again  
It's times like these time and time again

[Foo Fighters &ndash; Times Like These](https://www.youtube.com/watch?v=rhzmNRtIp8k)

Reading about a song by a famous rock band would certainly be exciting. But a post on GNU/Linux `time`, a utility that is [part of Unix since late 1970's](https://en.wikipedia.org/wiki/Time_(Unix))? Seriously!? In my case it was a simple question about cryptography&mdash;how long does it take to generate an RSA key pair?&mdash;that led me to take another look at `time`. And boy did I underestimate the capabilities of this handy tool.

Last time I used `time` was during my university days. Reading the [man page](https://linux.die.net/man/1/ssh-keygen) now, I realized there were numerous things I was completely unaware of. Did you know that you can configure `time`'s output format, write (or append) its output to a file (for instance, to generate a `.csv` file for further processing), and measure much much more than just the execution time?

# The Keys, Please
Back to the the initial question: how long does it take to generate an RSA key pair? One way to answer this question is to measure the execution time of `ssh-keygen`, a utility to [generate, manage and convert authentication keys for `ssh`](https://linux.die.net/man/1/ssh-keygen). For `ssh-keygen`, the parameter `-t` specifies the type and parameter `-b` the number of bits in the key to create. For RSA keys, the minimum size is 1024 bits and the default is 2048 bits. So the simplest command to generate an RSA key is:

```bash
$ ssh-keygen -t rsa
```
With the above command, `ssh-keygen` generates the key and asks the user for a file in which to store the private key. The public key is stored in the file with the same name and the extension ".pub". `ssh-keygen` also asks for a passphrase. The user may choose an empty passphrase (just hit enter) to indicate no passphrase or choose a string of arbitrary length.

By default, the `ssh` per-user files are stored in `~/.ssh` directory. So a user wishing to use SSH with RSA public key authentication would invoke `ssh-keygen` to generate the files `~/.ssh/id_rsa` (private key) and `~/.ssh/id_rsa.pub` (public key). 

In our case, we don't want to overwrite the files in `~/.ssh/`. So we can use the `-f` parameter to pass `ssh-keygen` a dummy filename. In addition, because we want to time the `ssh-keygen` execution time, we need to prevent the program from asking for the passphrase. This can be done using the `-N` parameter for providing a new passphrase and giving it an empty string. Thus, creating a $B$-bit RSA key pair, writing the key into a dummy file and skipping the passphrase input can be done by issuing:

```bash
$ ssh-keygen -t rsa -b <B> -N '' -f rsa_key
```

# Format `time` Output
Parameter `-f` (or `--format`) together with a format string [controls which information `time` displays](https://man7.org/linux/man-pages/man1/time.1.html). The format string usually consists of _resource specifiers_ interspersed with plain text. A percent sign (`%`) in the format string causes the following character to be interpreted as a resource specifier. A backslash (`\`) can be used to escape a character, e.g., `\t` output a tab character, `\n` outputs a newline, and `\\` outputs a backslash. Other text in the format string is copied verbatim to the output. `time` accepts resource specifiers shown in the table below. 

| Specifier | Description                                                                                                                    |
| :-------  | :----------------------------------------------------------------------------------------------------------------------------- |
| %         | A literal `%`                                                                                                                  |
| F         | Number of major, I/O-requiring, page faults that occurred while the process was running                                        |
| I         | Number of file system inputs by the process                                                                                    |
| K         | Average total (data+stack+text) memory use of the process, in Kilobytes                                                        |
| M         | Maximum resident set size of the process during its lifetime, in Kilobytes                                                     |
| O         | Number of file system outputs by the process                                                                                   |
| P         | Percentage of the CPU that this job got (user + system times divided by the total running time)                                |
| R         | Number of minor, recoverable, page faults                                                                                      |
| S         | Total number of CPU-seconds used by the system on behalf of the process (in kernel mode), in seconds                           |
| U         | Total number of CPU-seconds that the process used directly (in user mode), in seconds                                          |
| W         | Number of times the process was swapped out of main memory                                                                     |
| X         | Average amount of shared text in the process, in Kilobytes                                                                     |
| Z         | System's page size, in bytes                                                                                                   |
| c         | Number of times the process was context-switched involuntarily (because the time slice expired)                                |
| e         | Elapsed real (wall clock) time used by the process, in seconds                                                                 |
| k         | Number of signals delivered to the process                                                                                     |
| p         | Average unshared stack size of the process, in Kilobytes                                                                       |
| r         | Number of socket messages received by the process                                                                              |
| s         | Number of socket messages sent by the process                                                                                  |
| t         | Average resident set size of the process, in Kilobytes                                                                         |
| w         | Number of times that the program was context-switched voluntarily, for instance while waiting for an I/O operation to complete |

Using the `-o` parameter and a filename we can write the resource usage statistics into a file instead of the standard error stream. The `-a` parameter can be used to append the statistics rather than overwriting the file.

# Automating the Measurement
For various reasons like involuntary context-switches or processor load, and especially with programs that have short execution times, a single execution time measurement is rarely accurate. Instead, we need to repeat each measurement several times and take the minimum value. The `bash` script below shows how this can be accomplished.  

```bash
#!/bin/bash

now=`date +%Y-%m-%d-%H-%M-%S`
logfile="log_${now}.csv"
echo ${logfile}

echo "key_bits, real_e, user_U, sys_S, ctx_switch_inv_c, ctx_switch_vol_w, page_faults_F, minor_page_faults_R, fs_inputs_I, fs_outputs_O, mem_used_K, unshared_stack_size_p, max_resident_set_size_M, avg_resident_set_size_t, percentage_cpu_P, proc_swapped_out_W, avg_shared_text_X, sys_page_size_Z, signals_to_process_k, socket_msgs_rec_r, socket_msgs_sent_s" > ${logfile} 

for (( b=2048; b<8192; b = b + 100 ));  
do
  printf "[*] generating ${b} bit keys "
  for (( i=0; i<20; i++));  
  do
    rm -f rsa_key*
    /usr/bin/time -a -o ${logfile} -f "${b}, %e, %U, %S, %c, %w, %F, %R, %I, %O, %K, %p, %M, %t, %P, %W, %X, %Z, %k, %r, %s" ssh-keygen -t rsa -b ${b} -N '' -q -f rsa_key
    printf "."
  done
  printf "\n"
done
```

The script first calls `date` with a format string to output "year-month-day-hour-minute-second" and uses this time stamp for a unique filename for the logfile. This way previous measurements will not be overwritten by a repeated invocation of the script. The script then writes the `csv` header line which will be useful later on, when the data is read for further processing, because we will be able since the columns because  when the `csv` data is read since this will allow us to name the data columns.

The script then iterates through RSA key bit lengths from 2048 to 8192 -- in steps of 100 bits -- and generates 20 keys for every bit length. `time` outputs a list of comma-separated values that are appended to the logfile. Note that `/usr/bin/time` must be used instead of the Bash command `time`, because the Bash command doesn't accept parameters.

Since the logfile is in `csv` format, it can be conveniently used for post-processing. As an example, Python's [Pandas framework](https://pandas.pydata.org/) for data analysis and manipulation has a [`pandas.read_csv()` function](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) to read a `csv` file into Panda's `DataFrame`. 


# `time` to Recap
Here are the main take-aways:

* `time` output is highly customizable, the format string is composed of _resource specifiers_ interspersed with plain text
*  `time` can display much much more than just the execution time
* using `-o` parameter, the output can be written to a file instead of the standard error stream
* the `-a` parameter can be used to append to rather than overwrite a file
* measurements should be repeated multiple times, and you should select either the minimum or compute the average to get a representative measurement
* you can use a shell script to perform the measurements and save them in a `csv` format for an easy post-processing