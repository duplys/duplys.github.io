---
layout: post
title:  "Playing with microk8s"
date:   2020-06-04 17:42:51 +0100
categories: kubernetes microk8s
---

# Installation
If you happen to have an old version of `microk8s` that is not working properly, remove it by issuing:

```shell
$ sudo snap remove microk8s
```

and then install the latest version using `snap`. At the time of my writing, the latest version is `1.18/stable`:

```shell
$ sudo snap install microk8s --classic --channel=1.18/stable
```

Once install, we can run the `kubectl` command to check the version of the microk8s cluster you are running. On my machine, this yields:

```shell
$ microk8s.kubectl version
Client Version: version.Info{Major:"1", Minor:"18", GitVersion:"v1.18.3", GitCommit:"2e7996e3e2712684bc73f0dec0200d64eec7fe40", GitTreeState:"clean", BuildDate:"2020-05-20T12:52:00Z", GoVersion:"go1.13.9", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"18", GitVersion:"v1.18.3", GitCommit:"2e7996e3e2712684bc73f0dec0200d64eec7fe40", GitTreeState:"clean", BuildDate:"2020-05-20T12:43:34Z", GoVersion:"go1.13.9", Compiler:"gc", Platform:"linux/amd64"}
$ 
```

To verify the health status of the cluster, we can also run:

```shell
$ microk8s.kubectl get componentstatuses
NAME                 STATUS    MESSAGE             ERROR
scheduler            Healthy   ok                  
controller-manager   Healthy   ok                  
etcd-0               Healthy   {"health":"true"}
$
```

To list all the nodes in the cluster, do:

```shell
$ microk8s.kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
terminus   Ready    <none>   81m   v1.18.3
$
```

In my case, `microk8s` is installed locally on my Linux machine `terminus`, so I see one node in my `microk8s` cluster. Let's get more information about this node:

```shell
$ microk8s.kubectl describe nodes terminus
Name:               terminus
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=terminus
                    kubernetes.io/os=linux
                    microk8s.io/cluster=true
Annotations:        node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Thu, 04 Jun 2020 18:23:25 +0200
Taints:             <none>
Unschedulable:      false
Lease:
  HolderIdentity:  terminus
  AcquireTime:     <unset>
  RenewTime:       Thu, 04 Jun 2020 20:00:59 +0200
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  MemoryPressure   False   Thu, 04 Jun 2020 19:59:06 +0200   Thu, 04 Jun 2020 18:23:25 +0200   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure     False   Thu, 04 Jun 2020 19:59:06 +0200   Thu, 04 Jun 2020 18:23:25 +0200   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure      False   Thu, 04 Jun 2020 19:59:06 +0200   Thu, 04 Jun 2020 18:23:25 +0200   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready            True    Thu, 04 Jun 2020 19:59:06 +0200   Thu, 04 Jun 2020 18:23:35 +0200   KubeletReady                 kubelet is posting ready status. AppArmor enabled
Addresses:
  InternalIP:  192.168.2.127
  Hostname:    terminus
Capacity:
  cpu:                4
  ephemeral-storage:  51475068Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             16346268Ki
  pods:               110
Allocatable:
  cpu:                4
  ephemeral-storage:  50426492Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             16243868Ki
  pods:               110
System Info:
  Machine ID:                 b9345171accd4bbdb68fb20877168a24
  System UUID:                465BFA80-9AA3-0000-0000-000000000000
  Boot ID:                    047e23bc-ce8e-4b53-afc7-475d3e68b878
  Kernel Version:             4.13.0-38-generic
  OS Image:                   Ubuntu 16.04.6 LTS
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  containerd://1.2.5
  Kubelet Version:            v1.18.3
  Kube-Proxy Version:         v1.18.3
Non-terminated Pods:          (0 in total)
  Namespace                   Name    CPU Requests  CPU Limits  Memory Requests  Memory Limits  AGE
  ---------                   ----    ------------  ----------  ---------------  -------------  ---
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests  Limits
  --------           --------  ------
  cpu                0 (0%)    0 (0%)
  memory             0 (0%)    0 (0%)
  ephemeral-storage  0 (0%)    0 (0%)
  hugepages-1Gi      0 (0%)    0 (0%)
  hugepages-2Mi      0 (0%)    0 (0%)
Events:              <none>
$
```

An alternative to get complete information about a Kubernetes object is to use the `-o yaml` flag:

```shell
$ microk8s.kubectl get nodes -o yaml
apiVersion: v1
items:
- apiVersion: v1
  kind: Node
  metadata:
    annotations:
      node.alpha.kubernetes.io/ttl: "0"
      volumes.kubernetes.io/controller-managed-attach-detach: "true"
    creationTimestamp: "2020-06-04T16:23:25Z"
    labels:
      beta.kubernetes.io/arch: amd64
      beta.kubernetes.io/os: linux
      kubernetes.io/arch: amd64
      kubernetes.io/hostname: terminus
      kubernetes.io/os: linux
      microk8s.io/cluster: "true"
    managedFields:
    - apiVersion: v1
      fieldsType: FieldsV1
      fieldsV1:
        f:metadata:
          f:annotations:
            f:node.alpha.kubernetes.io/ttl: {}
      manager: kube-controller-manager
      operation: Update
      time: "2020-06-04T16:23:28Z"
    - apiVersion: v1
      fieldsType: FieldsV1
      fieldsV1:
        f:metadata:
          f:annotations:
            .: {}
            f:volumes.kubernetes.io/controller-managed-attach-detach: {}
          f:labels:
            .: {}
            f:beta.kubernetes.io/arch: {}
            f:beta.kubernetes.io/os: {}
            f:kubernetes.io/arch: {}
            f:kubernetes.io/hostname: {}
            f:kubernetes.io/os: {}
            f:microk8s.io/cluster: {}
        f:status:
          f:addresses:
            .: {}
            k:{"type":"Hostname"}:
              .: {}
              f:address: {}
              f:type: {}
            k:{"type":"InternalIP"}:
              .: {}
              f:address: {}
              f:type: {}
          f:allocatable:
            .: {}
            f:cpu: {}
            f:ephemeral-storage: {}
            f:hugepages-1Gi: {}
            f:hugepages-2Mi: {}
            f:memory: {}
            f:pods: {}
          f:capacity:
            .: {}
            f:cpu: {}
            f:ephemeral-storage: {}
            f:hugepages-1Gi: {}
            f:hugepages-2Mi: {}
            f:memory: {}
            f:pods: {}
          f:conditions:
            .: {}
            k:{"type":"DiskPressure"}:
              .: {}
              f:lastHeartbeatTime: {}
              f:lastTransitionTime: {}
              f:message: {}
              f:reason: {}
              f:status: {}
              f:type: {}
            k:{"type":"MemoryPressure"}:
              .: {}
              f:lastHeartbeatTime: {}
              f:lastTransitionTime: {}
              f:message: {}
              f:reason: {}
              f:status: {}
              f:type: {}
            k:{"type":"PIDPressure"}:
              .: {}
              f:lastHeartbeatTime: {}
              f:lastTransitionTime: {}
              f:message: {}
              f:reason: {}
              f:status: {}
              f:type: {}
            k:{"type":"Ready"}:
              .: {}
              f:lastHeartbeatTime: {}
              f:lastTransitionTime: {}
              f:message: {}
              f:reason: {}
              f:status: {}
              f:type: {}
          f:daemonEndpoints:
            f:kubeletEndpoint:
              f:Port: {}
          f:nodeInfo:
            f:architecture: {}
            f:bootID: {}
            f:containerRuntimeVersion: {}
            f:kernelVersion: {}
            f:kubeProxyVersion: {}
            f:kubeletVersion: {}
            f:machineID: {}
            f:operatingSystem: {}
            f:osImage: {}
            f:systemUUID: {}
      manager: kubelet
      operation: Update
      time: "2020-06-04T17:59:06Z"
    name: terminus
    resourceVersion: "12715"
    selfLink: /api/v1/nodes/terminus
    uid: 476119e1-c4a0-412a-b2ac-bb53e98dff25
  spec: {}
  status:
    addresses:
    - address: 192.168.2.127
      type: InternalIP
    - address: terminus
      type: Hostname
    allocatable:
      cpu: "4"
      ephemeral-storage: 50426492Ki
      hugepages-1Gi: "0"
      hugepages-2Mi: "0"
      memory: 16243868Ki
      pods: "110"
    capacity:
      cpu: "4"
      ephemeral-storage: 51475068Ki
      hugepages-1Gi: "0"
      hugepages-2Mi: "0"
      memory: 16346268Ki
      pods: "110"
    conditions:
    - lastHeartbeatTime: "2020-06-04T17:59:06Z"
      lastTransitionTime: "2020-06-04T16:23:25Z"
      message: kubelet has sufficient memory available
      reason: KubeletHasSufficientMemory
      status: "False"
      type: MemoryPressure
    - lastHeartbeatTime: "2020-06-04T17:59:06Z"
      lastTransitionTime: "2020-06-04T16:23:25Z"
      message: kubelet has no disk pressure
      reason: KubeletHasNoDiskPressure
      status: "False"
      type: DiskPressure
    - lastHeartbeatTime: "2020-06-04T17:59:06Z"
      lastTransitionTime: "2020-06-04T16:23:25Z"
      message: kubelet has sufficient PID available
      reason: KubeletHasSufficientPID
      status: "False"
      type: PIDPressure
    - lastHeartbeatTime: "2020-06-04T17:59:06Z"
      lastTransitionTime: "2020-06-04T16:23:35Z"
      message: kubelet is posting ready status. AppArmor enabled
      reason: KubeletReady
      status: "True"
      type: Ready
    daemonEndpoints:
      kubeletEndpoint:
        Port: 10250
    nodeInfo:
      architecture: amd64
      bootID: 047e23bc-ce8e-4b53-afc7-475d3e68b878
      containerRuntimeVersion: containerd://1.2.5
      kernelVersion: 4.13.0-38-generic
      kubeProxyVersion: v1.18.3
      kubeletVersion: v1.18.3
      machineID: b9345171accd4bbdb68fb20877168a24
      operatingSystem: linux
      osImage: Ubuntu 16.04.6 LTS
      systemUUID: 465BFA80-9AA3-0000-0000-000000000000
kind: List
metadata:
  resourceVersion: ""
  selfLink: ""
$
```

To debug, the following command should show the logs for a running container:

```shell
$ microk8s.kubectl logs my-nginx-9b596c8c4-4jp7d
$
```

However, I don't see any logs regardless of which of the 3 replicas, i.e., pods, I query with this command. But in the web browser I see that the nginx container is running (I get the "Welcome to nginx!" page when I hit the RPi4 IP address + the port the service is exposed on).


Interestingly enough, the `top` command seems not to work with microk8s

```shell
$ paul@terminus:~$ microk8s.kubectl top nodes
Error from server (NotFound): the server could not find the requested resource (get services http:heapster:)
$
```

The `microk8s.kubectl top pods` command returns the same error even if I have pods running (checked this on my microk8s cluster on RPi4).


To enable tab completion for `microk8s` commands and resources for the current terminal session (the `bash-completion` package needs to be installed):

```shell
$ source <(microk8s.kubectl completion bash)
```

To permanently enable the tab completion:

```shell
$ echo "source <(microk8s.kubectl completion bash)" >> ${HOME}/.bashrc
```

```shell
$ microk8s kubectl get all --all-namespaces
```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```

```shell

```