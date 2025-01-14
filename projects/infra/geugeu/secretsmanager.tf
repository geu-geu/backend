resource "aws_secretsmanager_secret" "prod" {
  name = "prod/${var.project}"
}
