environment = "dev"
role_name   = "github-oidc-role"
repositories = ["SuperSon7/H-art-archive"]
tags = {
  Project     = "h-art"
  Environment = "dev"
  Owner       = "vanillabean"
  Terraform   = "true"
  ManagedBy   = "Terraform"
}

oidc_role_attach_policies = [
  "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"  # 예시
]

max_session_duration = 3600  # 1시간으로 제한