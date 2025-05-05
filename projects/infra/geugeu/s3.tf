resource "aws_s3_bucket" "geugeu" {
  bucket = "geugeu"
}

resource "aws_s3_bucket_public_access_block" "geugeu" {
  bucket = aws_s3_bucket.geugeu.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "geugeu" {
  bucket = aws_s3_bucket.geugeu.id

  versioning_configuration {
    status = "Enabled"
  }
}
