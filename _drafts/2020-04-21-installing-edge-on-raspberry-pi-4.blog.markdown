---
layout: post
title:  "Installing Edge Stuff on a Raspberry Pi 4!"
date:   2020-04-21 21:03:09 +0100
categories: linux rpi raspberry-pi edge microk8s
---

Approximate time to install: around 2 hours.

Install using the standard instructions, e.g., found here: https://ubuntu.com/download/raspberry-pi/thank-you?version=18.04.4&architecture=arm64+raspi3. After downloading and extracting the image (you need to extract the .xz file, it's an archive) use e.g., win32disk to write the image onto the SD card. 

Next, similar to what is described here https://www.raspberrypi.org/documentation/remote-access/ssh/, simply create a new file `ssh` in the root directory of the SD card, where also file like config.txt, etc. are located. This will enable `ssh` at the first boot of your Pi.

Next, connect your RPi to your router using a network cable, insert the SD card in the Pi's SD card slot and power up the RPi.

Connect to your router - most of them like e.g., the AVM FritzBox have a web admin frontend where you can login; for FritzBox, just fire up your browser and enter `http://fritz.box`. This will give you a login mask. Once you logged in, look up the IP address of the newly connected RPi. Typically, it will have `ubuntu` as device name.

Now, from your host (which needs to be connected to the router, e.g., via WiFi), do

```shell
$ ssh ubuntu@<IP address of your pi>
```

and enter `ubuntu` when asked for password. When logging in for the first time, you will be asked to choose a new password. From then on, you login using the user `ubuntu` and your new password.

To install and use Kubernetes or microk8s, you need `cgroups`. By default, `cgroups` are not enabled on the Ubuntu server image for RPi. According to https://microk8s.io/docs/install-alternatives#arm, you need to edit the boot parameters in `nobtcmd.txt` (in the older Pi versions before Pi 4, this file was called `cmdline.txt`; if you google for how to enable cgroups on a RPi, you might hit a tutorial that uses this outdated name):

```shell
$ sudo vi /boot/firmware/nobtcmd.txt
```
and add the following:

```
cgroup_enable=memory cgroup_memory=1
```

After doing this change, in order for it to take effect, issue

```shell
$ sudo reboot
```

Next, follow the instructions at https://microk8s.io on how to install microk8s using snap. As I'm writing this post, the current channel version is 1.18, so on your RPi, issue:

```shell
$ sudo snap install microk8s --classic --channel=1.18/stable
```

After the installation is complete, you need to add your current user `ubuntu` to the `microk8s` group and make some other changes. See https://microk8s.io/docs for details:

```shell
ubuntu@ubuntu:~$ sudo usermod -a -G microk8s $USER
ubuntu@ubuntu:~$ sudo chown -f -R $USER ~/.kube
ubuntu@ubuntu:~$ su - $USER
Password: 
ubuntu@ubuntu:~$ microk8s status --wait-ready
microk8s is running
addons:
dashboard: disabled
dns: disabled
helm: disabled
helm3: disabled
ingress: disabled
kubeflow: disabled
metallb: disabled
metrics-server: disabled
rbac: disabled
registry: disabled
storage: disabled
ubuntu@ubuntu:~$ microk8s kubectl get nodes
NAME     STATUS   ROLES    AGE   VERSION
ubuntu   Ready    <none>   10m   v1.18.0
ubuntu@ubuntu:~$ microk8s kubectl get services
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.152.183.1   <none>        443/TCP   10m
```

Congrats! You now have a working microk8s Kubernetes installation on your Raspberry Pi 4!

Further references: 
* https://ubuntu.com/tutorials/install-a-local-kubernetes-with-microk8s#2-deploying-microk8s
* https://kubernetes.io/blog/2019/11/26/running-kubernetes-locally-on-linux-with-microk8s/
* https://microk8s.io/docs/

# What can we do next?
* GitLab
* Nginx (also for security experiments)
* A simple code checking service, e.g., using RATS, FlawFinder, Cppcheck or Cobra
* A node.js application
* Apache Spark
* A service for weather forecast, e.g., using OpenWeatherMap (https://de.wikipedia.org/wiki/OpenWeatherMap)
* An application to continuously analyze the IACR ePrint publications 
* https://data.europa.eu/euodp/en/home
* https://www.govdata.de
* http://www.dvwa.co.uk

# Short life sign
```shell
paulduplys@Pauls-MBP duplys.github.io % ping 192.168.178.66
PING 192.168.178.66 (192.168.178.66): 56 data bytes
64 bytes from 192.168.178.66: icmp_seq=0 ttl=64 time=8.263 ms
64 bytes from 192.168.178.66: icmp_seq=1 ttl=64 time=7.691 ms
64 bytes from 192.168.178.66: icmp_seq=2 ttl=64 time=7.977 ms
64 bytes from 192.168.178.66: icmp_seq=3 ttl=64 time=8.822 ms
^C
--- 192.168.178.66 ping statistics ---
4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 7.691/8.188/8.822/0.418 ms
paulduplys@Pauls-MBP duplys.github.io % 
```


# Kubernetes nginx deployment

```shell
ubuntu@ubuntu:~$ microk8s.kubectl create deployment my-nginx --image nginx
deployment.apps/my-nginx created
ubuntu@ubuntu:~$ microk8s.kubectl get all
NAME                           READY   STATUS    RESTARTS   AGE
pod/my-nginx-9b596c8c4-ngd2q   1/1     Running   0          12m

NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.152.183.1   <none>        443/TCP   47h

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-nginx   1/1     1            1           12m

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/my-nginx-9b596c8c4   1         1         1       12m
ubuntu@ubuntu:~$ microk8s.kubectl get services
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.152.183.1   <none>        443/TCP   47h
ubuntu@ubuntu:~$ microk8s.kubectl scale deployment my-nginx --replicas 3
deployment.apps/my-nginx scaled
ubuntu@ubuntu:~$ microk8s.kubectl get all
NAME                           READY   STATUS    RESTARTS   AGE
pod/my-nginx-9b596c8c4-4jp7d   1/1     Running   0          7s
pod/my-nginx-9b596c8c4-7ql2q   1/1     Running   0          7s
pod/my-nginx-9b596c8c4-ngd2q   1/1     Running   0          14m

NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.152.183.1   <none>        443/TCP   47h

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-nginx   3/3     3            3           14m

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/my-nginx-9b596c8c4   3         3         3       14m
ubuntu@ubuntu:~$ microk8s.kubectl expose deployment my-nginx --port 80 --name my-nginx-np --type NodePort
service/my-nginx-np exposed
ubuntu@ubuntu:~$ microk8s.kubectl get services
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes    ClusterIP   10.152.183.1    <none>        443/TCP        47h
my-nginx-np   NodePort    10.152.183.73   <none>        80:30178/TCP   13s
ubuntu@ubuntu:~$ microk8s.kubectl get all
NAME                           READY   STATUS    RESTARTS   AGE
pod/my-nginx-9b596c8c4-4jp7d   1/1     Running   0          3m34s
pod/my-nginx-9b596c8c4-7ql2q   1/1     Running   0          3m34s
pod/my-nginx-9b596c8c4-ngd2q   1/1     Running   0          17m

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes    ClusterIP   10.152.183.1    <none>        443/TCP        47h
service/my-nginx-np   NodePort    10.152.183.73   <none>        80:30178/TCP   20s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-nginx   3/3     3            3           17m

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/my-nginx-9b596c8c4   3         3         3       17m
ubuntu@ubuntu:~$ 
ubuntu@ubuntu:~$ curl 127.0.0.1:30178
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
ubuntu@ubuntu:~$ ubuntu@ubuntu:~$
```

And now let's try to reach the nginx from outside of the RPi:

```shell
paulduplys@Pauls-MBP duplys.github.io % curl 192.168.178.66:30178
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
paulduplys@Pauls-MBP duplys.github.io % 
```



Need to expose a NodePort to access the deployment not just within the 
Let's expose a NodePort so we can access it via the host IP (including localhost on Windows/Linux/macOS)
> kubectl expose deployment/httpenv --port 8888 --name httpenv- np --type NodePort
• Did you know that a NodePort service also creates a ClusterIP?
• These three service types are additive, each one
creates the ones above it: • ClusterIP
• NodePort
• LoadBalancer

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
