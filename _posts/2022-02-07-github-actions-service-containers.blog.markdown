---
layout: post
title:  "Can't Access Service Container in GitHub Actions? Here's How to Fix it"
date:   2022-01-21 21:01:45 +0100
categories: programming github
---


# Error
When running GitHub Actions, you might want to start an application in a [service container](https://docs.github.com/en/actions/using-containerized-services/about-service-containers) and access the application from the GitHub Actions host. 

As an example, you might want to run a web application&mdash;in my case, it was the [OWASP's Juice Shop](https://owasp.org/www-project-juice-shop/)&mdash;in the service container and then access it from the host using `curl`. Unfortunately, that might easily end up with an error like this:

!["GitHub Actions failure"](/assets/github-actions-failure.png)

What's happening here? First, it makes sense to take a look at the workflow logs, especially the Docker commands as the containerized application is apparently not working (or we fail to reach the Docker container). One interesting clue you'd discover is that GitHub Actions creates a Docker network and connects the service container to that network:  

```bash
...

##[command]/usr/bin/docker pull bkimminich/juice-shop
Using default tag: latest
latest: Pulling from bkimminich/juice-shop

...

Status: Downloaded newer image for bkimminich/juice-shop:latest
docker.io/bkimminich/juice-shop:latest
##[command]/usr/bin/docker create --name 58e55591ffe849f8bf9c3dfbe1dbdf13_bkimminichjuiceshop_a12804 --label 9916a7 --network github_network_242bd42709204f349068bf9786120d2d --network-alias juice_shop_app -p 3000:3000  -e GITHUB_ACTIONS=true -e CI=true bkimminich/juice-shop
c7aaf737b377e503bd96f3d458f67d08cae4497a8b89d7826d4961e070f1fa57
##[command]/usr/bin/docker start c7aaf737b377e503bd96f3d458f67d08cae4497a8b89d7826d4961e070f1fa57
c7aaf737b377e503bd96f3d458f67d08cae4497a8b89d7826d4961e070f1fa57

...
```

## Now What Does That `docker network create` Actually Do?
In an attempt to debug the error, I tried reproducing the Docker setup on my local machine. Here's [what my machine looks like](https://www.tecmint.com/commands-to-collect-system-and-hardware-information-in-linux/):
```bash
$ uname -a
Linux terminus 4.13.0-38-generic #43-Ubuntu SMP Wed Mar 14 15:20:44 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
```

After executing Docker commands from the GitHub Actions log the current Docker networks look like this:
```bash
$ docker network ls
NETWORK ID     NAME                                              DRIVER    SCOPE
...
74bb2975d284   github_network_242bd42709204f349068bf9786120d2d   bridge    local
...
```

As we would expect, Docker created a network named `github_network_242...`. Here's what this network looks like in detail:

```bash
$ docker network inspect github_network_242bd42709204f349068bf9786120d2d 
[
    {
        "Name": "github_network_242bd42709204f349068bf9786120d2d",
        "Id": "74bb2975d2848f54446da523ca5d9d66b98ea97016203bcbc1c74f5365dfd5b1",
        "Created": "2022-01-20T20:00:58.215693749+01:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        ...
    }
]
paul@terminus:~/Repositories/juice-shop$ 
```

It turns out the driver for the `github_network_242...` network is of type `bridge`. The [official Docker documenetation](https://docs.docker.com/network/) says that Docker’s networking subsystem is pluggable, using drivers. `bridge` is the default network driver. If you don’t specify a driver, this is the type of network you are creating. 

A [Docker bridge network](https://docs.docker.com/network/bridge/) uses a software bridge which allows containers connected to the same bridge network to communicate and isolates them from containers unconnected to that bridge network. But to be able to access a Docker container from the host, you need the `host` Docker network driver as explained [here](https://docs.docker.com/network/).

While [GitHub Actions documentation](https://docs.github.com/en/actions/using-containerized-services/about-service-containers) says that when running jobs directly on the runner machine, service containers can be accessed using `localhost:<port>` or `127.0.0.1:<port>`, that didn't work in my case (as you can see above).

# The Fix
The fix was to change the workflow file so that `curl` is called not on the GitHub Actions host, but rather in another Docker container by adding `container: ubuntu` below the `runs-on` directive. 

```yaml
name: "WebApplicationDefinition PoC with Docker"
on: [push]
jobs:
  web_app_defn:
    runs-on: ubuntu-latest
    container: ubuntu
    services:
      juice_shop_app:
        image: bkimminich/juice-shop
        ports:
          - 3000:3000
      
    steps:
      - run: apt-get update; apt-get install curl -y
      - run: curl juice_shop_app:3000 > curl_result_docker
      - run: cat curl_result_docker
```

It turns out that in this case, GitHub Actions attach both the `ubuntu` and the `juice_shop_app` containers to the same Docker network:

```bash
##[command]/usr/bin/docker create --name e7bc0fa4f08042b283f7c17b6f6a16d8_ubuntu_e4790c [...] --network github_network_e2d8e92952e5496a9b185d930d41bb1f  [...]
...
##[command]/usr/bin/docker create --name 2b247fe7ed4e430c8e853325460a3032_bkimminichjuiceshop_a2272b [...] --network github_network_e2d8e92952e5496a9b185d930d41bb1f ...
```
Now both containers are attached to the same network. After installing `curl` on the `ubuntu` container, I can use the name of the Juice Shop container (`juice_shop_app`) to access it within the Docker network.