/*
 * # AWS Github OIDC Provider Terraform Module
*/
locals {
  # repositories × allowed_refs → "repo:ORG/REPO:ref:<ref>"
  derived_subs = distinct(flatten([
    for repo in var.repositories : [
      for ref in var.allowed_refs : "repo:${repo}:ref:${ref}"
    ]
  ]))

  # override list if exists
  allowed_subs_effective = length(var.allowed_subs_override) > 0 ? var.allowed_subs_override : local.derived_subs
}

#--------------------------------
# OIDC Provider
#--------------------------------
resource "aws_iam_openid_connect_provider" "this" {
  count            = var.create_oidc_provider ? 1 : 0
  url              = "https://token.actions.githubusercontent.com"
  client_id_list   = ["sts.amazonaws.com"]
  thumbprint_list  = var.github_thumbprints
}

#--------------------------------
# Trust Policy for GitHub OIDC
#--------------------------------
data "aws_iam_policy_document" "assume" {
  count = var.create_oidc_role ? 1 : 0

  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    # aud = sts.amazonaws.com
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = [var.oidc_audience]
    }

    # sub: repositories × refs, 또는 override
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = local.allowed_subs_effective
    }

    principals {
      type = "Federated"
      identifiers = [
        # 새 Provider가 있으면 그걸, 아니면 외부 주입 ARN 사용
        coalesce(try(aws_iam_openid_connect_provider.this[0].arn, null), var.oidc_provider_arn)
      ]
    }
  }
}

#--------------------------------
# IAM Role for GitHub OIDC
#--------------------------------
resource "aws_iam_role" "this" {
  count                = var.create_oidc_role ? 1 : 0
  name                 = var.role_name
  description          = var.role_description
  max_session_duration = var.max_session_duration
  assume_role_policy   = data.aws_iam_policy_document.assume[0].json
  tags                 = var.tags

  # NOTE: external provider can be used, so depends_on is omitted
}

#--------------------------------
# Attach managed policies (least privilege recommended)
#--------------------------------
resource "aws_iam_role_policy_attachment" "attach" {
  count      = var.create_oidc_role ? length(var.oidc_role_attach_policies) : 0
  role       = aws_iam_role.this[0].name
  policy_arn = var.oidc_role_attach_policies[count.index]
}
