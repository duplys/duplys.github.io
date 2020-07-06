---
layout: post
title:  "Mediawiki with microk8s"
date:   2020-07-06 20:48:45 +0100
categories: kubernetes
---

# Introduction

* how can I create a volume in a deployment?
* how can I create a deployment of the mediawiki container?
* how can I create a deployment of the mariadb container?
* is everything going into a single deployment or into two deployments?

# Starting Point

OK, here is a Mediawiki `docker-compose.yml`:

```docker
# MediaWiki with MariaDB
#
# Access via "http://localhost:8080"
#   (or "http://$(docker-machine ip):8080" if using docker-machine)
version: '3'
services:
  mediawiki:
    image: mediawiki
    restart: always
    ports:
      - 8080:80
    links:
      - database
    volumes:
      - /var/www/html/images
      # After initial setup, download LocalSettings.php to the same directory as
      # this yaml and uncomment the following line and use compose to restart
      # the mediawiki service
      # - ./LocalSettings.php:/var/www/html/LocalSettings.php
  database:
    image: mariadb
    restart: always
    environment:
      # @see https://phabricator.wikimedia.org/source/mediawiki/browse/master/includes/DefaultSettings.php
      MYSQL_DATABASE: my_wiki
      MYSQL_USER: wikiuser
      MYSQL_PASSWORD: example
      MYSQL_RANDOM_ROOT_PASSWORD: 'yes'
```

# The Mediawiki container

## Deployment
```docker
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mediawiki-app
spec:
  selector:
    matchLabels:
      app: mediawiki-app
  replicas: 2
  template:
    metadata:
      labels:
        app: mediawiki-app
    spec:
      containers:
        - name: mediawiki-container
          image: mediawiki
```

## Volumes
OK, so first let's see how to deal with volumes in Kubernetes. The official documentation for Kubernetes volumes [can be found here](https://kubernetes.io/docs/concepts/storage/volumes/). 

I can create a deployment by issuing `microk8s.kubectl apply -f mediawiki.yml` with this deployment manifest:

```docker
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mediawiki-app
spec:
  selector:
    matchLabels:
      app: mediawiki-app
  replicas: 2
  template:
    metadata:
      labels:
        app: mediawiki-app
    spec:
      containers:
        - name: mediawiki-container
          image: mediawiki
          volumeMounts:
            - mountPath: /var/www/html/images
              name: mediawiki-volume
      volumes:
        - name: mediawiki-volume
```

It takes some time if I run it for the first time since the images must be downloaded first. After a while - approximately 5-10 minutes on my RPi - I see this:

```shell
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl get all
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mediawiki-app-656f6f8d64-7f4xz   1/1     Running   0          11m
pod/mediawiki-app-656f6f8d64-9x924   1/1     Running   0          11m
pod/my-nginx-9b596c8c4-4jp7d         1/1     Running   7          73d
pod/my-nginx-9b596c8c4-fsm2d         1/1     Running   0          13d
pod/my-nginx-9b596c8c4-m5vtt         1/1     Running   0          9d

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes    ClusterIP   10.152.183.1    <none>        443/TCP        75d
service/my-nginx-np   NodePort    10.152.183.73   <none>        80:30178/TCP   73d

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mediawiki-app   2/2     2            2           11m
deployment.apps/my-nginx        3/3     3            3           73d

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/mediawiki-app-656f6f8d64   2         2         2       11m
replicaset.apps/my-nginx-9b596c8c4         3         3         3       73d
ubuntu@ubuntu:~/mediawiki$ 
```

It seems like both pods are running, which is good. If I look closer into one of the pods, I see this:

```shell
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl describe pod mediawiki-app-656f6f8d64-7f4xz
Name:         mediawiki-app-656f6f8d64-7f4xz

# -- snip --

Containers:
  mediawiki-container:
    Container ID:   containerd://8525869985915306078e1c2b836682ddf145510a4fe04b7155618a749ed87e2d
    Image:          mediawiki

    # -- snip --

    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-krfdn (ro)
      /var/www/html/images from mediawiki-volume (rw)

# -- snip --

Volumes:
  mediawiki-volume:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     
    SizeLimit:  <unset>

# -- snip --

ubuntu@ubuntu:~/mediawiki$ 
```

Note that `microk8s` reports that this volume is just a temporary directory. That is, this type of volume is not persistent in the sense that it is deleted if the pod ceases to exist.


## Restart
The official Kubernetes documentation for the Pod lifecycle [can be found here](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/). It turns out that a `PodSpec` has a `restartPolicy` field with possible values `Always`, `OnFailure`, and `Never`. The default value is `Always`. Thus, there's nothing for us to do. 

## Ports
```docker
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mediawiki-app
spec:
  selector:
    matchLabels:
      app: mediawiki-app
  replicas: 2
  template:
    metadata:
      labels:
        app: mediawiki-app
    spec:
      containers:
        - name: mediawiki-container
          image: mediawiki
          volumeMounts:
            - mountPath: /var/www/html/images
              name: mediawiki-volume
          ports:
            - containerPort: 80
      volumes:
        - name: mediawiki-volume
```

Applying the above manifest (added `ports`) using `microk8s.kubectl apply -f mediawiki.yml` gives this:

```shell
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl describe deployment mediawiki-app
Name:                   mediawiki-app

# -- snip --

Pod Template:
  Labels:  app=mediawiki-app
  Containers:
   mediawiki-container:
    Image:        mediawiki
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>

# -- snip --

ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl describe pod mediawiki-app-5494668f87-5xldp
Name:         mediawiki-app-5494668f87-5xldp

# -- snip --

Containers:
  mediawiki-container:
    Container ID:   containerd://6ba69454dc74ebc359466edc233197e2cf11f3ae8365d4fcf5ea60b0b62ec3b7
    Image:          mediawiki
    Image ID:       docker.io/library/mediawiki@sha256:e3be6a44c1d82e454657a013c5df29f7a9a0bfc112325d6d9df1ab1e21087b51
    Port:           80/TCP
    Host Port:      0/TCP

# -- snip --

ubuntu@ubuntu:~/mediawiki$ 
```

OK, so this shows that the port 80 of the container is now exposed. What this means is that now your Pod is accessible through port 80 from any node within your cluster [need to check this!]. From [Kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/):

  So we have pods running nginx in a flat, cluster wide, address space. In theory, you could talk to these pods directly, but what happens when a node dies? The pods die with it, and the Deployment will create new ones, with different IPs. This is the problem a Service solves.

  A Kubernetes Service is an abstraction which defines a logical set of Pods running somewhere in your cluster, that all provide the same functionality. When created, each Service is assigned a unique IP address (also called clusterIP). This address is tied to the lifespan of the Service, and will not change while the Service is alive. Pods can be configured to talk to the Service, and know that communication to the Service will be automatically load-balanced out to some pod that is a member of the Service.

Thus, we need to create a service to expose the mediawiki pods to the outside. Note that the service label must match our `selector` label in the Deployment `spec`, namely `app: mediawiki-app` in our case.

```docker
apiVersion: v1
kind: Service
metadata:
  name: mediawiki-srv
  labels:
    app: mediawiki-app
spec:
  ports:
    - port: 8883
      protocol: TCP
  selector:
    app: mediawiki-app

```

By the way: for some odd reason, `microk8s.kubectl` returns an error saying `Service` is an unknown type if I use `apiVersion: apps/v1` as in the deployment (using just `v1` instead works). Anyway, let's look at what the Kubernetes cluster looks like now:

```shell
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl get all
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mediawiki-app-5494668f87-5xldp   1/1     Running   0          19m
pod/mediawiki-app-5494668f87-p7p4s   1/1     Running   0          19m

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes      ClusterIP   10.152.183.1    <none>        443/TCP        75d
service/mediawiki-srv   ClusterIP   10.152.183.17   <none>        8883/TCP       3m51s

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mediawiki-app   2/2     2            2           49m

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/mediawiki-app-5494668f87   2         2         2       19m
replicaset.apps/mediawiki-app-656f6f8d64   0         0         0       49m
ubuntu@ubuntu:~/mediawiki$ 
```

We see that the service was created, but it has the type `ClusterIP` which means that it cannot be reached from outside of the Raspberry Pi. To change this, we need to change the type of the `mediawiki-srv` service into `NodePort`. In addition, the port should be 80 (as this is the port exposed by the mediawiki Pod):

```docker
apiVersion: v1
kind: Service
metadata:
  name: mediawiki-srv
  labels:
    app: mediawiki-app
spec:
  type: NodePort
  ports:
    - port: 80
      protocol: TCP
  selector:
    app: mediawiki-app
```

and run `microk8s.kubectl apply -f mediawiki-service.yml` again:

```shell
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl apply -f mediawiki-service.yml 
service/mediawiki-srv configured
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl get all
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mediawiki-app-5494668f87-5xldp   1/1     Running   0          30m
pod/mediawiki-app-5494668f87-p7p4s   1/1     Running   0          30m

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes      ClusterIP   10.152.183.1    <none>        443/TCP        76d
service/mediawiki-srv   NodePort    10.152.183.17   <none>        80:32681/TCP   14m

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mediawiki-app   2/2     2            2           59m

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/mediawiki-app-5494668f87   2         2         2       30m
replicaset.apps/mediawiki-app-656f6f8d64   0         0         0       59m
ubuntu@ubuntu:~/mediawiki$ 
```

OK, so let's try to query our newly created service using `curl` command line tool directly on the Raspberry Pi:

```shell
ubuntu@ubuntu:~/mediawiki$ curl http://127.0.0.1:32681
<!DOCTYPE html>
<html lang="en" dir="ltr">
	<head>
		<meta charset="UTF-8" />
		<title>MediaWiki 1.34.2</title>
		<style media="screen">
			body {
				color: #000;
				background-color: #fff;
				font-family: sans-serif;
				text-align: center;
			}

			h1 {
				font-size: 150%;
			}
		</style>
	</head>
	<body>
		<img src="/resources/assets/mediawiki.png" alt="The MediaWiki logo" />

		<h1>MediaWiki 1.34.2</h1>
		<div class="error">
		
		
			<p>LocalSettings.php not found.</p>
			
			
				<p>Please <a href="/mw-config/index.php">set up the wiki</a> first.</p>
			
		
		</div>
	</body>
</html>
ubuntu@ubuntu:~/mediawiki$ 
```

Nice - it works! OK, now let's try to access the mediawiki service from the host, i.e., outside the Raspberry Pi:

![alt text](/assets/mediawiki-initial-screenshot.png)

## Links
In `docker-compose` the `link` directive creates a link to containers in another service. From the [official Docker Compose documentation](https://docs.docker.com/compose/compose-file/compose-file-v2/#links):

  Containers for the linked service are reachable at a hostname identical to the alias, or the service name if no alias was specified.

  Links are not required to enable services to communicate - by default, any service can reach any other service at that service’s name. (See also, the Links topic in Networking in Compose.)

  Links also express dependency between services in the same way as depends_on, so they determine the order of service startup.

I'm not sure whether I need this in Kubernetes because the [official documentation](https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/) says:

  Kubernetes gives every pod its own cluster-private IP address, so you do not need to explicitly create links between pods or map container ports to host ports. This means that containers within a Pod can all reach each other's ports on localhost, and all pods in a cluster can see each other without NAT.

