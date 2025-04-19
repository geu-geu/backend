resource "aws_s3_bucket" "geugeu" {
  bucket = "geugeu"
}

resource "aws_s3_bucket_public_access_block" "geugeu" {
  bucket = aws_s3_bucket.geugeu.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

data "aws_iam_policy_document" "public_read_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.geugeu.arn}/profile-images/*"]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    effect = "Allow"
  }
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.geugeu.id
  policy = data.aws_iam_policy_document.public_read_policy.json
}

data "aws_iam_policy_document" "presign_upload_policy" {
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.geugeu.arn}/profile-images/*"]
    effect    = "Allow"
  }
}

resource "aws_iam_policy" "s3_presign_upload" {
  name   = "S3PresignedUploadPolicy"
  policy = data.aws_iam_policy_document.presign_upload_policy.json
}
