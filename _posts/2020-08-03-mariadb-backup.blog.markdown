---
layout: post
title:  "How to Backup MariaDB Database Running in a Kubernetes Pod"
date:   2020-08-07 22:40:04 +0200
categories: kubernetes docker database
---

![recovering-data](/assets/fishing.jpg)

The easiest way to backup (and restore) a MariaDB database is to use [the `mysqldump` tool](https://mariadb.com/kb/en/mysqldump/). This is especially true when you don't have a huge amount of data in your database. `mysqldump` dumps the data in SQL format which is really handy as it can be imported by most database engines. For more details, see [this MariaDB documentation](https://mariadb.com/kb/en/backup-and-restore-overview/).

But how do you backup a database running in a container? First, get the name of the Kubernetes Pod containing your database:

```console
ubuntu@ubuntu:~$ microk8s.kubectl get all
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mediawiki-app-55f45cf568-gmpzv   1/1     Running   2          5d22h
pod/mediawiki-db-5cb8db589f-r6q8k    1/1     Running   0          5d23h
pod/my-nginx-9b596c8c4-4jp7d         1/1     Running   15         102d
pod/my-nginx-9b596c8c4-fnlm7         1/1     Running   2          12d
pod/my-nginx-9b596c8c4-hmz4r         1/1     Running   2          12d

NAME                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/kubernetes         ClusterIP   10.152.183.1     <none>        443/TCP          104d
service/mediawiki-db-srv   NodePort    10.152.183.195   <none>        3306:31501/TCP   5d23h
service/mediawiki-srv      NodePort    10.152.183.17    <none>        80:32681/TCP     28d
service/my-nginx-np        NodePort    10.152.183.73    <none>        80:30178/TCP     102d

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mediawiki-app   1/1     1            1           11d
deployment.apps/mediawiki-db    1/1     1            1           5d23h
deployment.apps/my-nginx        3/3     3            3           102d

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/mediawiki-app-5494668f87   0         0         0       5d23h
replicaset.apps/mediawiki-app-55f45cf568   1         1         1       5d23h
replicaset.apps/mediawiki-app-75cb9c97d7   0         0         0       11d
replicaset.apps/mediawiki-db-5cb8db589f    1         1         1       5d23h
replicaset.apps/my-nginx-9b596c8c4         3         3         3       102d
ubuntu@ubuntu:~$ 
```

In my setup, it's the Pod `mediawiki-db-5cb8db589f-r6q8k` (I know this because in my [Kubernetes Deployment manifest file](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), I named my MariaDB Deployment `mediawiki-db`). Now that we know the Deployment name, we need to find out its IP address. You can easily do this with the `kubectl describe` command (note that since I'm running Canonical's [microk8s, a lightweight Kubernetes variant](https://microk8s.io/), and I don't have shell aliases, I need to prepend `microk8s.`; if you are running regular Kubernetes, just use the standard `kubectl` command): 

```shell
ubuntu@ubuntu:~$ microk8s.kubectl describe pod mediawiki-db-5cb8db589f-r6q8k
Name:         mediawiki-db-5cb8db589f-r6q8k

# -- snip --

IP:           10.1.49.32
IPs:
  IP:           10.1.49.32
Controlled By:  ReplicaSet/mediawiki-db-5cb8db589f

# -- snip --

Events:          <none>
```

You can double check that the IP address is correct by issuing a simple `ping` command:

```shell
ubuntu@ubuntu:~$ ping 10.1.49.32
PING 10.1.49.32 (10.1.49.32) 56(84) bytes of data.
64 bytes from 10.1.49.32: icmp_seq=1 ttl=63 time=2.04 ms
64 bytes from 10.1.49.32: icmp_seq=2 ttl=63 time=0.615 ms
^C
--- 10.1.49.32 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.615/1.329/2.044/0.715 ms
ubuntu@ubuntu:~$
```

Now that you know the IP address exists and is alive, you can check whether the MariaDB database is actually running. To do this, you can use the `mysql` command to connect to a MariaDB database on that Pod. In my case, `wikiuser` is the user name for the database, `10.1.49.32` is the IP address of the corresponding Kubernetes Pod, and `my_wiki` is the name of the database I have previously created. 

```shell
ubuntu@ubuntu:~$ mysql -u wikiuser -p -h 10.1.49.32 my_wiki
Enter password: 
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 160
Server version: 5.5.5-10.3.22-MariaDB-0+deb10u1 Raspbian 10

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> exit
Bye
ubuntu@ubuntu:~$
```

If all looks well, you can issue the `mysqldump` command as shown below. The command takes the username (`-u` switch), the `-p` switch for password (if you omit the password value, `mysqldump` prompts for one), the IP address (`-h` switch), and the name of the database to be dumped. By default, the `mysqldump` outputs the SQL statements to create and populate the database to the standard output. Hence, to backup into a file, you can simply redirect the output to an arbitrary file or your choice using the `>` shell operator:

```shell
ubuntu@ubuntu:~$ mysqldump -u wikiuser -p -h 10.1.49.32 my_wiki > my_wiki_backup.sql
Enter password:  
ubuntu@ubuntu:~$ head -n 20 my_wiki_backup.sql 
-- MySQL dump 10.13  Distrib 5.7.31, for Linux (aarch64)
--
-- Host: 10.1.49.32    Database: my_wiki
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.22-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actor`
--
ubuntu@ubuntu:~$ 
```
