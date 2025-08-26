variable "project" {
  description = "Project name for the resources."
  default     = "h-art"
}

variable "environment" {
  description = "Environment name (dev|stage|prod)."
  type        = string
  default     = "dev"
}

variable "create_oidc_provider" {
  description = "Whether or not to create the associated oidc provider. If false, variable 'oidc_provider_arn' is required"
  type        = bool
  default     = true
}

variable "oidc_provider_arn" {
  description = "ARN of the OIDC provider to use. Required if 'create_oidc_provider' is false"
  type        = string
  default     = null
}

variable "create_oidc_role" {
  description = "Whether or not to create the OIDC attached role"
  type        = bool
  default     = true
}

# Refer to the README for information on obtaining the thumbprint.
# This is specified as a variable to allow it to be updated quickly if it is
# unexpectedly changed by GitHub.
# See: https://github.blog/changelog/2023-06-27-github-actions-update-on-oidc-integration-with-aws/
variable "github_thumbprints" {
  description = "GitHub OpenID TLS certificate thumbprints."
  type        = list(string)
  default     = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
  ]
}

# repo slash format
# Ensures each element of github_repositories list matches the
# organization/repository format used by GitHub.
variable "repositories" {
  description = "List of GitHub organization/repository names authorized to assume the role."
  type        = list(string)
  default     = []

  validation {
    condition = length([
      for repo in var.repositories : 1
      if length(regexall("^[A-Za-z0-9_.-]+?/([A-Za-z0-9_.:/-]+|\\*)$", repo)) > 0
    ]) == length(var.repositories)
    error_message = "Repositories must be specified in the organization/repository format."
  }
}

# audience
variable "oidc_audience" {
  description = "Expected OIDC audience claim for GitHub->AWS."
  type        = string
  default     = "sts.amazonaws.com"
}

# refs inventory(branch/tag). default: master only
variable "allowed_refs" {
  description = "List of fully-qualified Git refs (e.g., refs/heads/master, refs/tags/v*)."
  type        = list(string)
  default     = ["refs/heads/master"]
}

# special case(PR etc.) override sub
variable "allowed_subs_override" {
  description = "Explicit list of allowed 'sub' claim values. If non-empty, it overrides repositories×allowed_refs."
  type        = list(string)
  default     = []
}

variable "max_session_duration" {
  description = "Maximum session duration in seconds."
  type        = number
  default     = 3600

  validation {
    condition     = var.max_session_duration >= 3600 && var.max_session_duration <= 43200
    error_message = "Maximum session duration must be between 3600 and 43200 seconds."
  }
}

variable "oidc_role_attach_policies" {
  description = "Attach policies to OIDC role."
  type        = list(string)
  default     = []
}

variable "role_name" {
  description = "(Optional, Forces new resource) Friendly name of the role."
  type        = string
  default     = "github-oidc-provider-aws"
}

variable "role_description" {
  description = "(Optional) Description of the role."
  type        = string
  default     = "Role assumed by the GitHub OIDC provider."
}

variable "tags" {
  description = "A mapping of tags to assign to all resources"
  type        = map(string)
  default     = {}
}
