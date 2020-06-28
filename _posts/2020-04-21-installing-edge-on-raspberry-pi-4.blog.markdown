---
layout: post
title:  "Installing microk8s and nginx on Raspberry Pi 4"
date:   2020-04-21 21:03:09 +0100
categories: linux rpi raspberry-pi microk8s nginx kubernetes
---

After finally getting my hands on a gorgeous [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) (the version with 4 GB of RAM), I decided to test-drive it by installing Canonical's [`microk8s`](https://microk8s.io), a small, single-package, CNCF certified fully-conformant upstream Kubernetes deployment for offline development, prototyping, and testing. 

It came in handy that I had watched the superb ["Docker Mastery: with Kubernetes + Swarm"](https://www.bretfisher.com/courses) course by Bret Fisher and so could apply the things I learned there. I can definitely recommend this course if you are interested in learning Docker, Swarm, and Kubernetes from the ground up. Bret is a great instructor and, besides the videos and slides, the course contains a lot of good exercises and handy reference material. All in all, it took me about 2 hours to install everything and maybe another 1 hour to play around a bit and set things up.

In this post, I'll show you step by step how you can replicate that and create a `microk8s` Kubernetes deployment on your Raspberry Pi 4. This will give you a nice environment where you can quickly deploy any containerized applications to experiment, prototype, test, and play around at home.

# The Hardware
In addition to the Raspberry Pi 4 microcomputer itself, you'll need 3 extra hardware items.
* A power supply for the Raspberry. I use [Raspberry Pi 15.3W USB-C](https://www.raspberrypi.org/products/type-c-power-supply/), the officially recommended USB-C power supply for Raspberry Pi 4.  
* An microSD card for storing the operating system, Docker + Kubernetes and your applications on your Raspberry. I use a 128GB microSD card from SanDisk.
* A network cable to connect the Raspberry to your router. Any Ethernet cable will do. 

# Installing Ubuntu 18.04 on Raspberry Pi 4
First of all, you need to install an operating system on the Raspberry. I chose Ubuntu Server because of its comprehensive package repositories and long-term support (LTS). Shortly after I was preparing this post, Ubuntu switched from 18.04 to 20.04 LTS release, but the instructions given here should work on 20.04 as well.

To get the Ubuntu image for Raspberry Pi, visit the [official Ubuntu download website](https://ubuntu.com/download/raspberry-pi) and download the 64-bit version of the Ubuntu Pi image. Follow the [installation instructions](https://ubuntu.com/download/raspberry-pi/thank-you?version=20.04&architecture=arm64+raspi).

Once the download is complete you need to extract the Ubuntu Server 20.04 image (the `.xz` file is an archive) and copy it onto your microSD card. The installation instructions contain links to short tutorials on how to do this under Linux, Windows and Macs. If you happen to be on a Windows machine, you can use the `win32disk` tool to write the Ubuntu image onto the microSD card (remember that you first need unpack the `.xz` archive).

Because I'm too lazy to use an extra screen for the installation, I rather chose to `ssh` into the Raspberry Pi once it has booted. To enable this, you can follow the instructions described [here](https://www.raspberrypi.org/documentation/remote-access/ssh/) and simply create a new file called `ssh` in the root directory of your microSD card (it's the same directory where files like config.txt are located). This will enable the `ssh` daemon at the first boot of your Rapsberry so you will be able to immediately `ssh` into it. 

Next, you need connect the Raspberry to your router using a network cable, insert the microSD card into the SD card slot and power up the Raspberry Pi.

Connect to your router - most of them like e.g., the AVM FritzBox have a web admin frontend where you can login; If you happen to have a FritzBox, just fire up your browser and enter `http://fritz.box`. This will give you a login mask. Once you logged in, look up the IP address of the newly connected Raspberry Pi. Typically, it will have `ubuntu` as its device name.

Now, from your host (which obviously needs to be connected to the same router, e.g., via WiFi), do:

{% highlight shell-session %}
$ ssh ubuntu@<IP address of your pi>
{% endhighlight %}

and enter `ubuntu` when asked for password. When logging in for the first time, you will be asked to choose a new password. From then on, you login using the user `ubuntu` and your new password.


# Installing `microk8s`
To install and use `microk8s`, you need `cgroups`. By default, `cgroups` are not enabled on the Ubuntu server image for Raspberry Pi. As described in this [`microk8s` documentation](https://microk8s.io/docs/install-alternatives#arm), you need to edit the boot parameters in `nobtcmd.txt` (attention: in the older Pi versions before Pi 4, this file was called `cmdline.txt`; if you google for how to enable `cgroups` on a Raspberry Pi, you might hit a tutorial that uses this outdated name). Thus, fire up the `vi` editor as `root` using `sudo`:

{% highlight shell-session %}
ubuntu@ubuntu:~$ sudo vi /boot/firmware/nobtcmd.txt
{% endhighlight %}

and add the following line:

{% highlight shell-session %}
cgroup_enable=memory cgroup_memory=1
{% endhighlight %}

After the change, you need to reboot the Raspberry Pi for it to take effect. To do this, issue:

{% highlight shell-session %}
ubuntu@ubuntu:~$ sudo reboot
{% endhighlight %}

Next, follow the [instructions on the `microk8s` website](https://microk8s.io) on how to install `microk8s` using snap. As I'm writing this post, the current channel version is 1.18. So on your Raspberry Pi, issue:

{% highlight shell-session %}
ubuntu@ubuntu:~$ sudo snap install microk8s --classic --channel=1.18/stable
{% endhighlight %}

After the installation is complete, you need to add your current user `ubuntu` to the `microk8s` group and make some other changes. See [the `microk8s` documentation](https://microk8s.io/docs) for details. You need to do the following:

{% highlight shell-session %}
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
{% endhighlight %}

Congrats! You now have a working `microk8s` installation on your Raspberry Pi 4!

# Deploying nginx with microk8s
To play around with your new shiny `microk8s` installation, you can create a deployment for `nginx`, a popular HTTP and reverse proxy server. If you want to learn more about `nginx`, visit [their website](https://nginx.org/en/). Start by creating a Kubernetes deployment using the `nginx` Docker image and verify that the deployment has been indeed created:

{% highlight shell-session %}
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
{% endhighlight %}

Next, you can optionally increase the number of your replicas (and again verify that it worked):

{% highlight shell-session %}
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
{% endhighlight %}

Finally, you need to expose a so-called NodePort so that the `nginx` deployment can be accessed from anywhere within your home network using the IP address of your Raspberry Pi. Issue the following commands:

{% highlight shell-session %}
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
{% endhighlight %}

Let's verify that `nginx` is working and can be accessed using the host IP address. We can first do this directly on the Raspberry Pi (in the `ssh` session) using the local IP address:

{% highlight shell-session %}
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
{% endhighlight %}

It works! Finally, let's try to reach `nginx` from outside of the Raspberry Pi. To do this, exit your `ssh` session and from your host machine, do:

{% highlight shell-session %}
% curl <IP address of your Raspberry Pi>:30178
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
{% endhighlight %}

Congratulations!! You now have a working `microk8s` deployment and the `nginx` application up and running on Kubernetes.



# Further References
You can also check out these references:
* https://ubuntu.com/tutorials/install-a-local-kubernetes-with-microk8s#2-deploying-microk8s
* https://kubernetes.io/blog/2019/11/26/running-kubernetes-locally-on-linux-with-microk8s/
* https://microk8s.io/docs/
