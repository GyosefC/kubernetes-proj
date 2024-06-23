FROM python:3.8

# example of how to install packages
RUN apt update && \
    apt install -y nano && \
    apt install -y v && \
    apt install -y curl && \
    apt install -y wget && \
    apt install -y git  

# Create a directory and set it as the working directory
WORKDIR /app     

# Copy the current directory contents into the container at /app
COPY . /app


RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 6000

CMD ["python", "app.py"]
 

