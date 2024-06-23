# Grafana Helm Chart

This repository contains the Helm chart to install Grafana on Kubernetes using Helm.

## Prerequisites

- Kubernetes cluster
- Helm

## Installation

1. Add the Grafana Helm repository:

    ```bash
    helm repo add grafana https://grafana.github.io/helm-charts
    ```

2. Update the Helm repositories:

    ```bash
    helm repo update
    ```

3. Install Grafana using Helm:

    ```bash
    helm install grafana grafana/grafana
    ```

4. Verify the installation:

    ```bash
    kubectl get pods
    ```

    You should see the Grafana pod running.

## Accessing Grafana

To access Grafana, you need to expose it as a service. You can use a LoadBalancer, NodePort, or Ingress depending on your Kubernetes setup.

For example, to expose Grafana using a NodePort:

1. Get the Grafana service details:

    ```bash
    kubectl get svc
    ```

    Note down the port number associated with the Grafana service.

2. Access Grafana using the NodePort:

    ```
    http://<node-ip>:<node-port>
    ```

    Replace `<node-ip>` with the IP address of one of your Kubernetes nodes, and `<node-port>` with the port number noted in the previous step.

## Configuration

You can customize the Grafana installation by modifying the values in the Helm chart. Refer to the [Grafana Helm chart documentation](https://grafana.github.io/helm-charts) for more information.

## Uninstallation

To uninstall Grafana, run the following command:

    ```bash
    helm unstall grafana grafana/grafana
    ```

## Add values.yaml

 ```bash
 helm show grafana
```