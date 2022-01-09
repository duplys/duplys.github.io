---
layout: post
title:  "Convenient SSH: Public Key-based Authentication and Memorable Aliases for Remote Hosts"
date:   2022-02-07 22:04:24 +0100
categories: programming raspberrypi
---

<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

# Introduction
This post describes how to simplify remote maintenance via SSH by configuring SSH to use:
1. public-key authentication to eliminate the need to type in a password during each log in, and
2. convenient aliases for the individual remote hosts (in order to avoid typing in the IP address during each log in).

In my case, I'm using this to simplify the maintenance of the individual Raspberry Pis in my [DeepPi computing cluster](https://duplys.github.io/linux/rpi/raspberry-pi/microk8s/nginx/kubernetes/2020/04/21/installing-edge-on-raspberry-pi-4.blog.html). 

# Enabling Public Key-based Authentication
In addition to password-based authentication (and several more authentication options), SSH supports public key-based authentication. 

Public key authentication is based on public-key cryptography where encryption and decryption are performed using two distinct keys: the so-called private key for encryption and the so-called public key for decryption. Public key cryptoschemes are designed in such a way that it is computationally unfeasible to derive the decryption key (i.e., the private key) from the encryption key (i.e., the public key). For public key-based `ssh` authentication, each user creates their own unique public/private key pair (for all practical purposes, the uniqueness of the key pair is ensured by the method used to generate it). This is done by running the `ssh-keygen` program which stores the public/private key pair in `~/.ssh/` directory on the user's machine. 

The names of the files where the public and private keys are stored depend on the cryptographic primitives used. For instance, for RSA the public key is stored in `~/.ssh/id_rsa.pub` and the private key is stored in `~/.ssh/id_rsa`; for ECDSA the public key is stored in `~/.ssh/id_ecdsa.pub (ECDSA)` and the private key is stored in `~/.ssh/id_ecdsa (ECDSA)`.

In the next step, the **public** key is must be copied into the `~/.ssh/authorized_keys` to the `ssh` **server**. As a result, the `ssh` server knows the public key, and only the user knows the private key. The `authorized_keys` file corresponds to the conventional `~/.rhosts` file, and has one key per line, though the lines can be very long. After this, the user can log in without giving the password.

The file `~/.ssh/authorized_keys` on the SSH server lists the public keys that are permitted to log in. When the user logs in, the `ssh` program tells the server which key pair it would like to use for authentication. The client proves that it has access to the private key and the server checks that the corresponding public key is authorized to accept the account.

## Example
This examples assumes that the public/private key pair is already created using `ssh-keygen`. This is what the content of the `~/.ssh` directory look like:

```bash
$ ls ~/.ssh/
id_rsa  id_rsa.pub  known_hosts
$ 
```
Copy the RSA public key to clipboard:

```bash
$ cat ~/.ssh/id_rsa.pub | xclip -sel clipboard
```

On the remote host (i.e., on the RPi), open the `~/.ssh/authorized_keys` file and paste the public key. Logging in next time will not prompt for the password:
```
ubuntu@kasparov:~$ exit
logout
Connection to 192.168.178.66 closed.
paul@terminus:~$ ssh ubuntu@192.168.178.66
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 5.3.0-1042-raspi2 aarch64)
 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed Jan  5 15:57:00 UTC 2022

  System load:  0.35                Users logged in:        0
  Usage of /:   30.4% of 114.04GB   IP address for eth0:    192.168.178.66
  Memory usage: 33%                 IP address for docker0: 172.17.0.1
  Swap usage:   0%                  IP address for cni0:    10.1.79.1
  Processes:    181

  => There is 1 zombie process.

* Super-optimized for small spaces - read how we shrank the memory
  footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

95 packages can be updated.
1 update is a security update.

New release '20.04.3 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

Your Hardware Enablement Stack (HWE) is supported until April 2023.

Last login: Wed Jan  5 15:47:17 2022 from 192.168.178.21
ubuntu@kasparov:~$ 
```

# Setting up Memorable Aliases for Remote Hosts
To avoid typing `ssh <username>@<IP address>` at every log in, SSH allows to create convenient, memorable aliases for individual hosts in `~/.ssh/config`. As a minimum, `HostName` must be specified for the real remote host to log into. `HostName` can also be an IP address. If the usernames on the remote host and on the local host are different, `User` must be set to the username on the remote host.

## Example
Edit `~/.ssh/config` and add:

```
Host kasparov
    HostName 192.168.178.66
    User ubuntu
```
to be able to login to `192.168.178.66` as user `ubuntu` simply by typing:

```bash
$ ssh kasparov
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 5.3.0-1042-raspi2 aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri Jan  7 08:31:08 UTC 2022

  System load:  0.41                Users logged in:        0
  Usage of /:   31.1% of 114.04GB   IP address for eth0:    192.168.178.66
  Memory usage: 41%                 IP address for docker0: 172.17.0.1
  Swap usage:   0%                  IP address for cni0:    10.1.79.1
  Processes:    196

  => There is 1 zombie process.

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

95 packages can be updated.
1 update is a security update.

Your Hardware Enablement Stack (HWE) is supported until April 2023.

Last login: Wed Jan  5 16:09:12 2022 from 192.168.178.21
ubuntu@kasparov:~$ 
```

# References
1. `ssh` manpage
2. `ssh_config` manpage
3. https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server
4. https://www.ssh.com/academy/ssh/authorized-keys-file