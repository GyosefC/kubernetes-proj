# Create first flask application on kubernetes.

1. Create first flask application  on python
2. create Dockerfile
3. Run docker build
4. Upload image to docker repository (ECR or Docker)
5. Create manifest file for kubernetes with yaml configuration
6. run kubernetes command to deploy app ("kubectl apply -f .\deployment.yaml")
7. Run kubernetes command to port forward ports ("kubectl port-forward deployment/<deployment-name> <local-port>:<remote-port>)
   