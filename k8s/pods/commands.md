# Running a Pod on Kubernetes with Nginx Image

In this tutorial, we will learn how to run a pod on a Kubernetes cluster using the nginx image.

## Prerequisites

Before we begin, make sure you have the following:

- A running Kubernetes cluster
- `kubectl` command-line tool installed and configured to connect to your cluster

## Step 1: Create a Pod manifest file

Create a file named `nginx-pod.yaml` and add the following content:


apiVersion: v1
kind: Pod
metadata:
    name: nginx-pod
spec:
    containers:
    - name: nginx
        image: nginx

## Or you can run the following command

kubectl run app-nginx-1 --image=nginx:1.25.5 --port=8000

## Run the following command get information about the pod and its dependencies

kubectl describe pod app-nginx-1

## Run to enter into the pod 

kubectl exec -it app-nginx-1 -- /bin/bash


