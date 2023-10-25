resource "aws_ecr_repository" "ecr" {
  for_each             = toset(var.microservices)
  name                 = join("-", [each.key, "repo"])
  image_tag_mutability = var.image_mutability

  encryption_configuration {
    encryption_type = var.encrypt_type
  }
  image_scanning_configuration {
    scan_on_push = false
  }
  tags          = {
    Name        = join("-", [each.key, "ecr"])
    Environment = var.environment
  }  
}

resource "aws_ecs_service" "demo-ecs-service" {
  name            = "demo-ecs-svc"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_taskdef.arn
  desired_count   = 2
  deployment_maximum_percent = 200
  deployment_minimum_healthy_percent = 50
  enable_ecs_managed_tags = false
  health_check_grace_period_seconds = 60
  launch_type = "FARGATE"
  depends_on      = [aws_lb_target_group.alb_ecs_tg, aws_lb_listener.ecs_alb_listener]

  load_balancer {
    target_group_arn = aws_lb_target_group.alb_ecs_tg.arn
    container_name   = "web"
    container_port   = 80
  }

  network_configuration {
    security_groups = [aws_security_group.ecs_sg.id]
    subnets = var.private_subnets
  }
}

# Create the ECS Service task definition. 
# 'nginx' image is being used in the container definition.
# This image is pulled from the docker hub which is the default image repository.
# ECS task execution role and the task role is used which can be attached with additional IAM policies to configure the required permissions.
resource "aws_ecs_task_definition" "ecs_taskdef" {
  for_each = toset(var.microservices)
  family   = join("-", [each.key, "task"])

  container_definitions = jsonencode([
    {
      name      = join("-", [each.key, "container"])
      #image     = "nginx"
      #"image": "101526122836.dkr.ecr.us-east-1.amazonaws.com/pruebas-query:latest",
      image     = ecr
      essential = true
      portMappings = [
        {
          containerPort = 80
          #hostPort      = 80,
          protocol      = "tcp"
        }
      ]
    }
  ])
  # "arn:aws:iam::101526122836:role/ecsTaskExecutionRole"
  execution_role_arn = aws_iam_role.ecs_task_exec_role.arn 
  # "arn:aws:iam::101526122836:role/ecsTaskExecutionRole"
  task_role_arn = aws_iam_role.ecs_task_role.arn 

  runtime_platform {
    operating_system_family = "LINUX"
  }
  
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu       = 256
  memory    = 512
}


    #     "healthCheck": {
    #       "command": ["CMD-SHELL","curl -f http://localhost/pruebas-query/ping || exit 1"],
    #       "interval": 30,
    #       "timeout": 5,
    #       "retries": 3
    #     }
    #   }
    # ],
