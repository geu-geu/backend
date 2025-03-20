resource "aws_secretsmanager_secret" "main" {
  name = var.project
}
