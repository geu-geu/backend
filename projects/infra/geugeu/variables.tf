variable "project" {
  type = string
}

variable "account_id" {
  type = string
}

variable "default_region" {
  type = string
}

variable "availability_zones" {
  type = list(string)
}

variable "cidr_public" {
  default = {
    "0" = "0"
    "1" = "16"
    "2" = "32"
  }
}

variable "cidr_private" {
  default = {
    "0" = "128"
    "1" = "144"
    "2" = "160"
  }
}

variable "ecs_task_execution_policy_arns" {
  type = list(string)
  default = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
  ]
}

variable "ecs_task_policy_arns" {
  type    = list(string)
  default = []
}

variable "domain" {
  type = string
}

variable "secrets" {
  type = list(string)
  default = [
    "SECRET_KEY",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
  ]
}
