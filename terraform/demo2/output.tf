# ##############################################################################
# # Outputs File
# #
# # Here is where we store the output values for all the variables used in our
# # Terraform code. If you create a variable with no default, the user will be
# # prompted to enter it (or define it via config file or command line flags.)
# 
# 
# 
output "vpc" {
  description = "The ID of the VPC."
  value       = aws_vpc.vpc.id
}

output "region" {
  description = "The ID of the region."
  value       = var.region
  
}

output "route_table" {
  description = "The ID of the route table."
  value       = aws_route_table.public-route-table.id
}

output "security_group" {
  description = "The ID of the security group."
  value       = aws_security_group.polybot-secure-group.id
}

output "ec2-1" {
  description = "The ID of the ec2."
  value       = aws_instance.ubuntu_public_linux_2.id
}


output "ec2-2" {
  description = "The ID of the ec2."
  value       = aws_instance.ubuntu_public_linux_2.id
}

output "ec2-1-public_ip" {
  description = "The public IP of the ec2."
  value       = aws_instance.ubuntu_public_linux_1.public_ip
}

output "ec2-2-public_ip" {
  description = "The public IP of the ec2."
  value       = aws_instance.ubuntu_public_linux_2.public_ip
}



# If yo want to see the output to json of the terraform code, you can run the following command: "terraform output -json > output.json"