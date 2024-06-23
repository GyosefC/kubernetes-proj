
# Use the latest version of Ubuntu as a parent image
FROM ubuntu:latest

# Update the Ubuntu software repository
RUN apt-get update

# Install nginx web server
RUN apt-get install -y nginx

# Start nginx when the container launches, running it in the foreground
CMD ["nginx", "-g", "daemon off;"]