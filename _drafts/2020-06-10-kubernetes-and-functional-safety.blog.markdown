---
layout: post
title:  "Kubernetes and Functional Safety"
date:   2020-06-10 08:03:53 +0100
categories: kubernetes safety functional-safety
---
To achieve high availability, you can have multiple Pods, i.e., multiple replicas of the same service. However, scheduling multiple replicas of the same application onto the same machine is worse for reliability, since the machine is a single failure domain. Consequently, Kubernetes scheduler tries to ensure that Pods from the same application are distributed onto different machiens for reliability in the presense of failures. 

# Health checks
Kubernetes has a built-in _process health check_ to make sure that your containers are always alive. This health check simply ensures that the main process of your application is always running. If it isn't, Kubernetes restarts it.

However, in most cases such a health check is insufficient, e.g., if your process enters a deadlock and is unable to serve requests, the health check would still believe everything is working fine.

To address this, Kubernetes introduced health checks for application _liveness_. Liveness health checks run application-specific logic (e.g., loading a web page) to verify that the application is not just still running, but is functioning properly. Since these liveness health checks are application-specific, you have to define them in the Pod manifest.

Su liveness probes are defined per container, which means each container inside a Pod is health-checked separately. In the following example, the liveness probe runs an HTTP request against the `/healthy` path on the container:

```yml
apiVersion: v1
kind: Pod
metadata:
  name: kuard
spec:
  containers:
    - image: gcr.io/kuard-demo/kuard-amd64:blue
      name: kuard
      livenessProbe:
        httpGet:
          path: /healthy
          port: 8080
        initialDelaySeconds: 5
        timeoutSeconds: 1
        periodSeconds: 10
        failureThreshold: 3
      ports:
        - containerPost: 8080
          name: http
          protocol: TCP
```

