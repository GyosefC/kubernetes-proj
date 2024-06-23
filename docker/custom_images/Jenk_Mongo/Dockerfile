# Use an official Jenkins image as base
FROM jenkins/jenkins:latest as jenkins

# Use an official MongoDB image as base
FROM mongo:latest as mongo

# Final stage
FROM ubuntu:latest

# Copy Jenkins from jenkins stage
COPY --from=jenkins /var/jenkins_home /var/jenkins_home

# Copy MongoDB from mongo stage
COPY --from=mongo /data/db /data/db

# Install necessary dependencies
RUN apt-get update && apt-get install -y openjdk-8-jdk wget

# Expose port for Jenkins and MongoDB
EXPOSE 8080 27017

# Start Jenkins and MongoDB
CMD java -jar /var/jenkins_home/jenkins.war & mongod --dbpath /data/db