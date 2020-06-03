---
layout: post
title: Kubernetes running on Raspberry Pi cluster
---

![_config.yml]({{ site.baseurl }}/images/raspberry-pi-cluster.png)

Is not nice to have the resources to start builiding a distributed systems with only around 150€?
Obviously this is more of an experiment than a production ready solution - but in order to get your hands dirty it is more than enough!

That is why I decided to buy all the utilities to setup up my own Kubernetes Cluster on Raspberry Pi's (Modell 3).
Finally I ended up with 4 of them, with one running as the master and 3 running as nodes.

This post is inspired by the [Hypriot Raspberry Kubernetes Cluster](https://blog.hypriot.com/post/setup-kubernetes-raspberry-pi-cluster) blogpost from the Hypriot developers.

## Flash HypriotOS on your SD cards

1. The first step is to flash HypriotOS on all your SD cards.
   1. Therefore you first have to install hypriot/flash on your OS from the [Hypriot Flash repository](https://github.com/hypriot/flash) on GitHub.

2. Flash the SD card(s)
 * Adapt the **`wifi-user-data.yml`** with the correct SSID and password if you want to use wifi as well as setting the **`hostname`**
 * Further you can adapt the **`no-uart-config.txt`** and set **`enable_uart=0`**.
 * Then run following command to flash the SD card with hypriot:
 ~~~ shell
 flash --userdata /Users/maxrichter/flash/wifi-user-data.yml --bootconf /Users/maxrichter/flash/no-uart-config.txt https://github.com/hypriot/image-builder-rpi/releases/download/v1.9.0/hypriotos-rpi-v1.9.0.img.zip
 ~~~ 
 * This resulted for me in 4 machines:
 ~~~ shell
 $ master.local
 $ node01.local
 $ node02.local
 $ node03.local
 ~~~ 
 * You should be able to connect to a raspberry with: **`ssh pirate@master.local`**
 * Login with username **`pirate`**, password **`hypriot`**
 * This should result in:
 ![_config.yml]({{ site.baseurl }}/images/hypriot_1.png)

## Install Kubernetes

1. Execute the following steps on every node:
 * Get root privileges:
 ~~~ shell
 $ sudo su -
 ~~~
 * First, trust the kubernetes APT key and add the official APT Kubernetes repository on every node:
 ~~~ shell
 $ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
 $ echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
 ~~~
 * and then just install kubeadm on every node:
 ~~~ shell
 $ apt-get update && apt-get install -y kubeadm
 ~~~
2. Execute the following on the master node:
 * After the previous command has been finished, initialize Kubernetes on the "master" node with:
 ~~~ shell
 $ apt-get update && apt-get install -y kubeadm$ kubeadm init --pod-network-cidr 10.244.0.0/16 --apiserver-advertise-address=192.168.178.30
 ~~~
 * It is important that you add the **`--pod-network-cidr`** command as given here, because we will use flannel.
If you are connected via WIFI instead of Ethernet, add **`--apiserver-advertise-address=<wifi-ip-address>`** as parameter to kubeadm init in order to publish Kubernetes’ API via WiFi. Feel free to explore the other options that exist for kubeadm init.
 * After Kubernetes has been initialized, the last lines of your terminal should look like this:
![_config.yml]({{ site.baseurl }}/images/hypriot_2.png)
 * To start using your cluster, you need to run (as a regular user) in the master node do:
 ~~~ shell
 $ mkdir -p $HOME/.kube
 $ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
 $ sudo chown $(id -u):$(id -g) $HOME/.kube/config
 ~~~
3. Go to every Node and enter the join command from the master:
 ~~~ shell
 $ kubeadm join 192.168.178.31:6443 --token tkbpzm.2mlrmy3dlw8t5d3q --discovery-token-ca-cert-hash sha256:6cc738b32406b2f21292b1b0106685105391a4a3f9d5bac5f8e9d3b9193b5e62
 ~~~
4. In the master node execute:
 ~~~ shell
 $ kubectl get nodes
 ~~~
 * Which should result in (but you will not see `ready` at this stage because we first need to install flannel):
 ![_config.yml]({{ site.baseurl }}/images/get-nodes.png)
	
## flannel

1. You can check out the [Flannel GitHub repository](https://github.com/coreos/flannel).
2. Run the following command on the master node:
 ~~~ shell
 $ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
 ~~~
![_config.yml]({{ site.baseurl }}/images/flannel.png)
3. Then wait until all flannel and all other cluster-internal Pods are Running before you continue:
 ~~~ shell
 $ kubectl get po --all-namespaces
 ~~~
4. That’s all for the setup of Kubernetes! Next, let’s actually spin up a service on the cluster!
![_config.yml]({{ site.baseurl }}/images/show-namespaces.png)

## Test your setup with a tiny service

1. Let’s start a simple service so see if the cluster actually can publish a service:
 ~~~ shell
 $ kubectl run hypriot --image=hypriot/rpi-busybox-httpd --replicas=3 --port=80
 ~~~
 * This command starts set of containers called hypriot from the image `hypriot/rpi-busybox-httpd` and defines the port the container listens on at `80`. The service will be replicated with 3 containers.
2. Next, expose the Pods in the above created Deployment in a Service with a stable name and IP:
 ~~~ shell
 kubectl expose deployment hypriot --port 80
 ~~~
3. Great! Now, let’s check if all three desired containers are up and running:
 ~~~ shell
 $ kubectl get endpoints hypriot
 ~~~
 ![_config.yml]({{ site.baseurl }}/images/show-endpoints.png)
4. Let’s curl one of them to see if the service is up:
 ~~~ shell
 $ curl 10.244.1.2
 ~~~
 ![_config.yml]({{ site.baseurl }}/images/curl-service.png)
5. The HTML is the response of the service. Good, it’s up and running! Next, let’s see how we can access it from outside the cluster!

## Finally access your service from outside the cluster

1. We will now deploy an example Ingress Controller to manage incoming requests from the outside world onto our tiny service. Also, in this example we we’ll use Traefik as load balancer. Read the following notes if you wanna know more about Ingress and Traefik.
	* In contrast to Docker Swarm, Kubernetes itself does not provide an option to define a specific port that you can use to access a service. According to Lucas this is an important design decision; routing of incoming requests should be handled by a third party, such as a load balancer or a webserver, but not by the core product. The core Kubernetes should be lean and extensible, and encourage others to build tools on top of it for their specific needs.
	* Regarding load balancers in front of a cluster, there is the Ingress API object and some sample Ingress Controllers. Ingress is a built-in way of exposing Services to the outside world via an Ingress Controller that anyone can build. An Ingress rule defines how traffic should flow from the node the Ingress controller runs on to services inside of the cluster.

2. Apply RBAC:
 ~~~ shell
 $ kubectl apply -f https://raw.githubusercontent.com/containous/traefik/master/examples/k8s/traefik-rbac.yaml
 ~~~
3. Apply the new controller:
 ~~~ shell
 $ kubectl apply -f https://raw.githubusercontent.com/containous/traefik/master/examples/k8s/traefik-deployment.yaml
 ~~~
4. Then you can use the ingress and node selector they used and it should work
5. Lastly, create an Ingress object that makes Traefik load balance traffic on port 80 to the hypriot service:
 
 ~~~ shell
 cat > hypriot-ingress.yaml <<EOF
 apiVersion: extensions/v1beta1
 kind: Ingress
 metadata:
   name: hypriot
 spec:
   rules:
   - http:
       paths:
       - path: /
         backend:
           serviceName: hypriot
           servicePort: 80
 EOF
 ~~~

6. Install the ingress:
 ~~~ shell
 $ kubectl apply -f hypriot-ingress.yaml
 ~~~
7. Run this to get <NODEPORT> from the traefik-ingress-service:
 ~~~ shell
 $ kubectl get services --namespace=kube-system
 ~~~
8. Visit the loadbalancing node’s IP address (from Raspberry Master) in your browser and you should see a nice web page:
	* For me this was: **`http://192.168.178.31:32556/`**
	![_config.yml]({{ site.baseurl }}/images/hypriot-website.png)
9. If you don’t see a website there yet, run:
	* **`$ kubectl get pods`**
	* and make sure all hypriot Pods are in the Running state.

## Tear down the cluster
1. If you wanna reset the whole cluster to the state after a fresh install, just run this on each node:
 ~~~ shell
 $ sudo kubeadm reset
 $ sudo etcdctl rm --recursive registry
 $ sudo rm -rf /var/lib/cni
 $ sudo rm -rf /run/flannel
 $ sudo rm -rf /etc/cni
 ~~~
2. In addition, it is recommended to delete some additional files [as its mentioned here](https://stackoverflow.com/questions/41359224/kubernetes-failed-to-setup-network-for-pod-after-executed-kubeadm-reset/41372829#41372829).
 ~~~ shell
 $ kubectl delete -f hypriot-ingress.yaml
 $ kubectl delete ingress hypriot
 $ kubectl delete service hypriot
 $ kubectl delete deployment hypriot
 ~~~
## Kubernetes Dashboard

1. The dashboard is a wonderful interface to visualize the state of the cluster. Start it with:
 ~~~ shell
 $ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.0/src/deploy/recommended/kubernetes-dashboard-arm.yaml
 ~~~
2. Edit the kubernetes-dashboard service to use type: ClusterIP to type: NodePort, see Accessing Kubernetes Dashboard for more details.
 ~~~ shell
 $ kubectl -n kube-system edit service kubernetes-dashboard
 ~~~
3. The following command provides the port that the dashboard is exposed at on every node with the NodePort function of Services, which is another way to expose your Services to the outside of your cluster:
 ~~~ shell
 $ kubectl get services --namespace=kube-system
 ~~~
4. Then you can checkout the dashboard on any node’s IP address on that port! Make sure to use https when accessing the dashboard, for example if running on port 32486 access it at:
 ~~~ shell
 $ https://<node-ip>:32486
 ~~~
5. Visit the load-balancers page:
 ~~~ shell
 https://192.168.178.31:32486
 ~~~
6. Log in with the created token
7. [Summary for the dashboard](https://github.com/kubernetes/dashboard/wiki/Access-control)
8. In order to use the admin account:
 * create **`dashboard-admin.yaml`** file
 * **`$ nano dashboard-admin.yaml`** and copy the following:
 
 ~~~ shell
 apiVersion: rbac.authorization.k8s.io/v1beta1
 kind: ClusterRoleBinding
 metadata:
   name: kubernetes-dashboard
   labels:
     k8s-app: kubernetes-dashboard
 roleRef:
   apiGroup: rbac.authorization.k8s.io
   kind: ClusterRole
   name: cluster-admin
 subjects:
 - kind: ServiceAccount
   name: kubernetes-dashboard
   namespace: kube-system
 ~~~

* Execute **`kubectl create -f dashboard-admin.yaml`** to deploy it.
* Afterwards you can use Skip option on login page to access Dashboard.
![_config.yml]({{ site.baseurl }}/images/dashboard.png)

## Summary

These are all the step to get  Kubernetes get running on a Raspberry Pi Cluster.
If you have any questions or suggestions, please feel free to use Disqus on this blog.
