resource "aws_s3_bucket" "geugeu" {
  bucket = "geugeu"
}

resource "aws_s3_bucket_public_access_block" "geugeu" {
  bucket = aws_s3_bucket.geugeu.id

  block_public_acls       = true
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = false
}

resource "aws_s3_bucket_versioning" "geugeu" {
  bucket = aws_s3_bucket.geugeu.id

  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_iam_policy_document" "allow_s3_access" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.geugeu.arn}/images/*",
    ]
  }
}

resource "aws_s3_bucket_policy" "allow_s3_access" {
  bucket = aws_s3_bucket.geugeu.id
  policy = data.aws_iam_policy_document.allow_s3_access.json
}
