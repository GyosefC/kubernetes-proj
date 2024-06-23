# Create Route Table and Add Public Route
# terraform aws create route table

resource "aws_route_table" "public-route-table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = var.route_table
    gateway_id = aws_internet_gateway.my_ig.id
  }
  tags = {
    Name =   format("%s-Public Route Table-terraform", var.tagging)
  }
}

# Associate Public Subnet 1/2 to "Public Route Table"
# terraform aws associate subnet with route table
resource "aws_route_table_association" "public-subnet-1-route-table-association" {
  subnet_id      = aws_subnet.public-subnet-1a.id
  route_table_id = aws_route_table.public-route-table.id
}
