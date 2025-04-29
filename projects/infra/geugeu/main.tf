provider "aws" {
  region = local.default_region

  default_tags {
    tags = {
      "Project"              = local.project
      "Managed by Terraform" = true
    }
  }
}
