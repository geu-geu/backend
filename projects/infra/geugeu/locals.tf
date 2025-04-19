locals {
  ecs_task_execution_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    "arn:aws:iam::aws:policy/SecretsManagerReadWrite",
    aws_iam_policy.s3_presign_upload.arn,
  ]
}
