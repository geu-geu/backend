provider "aws" {
  region = var.default_region

  default_tags {
    tags = {
      "Project"              = var.project
      "Managed by Terraform" = true
    }
  }
}

resource "aws_s3_bucket" "tfstate" {
  bucket = "${var.project}-tfstate"
}

resource "aws_s3_bucket_versioning" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-lock"
  hash_key     = "LockID"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "LockID"
    type = "S"
  }
}

terraform {
  backend "s3" {
    bucket         = "geugeu-tfstate"
    key            = "geugeu/geugeu/terraform.tfstate"
    region         = "ap-northeast-2"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
