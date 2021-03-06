---
layout: post
title:  "Deploying Mediawiki on a microk8s Kubernetes Cluster"
date:   2020-07-06 20:48:45 +0100
categories: kubernetes microk8s
---

![kubernetes-dashboard](/assets/sunflowers.jpg)

# Boost Your Memory
In a book I read some time ago, I stumbled upon the idea of artificially augmenting one's memory by systematically storing everything one learns in a single place. The book used the term *exocortex* to refer to this concept of extending the natural brain's memory capabilities by external technical means. Since then, I have used such a mechanism to keep everything I consider important (mostly technical) stuff in one place.

In this post, I'll show you how you can use a MediaWiki instance on your private Raspberry Pi Kubernetes cluster to implement an exocortex. [MediaWiki](https://en.wikipedia.org/wiki/MediaWiki) is an open source wiki software originally authored by Magnus Manske and improved by Lee Danial Crocker. The most prominent website running MediaWiki is Wikipedia. It is written in the PHP programming language and stores the contents into a database.

For ease of administration, we'll use Kubernetes to deploy the Mediawiki application. Kubernetes will ensure that things work reliably. For example, if the applications stops working, Kubernetes will immediately spawn a new instance.

A word on spelling: for easier reading -- and in alignment with conventions used in the official Kubernetes documentation -- I will capitalize the names of the Kubernetes objects. Hence, the words "Deployment" and "Pod" refer to specific Kubernetes objects (more details on that later).

# The Ingredients
Here's a list of ingredients we'll need:
* [A `microk8s` Kubernetes cluster on Raspberry Pi](https://dev.to/duplys/a-la-carte-for-devs-microk8s-on-raspberry-pi-4-9j9)
* The official `mediawiki` Docker image
* The official `mariadb` Docker image
* A `docker-compose.yml` file that we will use as a starting point

# Starting Point
If you look up the [official MediaWiki Docker image on DockerHub](https://hub.docker.com/_/mediawiki), you will also find there a `docker-compose` file recommended to deploy the dockerized MediaWiki. We will use this file as a starting point for writing our Kubernetes manifests so we can deploy MediaWiki using `microk8s.kubectl apply` on the Raspberry Pi Kubernetes cluster. This is what the `docker-compose` file looks like: 

```yml
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

Essentially, it consists of two services: the `mediawiki` application itself and the `database` service for storing the data. The `mediawiki` service is exposed to port 8080 and requires two volumes for regular operation. The `database` service run a MariaDB container and needs several environment variables to be set so that the `mediawiki` application can access the database. In the remainder of this post, we'll recreated this setup using Kubernetes mechanisms.  

# The MediaWiki Application
Let's start by creating a `microk8s` Kubernetes deployment for the MediaWiki container.

## The Minimal MediaWiki Deployment
A [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) is a Kubernetes object &mdash; a persistent entity in the Kubernetes system defining the _desired state_ &mdash; that basically specifies a ReplicaSet and the replicated Pods to be run. The specification of a Kubernetes object, referred to as a _manifest_, must contain the following [required fields](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/): 
* `apiVersion` specifying which version of the Kubernetes API is used to create the object
* `kind` specifying the kind of the object to be created
* `metadata` for uniquely identifying the object (at least a `name` string and a UID)
* `spec` specifying the object's desired state

Therefore, as a minimum, the MediaWiki Deployment manifest would look something like this (feel free to choose your own UIDs and label values):

```yml
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

Note that the label in `spec.selector.matchLabels` must match the label in `spec.template.metadata.labels`. [This is because](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) the `.spec.selector` field defines how the Deployment finds which Pods to manage. Thus, you need to select a label that is defined in the Pod template (`app: mediawiki-app`).

We can create the Deployment by issuing `microk8s.kubectl apply -f mediawiki.yml` on the command line of the Raspberry Pi (assuming you saved the Deployment manifest in the file `mediawiki.yml`). It takes some time when we run it for the first time because the images must be downloaded first. After a while &mdash; it takes approximately 5-10 minutes on my RPi &mdash; you should see something like this:

```shell
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl get all
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mediawiki-app-656f6f8d64-7f4xz   1/1     Running   0          11m
pod/mediawiki-app-656f6f8d64-9x924   1/1     Running   0          11m

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes    ClusterIP   10.152.183.1    <none>        443/TCP        75d

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mediawiki-app   2/2     2            2           11m

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/mediawiki-app-656f6f8d64   2         2         2       11m
ubuntu@ubuntu:~/mediawiki$
```

The Deployment is running, the ReplicaSet was created and the two Pods are running just like we specified in the above manifest.

## Adding Volumes
In the `docker-compose` file, our starting point from above, the `mediawiki` service uses a Docker volume for the `/var/www/html/images` directory within the `mediawiki` container. So let's add a volume to our Kubernetes Deployment. The official documentation for Kubernetes volumes [can be found here](https://kubernetes.io/docs/concepts/storage/volumes/). It turns out, we need to add a `volumeMounts` field to `spec.containers` and pass it a list (that's why the next line starts with a `-`) containing the `mountPath` and the `name` of the volume. We also need to add the a `volume` field to `spec` and list the volume we want to add. The Deployment manifest now looks like this:

```yml
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

To update our MediaWiki Deployment, we issue again the same command `microk8s.kubectl apply -f mediawiki.yml`. If we now take a closer look at one of the Pods, we should see a volume attached to it (the actual output of `microk8s.kubectl describe pod` is very detailed, I have trimmed it here for the ease of reading):

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

Note that `microk8s` reports that this volume is just a temporary directory. This is because this type of volume is not persistent in the sense that it is deleted if the pod ceases to exist.

## Restart
Our `docker-compose` file defines the restart policy `always` for the `mediawiki` service. As described in the [official Kubernetes documentation for the Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/), a Pod specification has a `restartPolicy` field with possible values `Always`, `OnFailure`, and `Never`. The default value is `Always`. So we're done here!

## Links
In `docker-compose` the `link` directive creates a link to containers in another service. From the [official Docker Compose documentation](https://docs.docker.com/compose/compose-file/compose-file-v2/#links):

  Containers for the linked service are reachable at a hostname identical to the alias, or the service name if no alias was specified.

  Links are not required to enable services to communicate - by default, any service can reach any other service at that service's name. (See also, the Links topic in Networking in Compose.)

  Links also express dependency between services in the same way as depends_on, so they determine the order of service startup.

I'm not sure whether I need this in Kubernetes because the [official documentation](https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/) says:

  Kubernetes gives every pod its own cluster-private IP address, so you do not need to explicitly create links between pods or map container ports to host ports. This means that containers within a Pod can all reach each other's ports on localhost, and all pods in a cluster can see each other without NAT.

## Ports
The `mediawiki` service in the `docker-compose` file exposes port 80 of the `mediawiki` container and maps it to the port 8080 on the host. To replicate this in our Kubernetes manifest, we first add the `spec.containers.ports` field and pass it a list of the container ports to be exposed (`- containerPort: 80` in this case). The manifest now looks like this:

```yml
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

We again update our Deployment using the `microk8s.kubectl apply -f mediawiki.yml` command. We can verify that `ports` specification took effect:

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

As you can see, port 80 of the MediaWiki container is now exposed. [What this means](https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/) is that your Pod is now accessible through port 80 from any Kubernetes Node within your cluster. 


## Adding a MediaWiki Service
But what happens if a Node dies? The Pods running on that Node die with it. The Deployment will create new Pods, but they will have different IP addresses. And that's exactly the problem solved by a Kubernetes Service. 

A Kubernetes Service defines a logical set of Pods that provide the same functionality and run somewhere in the Kubernetes cluster. Upon creation, each Service is assigned a unique IP address, the so-called `clusterIP`.  This address will not change while the Service is alive. Communication to the Service will be automatically load-balanced to some Pod that is a member of that Service.

Thus, we need to create a Service to expose the `mediawiki` pods to the outside world (outside of the Kubernetes cluster, that is). As with our MediaWiki Deployment, we store the Service manifest in a new file `mediawiki-service.yml`: 

```yml
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

Note that the Service label must match our `selector` label in the Deployment `spec` (in our case the label `app: mediawiki-app`). By the way: for some odd reason, `microk8s.kubectl` returns an error saying `Service` is an unknown type if I use `apiVersion: apps/v1` as in the Deployment (using just `v1` instead works). 

To start the Service, we issue the `microk8s.kubectl apply -f mediawiki-service.yml` command. Let's now inspect out Kubernetes cluster:

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

From the above output, you can see that the Service was created. However, the Service has the type `ClusterIP` meaning that it cannot be reached from outside of the Kubernetes cluster. To fix this, we need to change the `type` of the `mediawiki-srv` service into `NodePort`. In addition, the port should be 80 (as this is the port exposed by the `mediawiki` Pod):

```yml
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

We `microk8s.kubectl apply` the Service manifest again and check the result:

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

## Verifying the Intermediate Result
We can now check our MediaWiki Service and Deployment using the `curl` command line tool directly on the Raspberry Pi:

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

Now that it works locally, we can try to access the `mediawiki` service from our host system, i.e., outside the Raspberry Pi. If you open your web browser and type `http://<ip address of you RPi>:32681`, you should see this:

![alt text](/assets/mediawiki-initial-screenshot.png)




# The Database Application
Next, we need to create a Deployment and Service for the database (MariaDB in our case). In the `docker-compose.yml` file, the MariaDB Service looks like this:

```yml
version: '3'
services:

  # -- snip --

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

## The MariaDB Deployment
We already saw that we don't need to do anything explicitly for the `always` restart policy since it's the default in Kubernetes. However, we have to use a different Docker image for MariaDB because that Docker container will run on our Raspberry Pi. 

Why do we need a different Docker image? Well, the Raspberry Pi CPU is based on the ARM architecture which is a different from that of your standard PC or laptop (which nowadays mostly happens to be x86_64). A Docker image is essentially a collection of layers (packaged in `*.tar` files) containing, among other things, binaries needed to run your application, e.g., command utilities like `cp` or `ls`, compilers like `gcc`, scripting languages like `python` or `ruby`, and your application itself, say, `nginx` (if you're curious, you can just run `docker image save <image-name> -o <some-name>.tar` and look into that `.tar` archive to see the layers and the binaries in each layer).

If the Docker image was built on an x86_64 architecture, the resulting binaries cannot be executed on ARM architecture. Thus, many of the official Docker images from DockerHub &mdash; an the official MariaDb image happens to be one of those &mdash; will not run on a Raspberry Pi. To deal with this, you can either build your own MariaDB image for RPi or [use e.g., the `rpi-mariadb` image](https://hub.docker.com/r/jsurf/rpi-mariadb/), which is a port of the official [`mariadb` image](https://hub.docker.com/_/mariadb/) for Raspberry Pi.

**A word of caution:** For security reasons, you should always be very careful when using unofficial Docker images from DockerHub! Since Docker itself runs with `root` permissions on your system, every Docker container can essentially also access your system with `root` permissions (unless you have configured your Docker installation to avoid this particular threat). If you want to learn more about this, a very accessible source is the "Docker in Practice" book by Ian Miell and Aidan Hobson Sayers, [Chapter 14 "Docker and Security"](https://livebook.manning.com/book/docker-in-practice-second-edition/chapter-14/92)).

Finally, we will need to define the 4 environment variables for the MariaDB container. In Kubernetes, you [set environment variables](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) using the `spec.containers.env` field. So the Deployment manifest for MariaDB looks like this:

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mediawiki-db
spec:
  selector:
    matchLabels:
      app: mediawiki-db
  replicas: 1
  template:
    metadata:
      labels:
        app: mediawiki-db
    spec:
      containers:
        - name: mediawiki-db-container
          image: jsurf/rpi-mariadb
          env:
            - name: MYSQL_DATABASE
              value: my_wiki
            - name: MYSQL_USER
              value: wikiuser
            - name: MYSQL_PASSWORD
              value: example
            - name: MYSQL_RANDOM_ROOT_PASSWORD
              value: 'yes'
```

Use the `microk8s.kubectl apply -f <mariadb-deployment-manifest.yml>` to create the Deployment. You can also check [the DefaultSettings.php file](https://phabricator.wikimedia.org/source/mediawiki/browse/master/includes/DefaultSettings.php) to see why we need to set these environment variables in the MariaDB container for it to work. 

## Adding MariaDB Service
Like with MediaWiki itself, we need to add a Kubernetes Service for MariaDB so it is exposed on the local host and thus can be accessed by the MediaWiki application. The default port number for MariaDB is 3306 and this is also the port MediaWiki will try to connect to. Hence, the manifest for the MariaDB service looks like this:

```yml
apiVersion: v1
kind: Service
metadata:
  name: mediawiki-db-srv
  labels:
    app: mediawiki-db
spec:
  type: NodePort
  ports:
    - port: 3306
      protocol: TCP
  selector:
    app: mediawiki-db
```

Use the `microk8s.kubectl apply -f <mariadb-service-manifest.yml>` to create the Service. You now should see the following Kubernetes objects running:

```shell
ubuntu@ubuntu:~/mediawiki$ microk8s.kubectl get all
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mediawiki-app-55f45cf568-gmpzv   1/1     Running   0          9h
pod/mediawiki-db-5cb8db589f-r6q8k    1/1     Running   0          9h

NAME                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/kubernetes         ClusterIP   10.152.183.1     <none>        443/TCP          98d
service/mediawiki-db-srv   NodePort    10.152.183.195   <none>        3306:31501/TCP   9h
service/mediawiki-srv      NodePort    10.152.183.17    <none>        80:32681/TCP     9h

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mediawiki-app   1/1     1            1           9h
deployment.apps/mediawiki-db    1/1     1            1           9h

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/mediawiki-app-55f45cf568   1         1         1       9h
replicaset.apps/mediawiki-db-5cb8db589f    1         1         1       9h
ubuntu@ubuntu:~/mediawiki$ 
```

# Setting Up MediaWiki
From your host computer, you can now point your browser to `http://<ip address of you RPi>:32681` and click on the link to start setting up the MediaWiki application. The installation procedure is self-explanatory. The only thing you need to adjust during the setup is to set the IP address of the database to `127.0.0.1` (instead of the default `localhost`).

At the end of the installation, you will be prompted to download the `LocalSettings.php` file. You will need this setting file to run MediaWiki (otherwise, you will always end up in the setup mode). First, you need to `scp` this file to your Raspberry Pi:

```shell
paulduplys@Pauls-MBP Downloads % paulduplys@Pauls-MBP Downloads % scp LocalSettings.php ubuntu@192.168.178.66:/home/ubuntu/mediawiki/
ubuntu@192.168.178.66's password: 
LocalSettings.php                                                                                                                                                                                           100% 4233   858.3KB/s   00:00    
paulduplys@Pauls-MBP Downloads %
```

To mount this file into the `mediawiki` container, we use the [`hostPath` volume](https://kubernetes.io/docs/concepts/storage/volumes/) which mounts a file or directory from the host node's filesystem into your Pod. So, we need to add the following to our Deployment manifest:

```yml

# -- snip --

    spec:
      containers:
        - name: mediawiki-container
          image: mediawiki
          volumeMounts:

            # -- snip --

            - mountPath: /var/www/html/LocalSettings.php
              name: mediawiki-localsettings
          ports:
            - containerPort: 80

      # -- snip --

      volumes:
        - name: mediawiki-volume
        - name: mediawiki-localsettings
          hostPath: 
            path: /home/ubuntu/mediawiki/LocalSettings.php
```

The final MediaWiki Deployment manifest looks like this:

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mediawiki-app
spec:
  selector:
    matchLabels:
      app: mediawiki-app
  replicas: 1
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
            - mountPath: /var/www/html/LocalSettings.php
              name: mediawiki-localsettings
          ports:
            - containerPort: 80
      volumes:
        - name: mediawiki-volume
        - name: mediawiki-localsettings
          hostPath:
            path: /home/ubuntu/mediawiki/LocalSettings.php
            type: File
```

Issue `microk8s.kubectl apply -f mediawiki.yml` one last time and you should have a Kubernetes-managed MediaWiki instance. Enjoy!