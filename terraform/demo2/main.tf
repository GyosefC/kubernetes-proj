terraform {

    backend "s3" {
    bucket = "alexey-yolo"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.45.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "3.1.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.1.0"
    }
  }
    required_version = ">= 0.13"  # Specify the minimum Terraform version required

}

# create terrafrom state file in s3 bucket


provider "aws" {
  region = var.region
}


