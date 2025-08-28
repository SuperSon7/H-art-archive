resource "aws_s3_bucket" "profile_images" {
  bucket = var.bucket_name

  tags = {
    Name        = "ProfileImageBucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_public_access_block" "profile_images" {
  bucket = aws_s3_bucket.profile_images.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "s3_bucket_policy" {
  statement {
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.profile_images.arn}/*"
    ]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}

resource "aws_iam_role_policy" "server_presigned_policy" {
    name = "PresignedS3Policy"
    role = aws_iam_role.backend_role.name
    policy = data.aws_iam_policy_document.presigned_url_policy.json
}

