FROM ubuntu as installer
RUN apt-get update \
  && apt-get install -y curl unzip wget vim

RUN curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip \
  && unzip awscliv2.zip \
  && ./aws/install --bin-dir /aws-cli-bin/ \
  && rm -rf aws awscliv2.zip

# Install terraform
ARG TERRAFORM_VERSION=1.7.4
# Download terraform for linux
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
# Unzip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv ./kubectl /usr/local/bin/

# SNYK
RUN curl https://static.snyk.io/cli/v1.666.0/snyk-linux -o snyk \
    && chmod +x ./snyk \
    && mv ./snyk /usr/local/bin/

FROM jenkins/inbound-agent:latest
USER root
COPY --from=docker /usr/local/bin/docker /usr/local/bin/
COPY --from=installer /usr/local/aws-cli/ /usr/local/aws-cli/
COPY --from=installer /aws-cli-bin/ /usr/local/bin/
COPY --from=installer terraform /usr/local/bin/
COPY --from=installer /usr/local/bin/kubectl /usr/local/bin/
COPY --from=installer /usr/local/bin/snyk /usr/local/bin/

# Install python3
RUN apt-get update && apt-get install -y python3 python3-pip curl unzip wget vim
# Install sonar-scanner
ARG SONAR_VERSION=5.0.1.3006
RUN curl -s -L https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}.zip -o sonarscanner.zip \
  && unzip -qq sonarscanner.zip \
  && rm -rf sonarscanner.zip \
  && mv sonar-scanner-${SONAR_VERSION} sonar-scanner

# Install ansible and ansible-galaxy
RUN apt-get update && apt-get install -y ansible
RUN ansible-galaxy collection install community.general


ENV SONAR_RUNNER_HOME=/usr/local/sonar-scanner/
ENV SONAR $PATH:$SONAR_RUNNER_HOME/bin
ENV PATH $SONAR_RUNNER_HOME:$PATH

