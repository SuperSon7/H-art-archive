# ===== S3 Bucket =====
module "upload" {
  source = "./modules/s3_base"
  bucket_name = "upload-${var.base_bucket_name}"
    # tags = {
    #     Name        = "ImageUploadBucket"
    #     Environment = "Dev"
    # }
    }

module "assets" {
  source = "./modules/s3_base"
  bucket_name = "assets-${var.base_bucket_name}"
}

module "logs" {
  source = "./modules/s3_base"
  bucket_name = "logs-${var.base_bucket_name}"
}

# ===== UPLOADS CONFIGURATION =====
# S3: Upload bucket cors configuration
resource "aws_s3_bucket_cors_configuration" "upload" {
  bucket = module.upload.id

  cors_rule {
    allowed_methods = ["PUT"]
    allowed_headers = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 300
    allowed_origins = var.cors_allowed_origins
  }
}

# S3: Upload bucket lifecycle configuration
resource "aws_s3_bucket_lifecycle_configuration" "upload" {
  bucket = module.upload.id

  rule {
    id     = "abort-multipart"
    status = "Enabled"
    abort_incomplete_multipart_upload {
        days_after_initiation = 7
    }
  }

  rule {
    id     = "expire-raw"
    status = "Enabled"
    filter { prefix = "raw/" }
    expiration { days = 14 }
  }
}

# ===== ASSETS CONFIGURATION =====
# S3: Assets bucket versioning
resource "aws_s3_bucket_versioning" "assets" {
  bucket = module.assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3: Assets bucket lifecycle configuration
resource "aws_s3_bucket_lifecycle_configuration" "assets" {
  bucket = module.assets.id

  # version management
  rule {
    id     = "noncurrent-versions"
    status = "Enabled"

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 365
    }
  }
}

# ===== LOGS CONFIGURATION =====
resource "aws_s3_bucket_policy" "logs" {
  bucket = module.logs.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = { Service = "logging.s3.amazonaws.com" },
        Action   = "s3:PutObject",
        Resource = "${module.logs.arn}/*",
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = var.account_id
          }
        }
      }
    ]
  })
}

# S3: Logs bucket lifecycle
resource "aws_s3_bucket_lifecycle_configuration" "logs" {
  bucket = module.logs.id

  rule {
    id     = "raw-to-glacier-then-deep-archive"
    status = "Enabled"

    filter { prefix = "raw/" }

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }
  }
}

# (필요 시) 퍼블릭/업로드 버킷에 로그 타깃 설정
resource "aws_s3_bucket_logging" "uploads" {
  bucket        = module.upload.id
  target_bucket = module.logs.id
  target_prefix = "s3/upload/"
}

resource "aws_s3_bucket_logging" "public" {
  bucket        = module.assets.id
  target_bucket = module.logs.id
  target_prefix = "s3/assets/"
}

# ===== CLOUDFRONT =====
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "assets-oac-${local.suffix}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "cdn" {
  enabled = true

  origin {
    domain_name              = module.assets.domain
    origin_id                = "s3-assets"
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  default_cache_behavior {
    target_origin_id       = "s3-assets"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
  }

  restrictions {
    geo_restriction { restriction_type = "none" }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# ===== S3: Upload bucket policy =====
# ---------------------------
# CloudFront OAC에서 채워 넣을 값(CloudFront 리소스에서 생성되는 OAC 서명자)
# 실제 배선 시 aws_cloudfront_distribution와 aws_cloudfront_origin_access_control 리소스와 함께,
# 아래 버킷 정책의 Principal/Condition을 업데이트해 연결.
# ---------------------------
data "aws_caller_identity" "current" {}

# 예시 버킷 정책(CloudFront OAC 전용 접근) — Principal/OAC ID는 배선 시 치환
resource "aws_s3_bucket_policy" "public_oac_only" {
  bucket = module.assets.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "AllowCloudFrontServicePrincipalReadOnly"
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "${module.assets.arn}/*"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.cdn.arn
          }
        }
      }
    ]
  })
}

# ===== S3: Upload bucket policy =====
data "aws_iam_policy_document" "s3_bucket_policy" {
  statement {
    actions = ["s3:GetObject"]
    resources = [
      "${module.upload.arn}/*"
    ]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}

# ---------------------------
# S3: Presigned url policy
# ---------------------------
resource "aws_iam_role_policy" "server_presigned_policy" {
    name = "PresignedS3Policy"
    role = aws_iam_role.backend_role.name
    policy = data.aws_iam_policy_document.presigned_url_policy.json
}
