---
layout: post
title:  "Growing Your Applications: Adding Nodes to a microk8s Kubernetes Cluster"
date:   2020-06-20 13:41:33 +0100
categories: kubernetes microk8s raspberry-pi-cluster
---
 
![kubernetes-dashboard](/assets/japanese-garden.jpg)

With `microk8s` up and running, the next step is to add new nodes to the Kubernetes cluster. Adding nodes not only increases the cluster's computing resources, but also adds _redundancy_. Redundancy, in turn, increases the availability and reliability of the cluster because the Kubernetes Pods, e.g., the replicas of the same service, can be distributed over multiple hardware devices. Multiple hardware instances mean that failures can be tolerated. That's exactly the reason why the Kubernetes scheduler tries to ensure that Pods from the same application are distributed onto different machines.

This post is a step-by-step guide for adding new nodes to a `microk8s` Kubernetes cluster running on Raspberry Pi (RPi) microcomputers. In particular, we will discuss how to add RPi nodes running the Ubuntu 20.04 release. As you will see, Ubuntu 20.04 nodes require a little manual tweaking related to `cgroups` before you can actually use them in an `microk8s` Kubernetes cluster.

Note: In the remainder of this post, all shell commands are executed on the RPi minicomputers. For me, the most convenient way to manage these microcomputers is to `ssh` into them from my development laptop. In case you'd like to know how to enable `ssh`, [the official Raspberry Pi documentation on remote access via `ssh`](https://www.raspberrypi.org/documentation/remote-access/ssh/) is a good place to start.

Luckily for us, Kubernetes makes adding new nodes really easy. In case of `microk8s`, the shell command `microk8s add-node` generates a connection string and outputs a list of suggested `microk8s join` commands for adding new nodes to the current `microk8s` cluster. The cluster node on which this command is executed becomes the main node of the Kubernetes cluster and will host its control plane.

So, to get started, connect to the main Raspberry Pi|s (i.e., the RPi you have designated to become the main node of your Kubernetes cluster) and issue:

```shell
ubuntu@ubuntu:~$ microk8s add-node
Join node with: microk8s join 192.168.178.66:25000/ipySurdsIOGAlYyYQzzOOSlpUTEDNGfk

If the node you are adding is not reachable through the default interface you can use one of the following:
 microk8s join 192.168.178.66:25000/ipySurdsIOGAlYyYQzzOOSlpUTEDNGfk
 microk8s join 10.1.79.0:25000/ipySurdsIOGAlYyYQzzOOSlpUTEDNGfk
 microk8s join 172.17.0.1:25000/ipySurdsIOGAlYyYQzzOOSlpUTEDNGfk
ubuntu@ubuntu:~$ 
```

In the above output of the `microk8s add-node` command you see the string `ipySurdsIOGAlYyYQzzOOSlpUTEDNGfk` that is required for a new node to join the Kubernetes cluster. The output also gives multiple suggestions for the parameters of the `microk8s join` command, which is great if you should have any issues with your setup. (Note: the value of your token will be different since Kubernetes generates it individually for every cluster).

Connect to the RPi minicomputer that you want to add to the `microk8s` cluster. The `microk8s` software must be installed and configured on this RPi before you proceed. If that's not the case, check the ["Installing microk8s and nginx on Raspberry Pi 4" post](http://duplys.github.io/linux/rpi/raspberry-pi/microk8s/nginx/kubernetes/2020/04/21/installing-edge-on-raspberry-pi-4.blog.html) for a step-by-step installation guide.

If you installed the operating system on your Raspberry Pi from a standard Linux image (in my setup, I use the Ubuntu 20.04 image for my Raspberry Pi), you might want to change the hostname of your second Raspberry Pi device to something unique (otherwise, you will see multiple Kubernetes nodes all having the same name `ubuntu` later on in your Kubernetes dashboard/command line). Under Linux, you can change the hostname like this:

1. edit `/etc/hostname` and replace the current hostname with the new hostname
2. edit `/etc/hosts` and replace every occurrence of the current hostname with the new hostname
2. reboot the system by issuing `sudo reboot`

In my case, the hostname of the second RPi is `ubuntu-2`. To add the second RPi to the `microk8s` cluster, I need to `ssh` into `ubuntu-2` and issue the command:

```shell
ubuntu@ubuntu-2:~$ microk8s join 192.168.178.66:25000/ipySurdsIOGAlYyYQzzOOSlpUTEDNGfk
ubuntu@ubuntu-2:~$ 
```

You can verify that the new node has been successfully added to your Kubernetes cluster by logging into the Raspberry Pi running the main cluster node (in my setup, the RPi with the hostname `ubuntu`) and issuing: 

```shell
ubuntu@ubuntu:~$ microk8s.kubectl get nodes
NAME       STATUS     ROLES    AGE   VERSION
ubuntu     Ready      <none>   59d   v1.18.3
ubuntu-2   NotReady   <none>   98s   v1.18.3
ubuntu@ubuntu:~$ 
```

As you can see from the output above, we now have two nodes - `ubuntu` and `ubuntu-2` - in our `microk8s` Kubernetes cluster. However, we have an issue that needs to be fix: The newly added node is in the state `NotReady`. It turns out, this is not due to a timing issue - even after more than an hour the node remains in this state. 

After searching a bit, I stumbled upon the [Konstantinos Tsakalozos comment](https://github.com/ubuntu/microk8s/issues/728) on this issue in the `microk8s` GitHub project.

    K8s was complaining that the cgroup memory was not enabled. Looking at /proc/cgroups was showing memeory disabled. Changes in config.txt are not enough, what actually worked is editing /boot/firmware/nobtcmd.txt, appending cgroup_enable=memory cgroup_memory=1. and rebooting.

Inspecting the `/proc/cgroups` file on my second RPi (the one I want to add to the `microk8s` cluster) confirmed this:

```shell
ubuntu@ubuntu-2:~$ sudo cat /proc/cgroups 
#subsys_name	hierarchy	num_cgroups	enabled
cpuset	8	1	1
cpu	7	1	1
cpuacct	7	1	1
blkio	3	1	1
memory	0	56	0
devices	5	47	1
freezer	6	2	1
net_cls	10	1	1
perf_event	9	1	1
net_prio	10	1	1
pids	2	52	1
rdma	4	1	1
ubuntu@ubuntu-2:~$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 20.04 LTS
Release:	20.04
Codename:	focal
ubuntu@ubuntu-2:~$ uname -a
Linux ubuntu-2 5.4.0-1012-raspi #12-Ubuntu SMP Wed May 27 04:08:35 UTC 2020 aarch64 aarch64 aarch64 GNU/Linux
```

The [`cgroups` man page](https://man7.org/linux/man-pages/man7/cgroups.7.html) explains that Linux control groups, usually referred to as `cgroups`, are a Linux kernel feature which allow processes to be organized into hierarchical groups whose resource usage can then be limited and monitored. In a nutshell, as [Tim Downey puts it in his post](https://downey.io/blog/exploring-cgroups-raspberry-pi/), `cgroups` allow you to do things like limit the amount of CPU usage of a process, limit the amount of memory that a process can consume, control how many additional processes a process can fork, and even “freeze” a process in place. In other words, `cgroups` are a [feature provided by the Linux kernel to manage, restrict, and audit groups of processes](https://wiki.archlinux.org/index.php/cgroups). Compared to other approaches like the `nice` command or `/etc/security/limits.conf`, `cgroups` are more flexible as they can operate on (sub)sets of processes (possibly with different system users). `cgroups` provide a mechanism for aggregating/partitioning sets of tasks, and all their future children, into hierarchical groups with specialized behavior. A container orchestrator like Kubernetes uses `cgroups` to place resource limits on the containers it creates. In case you want to learn more about `cgroups`, check out [this documentation on kernel.org](https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt).

Coming back to our issue, in contrast to the RPi running Ubuntu 20.04, the `cgroups` settings on my main RPi (the main Kubernetes node) look like this:

```shell
ubuntu@ubuntu:~$ sudo cat /proc/cgroups 
#subsys_name	hierarchy	num_cgroups	enabled
cpuset	9	33	1
cpu	4	111	1
cpuacct	4	111	1
blkio	2	111	1
memory	3	125	1
devices	7	111	1
freezer	11	34	1
net_cls	6	33	1
perf_event	8	33	1
net_prio	6	33	1
pids	5	117	1
rdma	10	1	1
ubuntu@ubuntu:~$ uname -a
Linux ubuntu 5.3.0-1017-raspi2 #19~18.04.1-Ubuntu SMP Fri Jan 17 11:14:07 UTC 2020 aarch64 aarch64 aarch64 GNU/Linux
ubuntu@ubuntu:~$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.4 LTS
Release:	18.04
Codename:	bionic
ubuntu@ubuntu:~$ 
```

Thus, as [described in this post](https://askubuntu.com/questions/1189480/raspberry-pi-4-ubuntu-19-10-cannot-enable-cgroup-memory-at-boostrap), you have to edit the `/boot/firmware/cmdline.txt` file to look like this:

```shell
net.ifnames=0 dwc_otg.lpm_enable=0 console=serial0,115200 cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1 console=tty1 root=LABEL=writable rootfstype=ext4 elevator=deadline rootwait fixrtc
```

by adding the `cgroup` options:

```shell
cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1
```

Finally, you need to reboot the RPi for the changes to take effect. Probably the simplest way to do this is by issuing the following command :

```shell
ubuntu@ubuntu-2:~$ sudo reboot
```

After the reboot is complete and you have logged in into the second RPi, you can check the `cgroups` settings and should see the `memory` cgroup enabled:

```shell
ubuntu@ubuntu-2:~$ cat /proc/cgroups 
#subsys_name	hierarchy	num_cgroups	enabled
cpuset	11	6	1
cpu	4	6	1
cpuacct	4	6	1
blkio	3	6	1
memory	9	101	1
devices	5	52	1
freezer	6	7	1
net_cls	7	6	1
perf_event	2	6	1
net_prio	7	6	1
pids	8	57	1
rdma	10	1	1
ubuntu@ubuntu-2:~$ 
```

As a result, if you now `ssh` into the Raspberry Pi running the main `microk8s` cluster node and check the node status in the cluster, you should see something like this:

```shell
ubuntu@ubuntu:~$ microk8s.kubectl get nodes
NAME       STATUS   ROLES    AGE     VERSION
ubuntu     Ready    <none>   59d     v1.18.3
ubuntu-2   Ready    <none>   4h12m   v1.18.3
ubuntu@ubuntu:~$ 
```

Voilà - as you can see, our `microk8s` Kubernetes cluster is now composed of two nodes, i.e., two RPi minicomputers. Both Kubernetes nodes are now in the `Ready` state. You can verify this in the Kubernetes dashboard (in case you haven't setup the dashboard yet, take a look [at this post](http://duplys.github.io/kubernetes/microk8s/dashboard/raspberry-pi-cluster/2020/06/04/experimenting-with-microk8s-dashboard.blog.html)):

![kubernetes-dashboard-two-nodes](/assets/microk8s-kubernetes-dashboard-two-nodes.png)

To recap, the three steps needed to add a RPi running Ubuntu 20.04 to your `microk8s` Kubernetes cluster look like this:

1. connect to the RPi you want to add to your `microk8s` Kubernetes cluster and edit the `/boot/firmware/cmdline.txt` file by adding `cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1` to enable `cgroup memory`. Restart that RPi (e.g., by issuing `sudo reboot`)
2. generate the connection token on your main `microk8s` node using the `microk8s add-node` command
3. add the second RPi to the `microk8s` cluster using the `microk8s join` command with the token obtained in step 2

![thats-all](/assets/thats_all_folks.png)