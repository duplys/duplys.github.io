---
layout: post
title:  "Installing StarlingX 3.0 on Raspberry Pi"
date:   2020-04-05 11:45:59 +0200
categories: edge robustness cybersafety
---
First, we need to create a bootable USB with the StarlingX ISO image. The instructions for this step can be [found here](https://docs.starlingx.io/deploy_install_guides/bootable_usb.html).
I downloaded this iso image: http://mirror.starlingx.cengn.ca/mirror/starlingx/release/3.0.0/centos/outputs/iso/bootimage.iso.

I run a laptop with native Linux operating system:

```shell
paul@terminus:~/Repositories/duplys.github.io/_drafts$ cat /etc/os-release 
NAME="Ubuntu"
VERSION="16.04.6 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.6 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial
```

On my Linux laptop, when I issue `lsblk` without the USB stick inserted, I see this:

```shell
paul@terminus:~/Repositories/duplys.github.io/_drafts$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop1    7:1    0    55M  1 loop /snap/core18/1705
loop11   7:11   0  93,8M  1 loop /snap/core/8935
loop8    7:8    0  44,9M  1 loop /snap/gtk-common-themes/1440
loop6    7:6    0  54,7M  1 loop /snap/core18/1668
loop4    7:4    0  48,3M  1 loop /snap/gtk-common-themes/1474
loop2    7:2    0   192M  1 loop /snap/microk8s/1320
loop0    7:0    0  91,4M  1 loop /snap/core/8689
loop9    7:9    0   100M  1 loop /snap/keepassxc/664
loop10   7:10   0 297,5M  1 loop /snap/stellarium-plars/55
sda      8:0    0 465,8G  0 disk 
├─sda4   8:4    0 407,3G  0 part /home
├─sda2   8:2    0     8G  0 part [SWAP]
├─sda3   8:3    0    50G  0 part /
└─sda1   8:1    0   512M  0 part /boot/efi
loop5    7:5    0   192M  1 loop /snap/microk8s/1293
loop3    7:3    0   100M  1 loop /snap/keepassxc/687
paul@terminus:~/Repositories/duplys.github.io/_drafts$ 
```

**With** the USB stick inserted, I see this:

```shell
paul@terminus:~/Repositories/duplys.github.io/_drafts$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop1    7:1    0    55M  1 loop /snap/core18/1705
loop11   7:11   0  93,8M  1 loop /snap/core/8935
sdb      8:16   1  14,7G  0 disk 
└─sdb1   8:17   1  14,7G  0 part 
loop8    7:8    0  44,9M  1 loop /snap/gtk-common-themes/1440
loop6    7:6    0  54,7M  1 loop /snap/core18/1668
loop4    7:4    0  48,3M  1 loop /snap/gtk-common-themes/1474
loop2    7:2    0   192M  1 loop /snap/microk8s/1320
loop0    7:0    0  91,4M  1 loop /snap/core/8689
loop9    7:9    0   100M  1 loop /snap/keepassxc/664
loop10   7:10   0 297,5M  1 loop /snap/stellarium-plars/55
sda      8:0    0 465,8G  0 disk 
├─sda4   8:4    0 407,3G  0 part /home
├─sda2   8:2    0     8G  0 part [SWAP]
├─sda3   8:3    0    50G  0 part /
└─sda1   8:1    0   512M  0 part /boot/efi
loop5    7:5    0   192M  1 loop /snap/microk8s/1293
loop3    7:3    0   100M  1 loop /snap/keepassxc/687
paul@terminus:~/Repositories/duplys.github.io/_drafts$ 
```

Thus, the device corresponding to the USB stick on my host machine is `sdb1`. Now we need to unmount the USB drive before we can burn an image onto it:

```shell
paul@terminus:~/Repositories/duplys.github.io/_drafts$ sudo umount /dev/sdb1
[sudo] password for paul: 
paul@terminus:~/Repositories/duplys.github.io/_drafts$
```

We can verify that the partition was unmounted successfully by issuing `lsblk` again:

```shell
$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop1    7:1    0    55M  1 loop /snap/core18/1705
loop11   7:11   0  93,8M  1 loop /snap/core/8935
sdb      8:16   1  14,7G  0 disk 
└─sdb1   8:17   1  14,7G  0 part 
loop8    7:8    0  44,9M  1 loop /snap/gtk-common-themes/1440
loop6    7:6    0  54,7M  1 loop /snap/core18/1668
loop4    7:4    0  48,3M  1 loop /snap/gtk-common-themes/1474
loop2    7:2    0   192M  1 loop /snap/microk8s/1320
loop0    7:0    0  91,4M  1 loop /snap/core/8689
loop9    7:9    0   100M  1 loop /snap/keepassxc/664
loop10   7:10   0 297,5M  1 loop /snap/stellarium-plars/55
sda      8:0    0 465,8G  0 disk 
├─sda4   8:4    0 407,3G  0 part /home
├─sda2   8:2    0     8G  0 part [SWAP]
├─sda3   8:3    0    50G  0 part /
└─sda1   8:1    0   512M  0 part /boot/efi
loop5    7:5    0   192M  1 loop /snap/microk8s/1293
loop3    7:3    0   100M  1 loop /snap/keepassxc/687
$ 
```

Note that now there is no partitiion listed under `sdb1`. So now we can burn the StarlingX image onto the USB drive:

```shell
$ sudo dd if=/home/paul/Downloads/bootimage.iso of=/dev/sdb1 bs=1M status=progress
1942+0 records in
1942+0 records out
2036334592 bytes (2,0 GB, 1,9 GiB) copied, 546,757 s, 3,7 MB/s
$ 
```

Next, need to find out how to boot a RPi3 from a USB. 

Once we boot the RPi3 from the USB drive, we need to install the StarlingX software as described here: https://docs.starlingx.io/deploy_install_guides/r3_release/bare_metal/aio_simplex_install_kubernetes.html#id2.

Follow the description given at https://docs.starlingx.io/deploy_install_guides/r3_release/bare_metal/aio_simplex_install_kubernetes.html#id3 to bootstrap the StarlingX system and perform the initial setup.

Next, configure controller-0 as described here: https://docs.starlingx.io/deploy_install_guides/r3_release/bare_metal/aio_simplex_install_kubernetes.html#id4. This is a quite lengthy session, so take your time.

Finally, unlock the controller-0 as described here: https://docs.starlingx.io/deploy_install_guides/r3_release/bare_metal/aio_simplex_install_kubernetes.html#id5.

See the section at https://docs.starlingx.io/deploy_install_guides/r3_release/bare_metal/aio_simplex_install_kubernetes.html#id6 for the next steps.

# Install something interesting

join nodes: https://sirchia.cloud/posts/kubernetes-on-64-bit-os-raspberry-pi-4/

add CoreDNS for services to work:

```shell
ubuntu@ubuntu:~$ microk8s.enable dns
Enabling DNS
Applying manifest
serviceaccount/coredns created
configmap/coredns created
deployment.apps/coredns created
service/kube-dns created
clusterrole.rbac.authorization.k8s.io/coredns created
clusterrolebinding.rbac.authorization.k8s.io/coredns created
Restarting kubelet
DNS is enabled
ubuntu@ubuntu:~$ 
```



Two ways to deploy Pods (containers): Via commands, or via YAML
• Let's run a pod of the nginx web server!
> kubectl create deployment my-nginx --image nginx
• Let's list the pod
> kubectl get pods
• Let's see all objects
> kubectl get all

Let's scale it up with another pod
> kubectl scale deploy/my-apache --replicas 2
> kubectl scale deployment my-apache --replicas 2
• those are the same command
• deploy = deployment = deployments

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
