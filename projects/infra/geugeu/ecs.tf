resource "aws_ecs_cluster" "main" {
  name = "${var.project}-ecs-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

resource "aws_cloudwatch_log_group" "ecs" {
  name = "/ecs/${var.project}"
}

resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project}-ecs-task-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy_attachment" {
  role       = aws_iam_role.ecs_task_execution.name
  count      = length(var.ecs_task_execution_policy_arns)
  policy_arn = var.ecs_task_execution_policy_arns[count.index]
}

resource "aws_iam_role" "ecs_task" {
  name = "${var.project}-ecs-task"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_policy_attachment" {
  role       = aws_iam_role.ecs_task.name
  count      = length(var.ecs_task_policy_arns)
  policy_arn = var.ecs_task_policy_arns[count.index]
}

resource "aws_ecs_task_definition" "main" {
  family                   = "${var.project}-ecs-task-definition"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  container_definitions = jsonencode([
    {
      name      = "${var.project}"
      image     = "${aws_ecr_repository.main.repository_url}:latest"
      essential = true
      portMappings = [
        {
          protocol      = "tcp"
          containerPort = 8000
          appProtocol   = "http"
          hostPort      = 8000
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "${aws_cloudwatch_log_group.ecs.name}"
          awslogs-region        = "${var.default_region}"
          awslogs-stream-prefix = "ecs"
          mode                  = "non-blocking"
          max-buffer-size       = "1m"
        }
      }

      secrets = [
        for key in var.secrets : {
          name      = key
          valueFrom = "${aws_secretsmanager_secret.main.arn}:${key}::"
        }
      ]
    }
  ])

  runtime_platform {
    cpu_architecture = "X86_64"
  }
}

resource "aws_security_group" "ecs" {
  name   = "${var.project}-ecs"
  vpc_id = aws_vpc.main.id

  // FIXME: RULE IS TOO FREE!

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  tags = {
    Name = "${var.project}-ecs"
  }
}

resource "aws_security_group" "alb" {
  name   = "${var.project}-alb"
  vpc_id = aws_vpc.main.id

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  tags = {
    Name = "${var.project}-alb"
  }
}

resource "aws_alb" "ecs" {
  name               = "${var.project}-ecs"
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [for subnet in aws_subnet.public : subnet.id]
}

resource "aws_alb_target_group" "ecs" {
  name        = "${var.project}-ecs-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path = "/docs"
  }
}

resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_alb.ecs.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = 443
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_alb_listener" "https" {
  load_balancer_arn = aws_alb.ecs.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    target_group_arn = aws_alb_target_group.ecs.arn
    type             = "forward"
  }
}

resource "aws_ecs_service" "main" {
  name            = var.project
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  launch_type     = "FARGATE"
  propagate_tags  = "SERVICE"
  desired_count   = 1

  network_configuration {
    subnets          = [for subnet in aws_subnet.public : subnet.id]
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.ecs.arn
    container_name   = var.project
    container_port   = 8000
  }
}
