terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.45.0"
    }

}
}

# Create a VPC with a /16 CIDR block and a subnet with a /24 CIDR block within the VPC  aws
provider "aws" {
    region = "ca-central-1"
}


# Create a VPC
resource "aws_vpc" "vpc_demo" {
    cidr_block = "10.0.0.0/16"
    tags = {
      "Name" = "demo1-vpc"
    }
}

# Create
resource "aws_subnet" "subnet1" {
    vpc_id     = aws_vpc.vpc_demo.id
    cidr_block = "10.0.1.0/24"
     tags = {
      "Name" = "demo1"
    }
    depends_on = [ aws_vpc.vpc_demo ]
}

# Create a ec2 instance 
resource "aws_instance" "ubuntu_public_linux_1" {
    ami           = "ami-05d4121edd74a9f06"
    instance_type = "t2.micro"
    subnet_id     = aws_subnet.subnet1.id
    key_name = "polybot_master"
    associate_public_ip_address = true
    vpc_security_group_ids = [aws_security_group.secure-group_demo.id]

    tags = {
        Name = "demo1"
    }
  
}

# Create a security group
resource "aws_security_group" "secure-group_demo" {
  name        = "web_server_secure_group"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.vpc_demo.id

# Egress rule
dynamic "ingress" {
  for_each = ["80", "443", "8080", "8081", "9000"]
  content {
    from_port = ingress.value
    to_port = ingress.value
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
# Inbound rule
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

    tags = {
        Name = "demo1"
    }
}

