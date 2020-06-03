==========================================
Kubernetes running on Raspberry Pi cluster
==========================================

:title: Kubernetes running on Raspberry Pi cluster
:date: 20180510
:author: maxrichter
:tags: Kubernetes, Raspberry Pi
:cover: images/spacex.jpg

.. image:: /images/traefik/raspberry-pi-cluster.png
    :align: center
    :alt: Raspberry Pi Cluster

Is not nice to have the resources to start builiding a distributed systems with only around 150€?
Obviously this is more of an experiment than a production ready solution - but in order to get your hands dirty it is more than enough!

That is why I decided to buy all the utilities to setup up my own Kubernetes Cluster on Raspberry Pi's (Modell 3).
Finally I ended up with 4 of them, with one running as the master and 3 running as nodes.

This post is inspired by the `Hypriot Raspberry Kubernetes Cluster <https://blog.hypriot.com/post/setup-kubernetes-raspberry-pi-cluster>`_ blogpost from the Hypriot developers.

Flash HypriotOS on your SD cards
--------------------------------

1. The first step is to flash HypriotOS on all your SD cards.
    * Therefore you first have to install hypriot/flash on your OS from the `Hypriot Flash repository <https://github.com/hypriot/flash>`_ on GitHub.

2. Flash the SD card(s)
    * Adapt the **wifi-user-data.yml** with the correct SSID and password if you want to use wifi as well as setting the **hostname**
    * Further you can adapt the **no-uart-config.txt** and set **enable_uart=0**.
    * Then run following command to flash the SD card with hypriot:

    .. code-block:: bash

        flash --userdata /Users/maxrichter/flash/wifi-user-data.yml --bootconf /Users/maxrichter/flash/no-uart-config.txt https://github.com/hypriot/image-builder-rpi/releases/download/v1.9.0/hypriotos-rpi-v1.9.0.img.zip

    *  This resulted for me in 4 machines:

    .. code-block:: bash

         $ master.local
         $ node01.local
         $ node02.local
         $ node03.local

    * You should be able to connect to a raspberry with: **ssh pirate@master.local**
    * Login with username **pirate**, password **hypriot**
    * This should result in:

    .. image:: /images/traefik/hypriot_1.png
        :align: center
        :alt: Hypriot 1

Install Kubernetes
------------------

1. Execute the following steps on every node:

    Get root privileges:

    .. code-block:: bash

        $ sudo su -

    First, trust the kubernetes APT key and add the official APT Kubernetes repository on every node:

    .. code-block:: bash

         $ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
         $ echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list

    and then just install kubeadm on every node:

    .. code-block:: bash

        $ apt-get update && apt-get install -y kubeadm

2. Execute the following on the master node:

    After the previous command has been finished, initialize Kubernetes on the "master" node with:

    .. code-block:: bash

        $ apt-get update && apt-get install -y kubeadm$ kubeadm init --pod-network-cidr 10.244.0.0/16 --apiserver-advertise-address=192.168.178.30

    It is important that you add the **--pod-network-cidr** command as given here, because we will use flannel. If you are connected via WIFI instead of Ethernet, add **--apiserver-advertise-address=<wifi-ip-address>** as parameter to kubeadm init in order to publish Kubernetes’ API via WiFi. Feel free to explore the other options that exist for kubeadm init.
    After Kubernetes has been initialized, the last lines of your terminal should look like this:

    .. image:: /images/traefik/hypriot_2.png
            :align: center
            :alt: Hypriot 2

    To start using your cluster, you need to run (as a regular user) in the master node do:

    .. code-block:: bash

         $ mkdir -p $HOME/.kube
         $ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
         $ sudo chown $(id -u):$(id -g) $HOME/.kube/config

3. Go to every Node and enter the join command from the master:

.. code-block:: bash

    $ kubeadm join 192.168.178.31:6443 --token tkbpzm.2mlrmy3dlw8t5d3q --discovery-token-ca-cert-hash sha256:6cc738b32406b2f21292b1b0106685105391a4a3f9d5bac5f8e9d3b9193b5e62

4. In the master node execute:

.. code-block:: bash

    $ kubectl get nodes

Which should result in (but you will not see `ready` at this stage because we first need to install flannel):

    .. image:: /images/traefik/get-nodes.png
            :align: center
            :alt: Hypriot Get Nodes

flannel
-------

1. You can check out the `Flannel GitHub repository <https://github.com/coreos/flannel>`_.
2. Run the following command on the master node:

    .. code-block:: bash

        $ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

    .. image:: /images/traefik/flannel.png
            :align: center
            :alt: Flannel

3. Then wait until all flannel and all other cluster-internal Pods are Running before you continue:

    .. code-block:: bash

        $ kubectl get po --all-namespaces

4. That’s all for the setup of Kubernetes! Next, let’s actually spin up a service on the cluster!

    .. image:: /images/traefik/show-namespaces.png
            :align: center
            :alt: Flannel Show Namespaces
