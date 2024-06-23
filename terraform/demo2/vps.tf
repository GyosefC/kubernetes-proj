# tflint:disable terraform_required_providers
resource "aws_vpc" "vpc" {
  cidr_block       = var.cidr_block_vpc
  instance_tenancy = "default"

  tags = {
    Name = format("%s-tf", var.tagging)
  }
}
