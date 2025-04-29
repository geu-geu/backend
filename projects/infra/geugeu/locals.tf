locals {
  project            = "geugeu"
  account_id         = "864899837939"
  default_region     = "ap-northeast-2"
  availability_zones = ["ap-northeast-2a", "ap-northeast-2b"]
  domain             = "geugeu.com"
  cidr_public = {
    "0" = "0"
    "1" = "16"
    "2" = "32"
  }
  cidr_private = {
    "0" = "128"
    "1" = "144"
    "2" = "160"
  }
  ecs_task_execution_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
  ]
  ecs_task_policy_arns = []
}
