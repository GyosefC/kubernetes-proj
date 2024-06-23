


data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}



resource "aws_instance" "ubuntu_public_linux_1" {
  ami                        = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  vpc_security_group_ids      = [aws_security_group.polybot-secure-group.id]
  subnet_id                   = aws_subnet.public-subnet-1a.id
  associate_public_ip_address = true
  key_name                    = "polybot_master"
  user_data                   = file("userdata.sh")
  tags = {
    Name        =  format("%s-tf", var.tagging)
    environment = "tf"
  }
  
}


resource "aws_instance" "ubuntu_public_linux_2" {
  ami                     = data.aws_ami.ubuntu.id
  instance_type           = "t2.micro"
  vpc_security_group_ids  = [aws_security_group.polybot-secure-group.id]
  subnet_id               = aws_subnet.public-subnet-1a.id
  key_name                = "polybot_master"
  user_data               = base64encode(file("userdata.sh"))
  tags = {
    Name        =  format("%s-tf", var.tagging)  
    environment = "tf"
  }


}
