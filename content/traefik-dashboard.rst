=============================================
Adding Trafik Dashboard to Kubernetes Cluster
=============================================

:title: Adding Trafik Dashboard to Kubernetes Cluster
:date: 20190101
:author: maxrichter
:tags: Kubernetes, Raspberry Pi
:cover: images/spacex.jpg


.. image:: /images/traefik/traefik.png
    :align: center
    :height: 300px
    :width: 200 px
    :alt: Traefik

After some break on this project, I am back with new features.
The first blog post was also updated to the latest version of Kubernetes and Flannel.

In this short entry, I will show you how to add the
`Treafik Dashboard <https://docs.traefik.io/configuration/api/>`_ to your Kubernetes cluster.

Installation of the ingress and service
---------------------------------------

If you have followed my blog, you have installed Traefik as a Deployment object (`traefik-deployment.yaml`).
To install the service and ingress execute on your master node:

.. code-block:: bash

    kubectl apply -f https://raw.githubusercontent.com/containous/traefik/master/examples/k8s/ui.yaml

To retrieve the Node-Port, execute on your master node and take the `admin` node port:

.. code-block:: bash

    kubectl describe svc traefik-ingress-service -n kube-system


If you execute on your master node:

.. code-block:: bash

    curl http://<IP-MASTER-NODE>:<NODE-PORT>
    <a href="/dashboard/">Found</a>.

you should see the same output as I did.

You should now be able to access the dashboard outside of your cluster:

.. image:: /images/traefik/traefik_dashboard.png
    :align: center
    :alt: Traefik Dashboard