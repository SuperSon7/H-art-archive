/*
 * # AWS Github OIDC Provider Terraform Module
*/
resource "aws_iam_openid_connect_provider" "this" {
  count = var.create_oidc_provider ? 1 : 0
  client_id_list = [
    "sts.amazonaws.com",
  ]
  thumbprint_list = [var.github_thumbprint]
  url             = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_role" "this" {
  count                = var.create_oidc_role ? 1 : 0
  name                 = var.role_name
  description          = var.role_description
  max_session_duration = var.max_session_duration
  assume_role_policy   = join("", data.aws_iam_policy_document.this[0].*.json)
  tags                 = var.tags
  # path                  = var.iam_role_path
  # permissions_boundary  = var.iam_role_permissions_boundary
  depends_on = [aws_iam_openid_connect_provider.this]
}

resource "aws_iam_role_policy_attachment" "attach" {
  count = var.create_oidc_role ? length(var.oidc_role_attach_policies) : 0

  policy_arn = var.oidc_role_attach_policies[count.index]
  role       = join("", aws_iam_role.this.*.name)

  depends_on = [aws_iam_role.this]
}

# IAM Role이 누구로부터 assume될 수 있는지 정의
data "aws_iam_policy_document" "this" {
  count = var.create_oidc_role ? 1 : 0

  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test   = "StringLike"
      values = [
        for repo in var.repositories :
        "repo:%{if length(regexall(":+", repo)) > 0}${repo}%{else}${repo}:*%{endif}"
      ]
      variable = "token.actions.githubusercontent.com:sub"
    }

    principals {
      identifiers = [try(aws_iam_openid_connect_provider.this[0].arn, var.oidc_provider_arn)]
      type        = "Federated"
    }
  }
}

# ECR Push Policy
resource "aws_iam_policy" "ecr_push_policy" {
  name        = "ECRPushPolicy"
  description = "Allow GitHub Actions to login, push, and describe ECR images"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteMultipartUpload",
          "ecr:GetDownloadUrlForLayer",
          "ecr:InitiateMultipartUpload",
          "ecr:PutImage",
          "ecr:UploadLayerPart",
          "ecr:DescribeRepositories",
          "ecr:CreateRepository",
          "ecr:BatchGetImage"
        ]
        Resource = "arn:aws:ecr:${var.region}:${var.account_id}:repository/${var.ecr_repository_name}"
      }
    ]
  })
}

# S3 Upload Policy
resource "aws_iam_policy" "s3_upload_policy" {
  name        = "S3UploadPolicy"
  description = "Allow GitHub Actions to upload static assets to S3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:GetObject",
          "s3:DeleteObject"
        ]
        Resource = "arn:aws:s3:::${var.s3_bucket_name}/*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "s3:ListBucket"
        ]
        Resource = "arn:aws:s3:::${var.s3_bucket_name}"
      }
    ]
  })
}
