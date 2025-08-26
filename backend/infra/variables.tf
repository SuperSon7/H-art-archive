variable "project" { type = string }
variable "env"     { type = string }   # dev|stg|prod
variable "region"  { type = string }

# 브라우저 업로드 허용 오리진
variable "cors_allowed_origins" {
  type = list(string)
  default = ["http://localhost:5173", "https://app.example.com"]
}

# CloudFront 배포 ID (assets 버킷 정책에 사용)
variable "cloudfront_distribution_id" {
  type = string
  default = "REPLACE_WITH_DIST_ID"
}


# ===== S3 Bucket =====
variable "base_bucket_name" {
  type = string
  default = "solren-image-bucket"
}

# TODO: 실제 계정 필요
variable "account_id" {
  type = string
  default = "123456789012"
}
