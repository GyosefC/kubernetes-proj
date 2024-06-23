##############################################################################
# Variables File
#
# Here is where we store the default values for all the variables used in our
# Terraform code. If you create a variable with no default, the user will be
# prompted to enter it (or define it via config file or command line flags.)



variable "region" {
  description = "The region where the virtual network is created."
  type = string
  default     = "eu-central-1"
}


variable "cidr_block_vpc" {
  description = "The address space that is used by the virtual network. You can supply more than one address space. Changing this forces a new resource to be created."
  type = string
  default     = "10.0.0.0/16"
}

variable "route_table" {
    description = "The route table to associate with the subnet."
    type = string
    default = "0.0.0.0/0"
}

variable "availability_zone_a" {
  description = "The availability_zone where the virtual network is created."
  type = string
  default     = "eu-central-1a"
}
variable "availability_zone_b" {
  description = "The availability_zone where the virtual network is created."
  type = string
  default     = "eu-central-1b"
}

variable "tagging" {
  description = "The availability_zone where the virtual network is created."
  type = string
  default     = "demo2"
  
}


