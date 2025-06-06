resource "aws_route53_zone" "main" {
  name = local.domain
}

resource "aws_route53_record" "root" {
  zone_id = aws_route53_zone.main.zone_id
  name    = local.domain
  type    = "A"

  alias {
    name                   = aws_alb.ecs.dns_name
    zone_id                = aws_alb.ecs.zone_id
    evaluate_target_health = true
  }
}
