resource "aws_acm_certificate" "main" {
  domain_name       = local.domain
  validation_method = "DNS"

  subject_alternative_names = ["*.${local.domain}"]
}
