// vpc

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project}-vpc"
  }
}

// public subnet

resource "aws_subnet" "public" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.main.id

  cidr_block        = "10.0.${var.cidr_public[count.index]}.0/20"
  availability_zone = element(var.availability_zones, count.index)

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project}-subnet-public${count.index + 1}-${element(var.availability_zones, count.index)}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-rtb-public"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(var.availability_zones)
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-igw"
  }
}

resource "aws_route" "igw" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

// private subnet

resource "aws_subnet" "private" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.main.id

  cidr_block        = "10.0.${var.cidr_private[count.index]}.0/20"
  availability_zone = element(var.availability_zones, count.index)

  tags = {
    Name = "${var.project}-subnet-private${count.index + 1}-${element(var.availability_zones, count.index)}"
  }
}

resource "aws_route_table" "private" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-rtb-private${count.index + 1}-${element(var.availability_zones, count.index)}"
  }
}

resource "aws_route_table_association" "private" {
  count          = length(var.availability_zones)
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}

// S3 endpoint

resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.default_region}.s3"

  tags = {
    Name = "s3-${var.project}"
  }
}

resource "aws_vpc_endpoint_route_table_association" "s3" {
  count           = length(var.availability_zones)
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
  route_table_id  = aws_route_table.private[count.index].id
}

// DynamoDB endpoint

resource "aws_vpc_endpoint" "dynamodb" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.default_region}.dynamodb"

  tags = {
    Name = "dynamodb-${var.project}"
  }
}

resource "aws_vpc_endpoint_route_table_association" "dynamodb" {
  count           = length(var.availability_zones)
  vpc_endpoint_id = aws_vpc_endpoint.dynamodb.id
  route_table_id  = aws_route_table.private[count.index].id
}
