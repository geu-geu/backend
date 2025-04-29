resource "aws_db_subnet_group" "postgres" {
  name       = "${local.project}-postgres"
  subnet_ids = [for subnet in aws_subnet.public : subnet.id]
}

resource "aws_db_instance" "postgres" {
  availability_zone               = element(local.availability_zones, 0)
  engine                          = "postgres"
  engine_version                  = "16.3"
  identifier                      = "${local.project}-postgres"
  username                        = "postgres"
  password                        = "gabPab-fudger-catza1"
  instance_class                  = "db.t4g.micro"
  storage_type                    = "gp2"
  allocated_storage               = 20
  vpc_security_group_ids          = [aws_security_group.ecs.id]
  db_subnet_group_name            = aws_db_subnet_group.postgres.name
  ca_cert_identifier              = "rds-ca-rsa2048-g1"
  port                            = 5432
  db_name                         = local.project
  performance_insights_enabled    = false
  parameter_group_name            = "default.postgres16"
  backup_retention_period         = 0
  storage_encrypted               = false
  enabled_cloudwatch_logs_exports = []
  auto_minor_version_upgrade      = false
  deletion_protection             = false
  publicly_accessible             = true
}
