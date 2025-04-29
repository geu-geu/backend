resource "aws_secretsmanager_secret" "main" {
  name = local.project
}
