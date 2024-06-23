FROM ultralytics/yolov5:latest-cpu

# Install AWS CLI
RUN apt-get update && apt-get install -y awscli

# Upgrade pip and install Python dependencies
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download YOLOv5 model weights
RUN curl -L https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt -o yolov5s.pt

# Set environment variables
ENV BUCKET_NAME=youssefs-bucket

# Copy your application code
COPY . .
EXPOSE 8081
# Run your application
CMD ["python3", "app.py"]