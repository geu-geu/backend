provider "aws" {
  region = var.default_region

  default_tags {
    tags = {
      "Project"              = var.project
      "Managed by Terraform" = true
    }
  }
}
