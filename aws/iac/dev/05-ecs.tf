# Create the ECS Cluster and Fargate launch type service in the private subnets
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project}-${var.environment}-cluster"
  tags = {
    Name        = "${var.project}-ecs"
    Environment = var.environment
  }
}

resource "aws_cloudwatch_log_group" "logs" {
  name = "${var.project}-${var.environment}-logs"
  tags = {
    Application = var.project
    Environment = var.environment
  }
}

resource "aws_ecr_repository" "ecr-repos" {
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

# Create the ECS Service task definition. 
# ECS task execution role and the task role is used which can be attached with additional IAM policies to configure the required permissions.
resource "aws_ecs_task_definition" "ecs_taskdef" {
  for_each = toset(var.microservices)
  family   = join("-", [each.key, "task"])
  container_definitions = jsonencode([
    {
      name      = join("-", [each.key, "container"])
      #"image": "101526122836.dkr.ecr.us-east-1.amazonaws.com/pruebas-query:latest",
      # image =  "${var.aws_cuenta}.dkr.ecr.${var.aws_region}.amazonaws.com/${each.key}:latest",
      image = aws_ecr_repository.ecr-repos[each.key].image
      # aws_lb_listener.app_listener_forward[each.key].arn

      essential = true
      # secrets           = local.task_environment_secret_variables
      # log_configuration = local.container_log_configuration
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

resource "aws_ecs_service" "ecs-services" {
  for_each             = toset(var.microservices)
  name                 = join("-", [each.key, "service"])
  cluster         = aws_ecs_cluster.ecs_cluster.id
  # task_definition = join("-", [each.key, "task"])
  task_definition = aws_ecs_task_definition.ecs_taskdef[each.key].arn

  desired_count   = 1
  deployment_maximum_percent = 200
  deployment_minimum_healthy_percent = 50
  enable_ecs_managed_tags = false
  health_check_grace_period_seconds = 60
  launch_type = "FARGATE"
  depends_on      = [aws_lb_target_group.alb_ecs_tg, aws_lb_listener.ecs_alb_listener]

  load_balancer {
    #"targetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:101526122836:targetgroup/candidatos-cmd-tg/f1d9cf46210019e6",
    target_group_arn = aws_lb_target_group.alb_ecs_tg.arn
    container_name   = join("-", [each.key, "container"])
    container_port   = 80
  }

  network_configuration {
    security_groups = [aws_security_group.ecs_security_group.id]
    subnets = var.private_subnets 
    # "assignPublicIp": "ENABLED",
  }
}

# aws ecs register-task-definition --cli-input-json file://aws/scripts/tasks/task-candidatos-cmd.json
# aws elbv2 create-target-group --protocol HTTP --port 80 --vpc-id vpc-038b519bea7fafb30 --target-type ip --name candidatos-cmd-tg --health-check-path /candidates/ping
#    arn:aws:elasticloadbalancing:us-east-1:101526122836:targetgroup/candidatos-cmd-tg/f1d9cf46210019e6
# aws elbv2 create-rule --listener-arn arn:aws:elasticloadbalancing:us-east-1:101526122836:listener/app/abcjobs-qa-lb/fd86a86408ffe63b/a73e50ffb9eaa159 --priority 15 --conditions Field=path-pattern,Values='/candidates/*'  --actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:101526122836:targetgroup/candidatos-cmd-tg/f1d9cf46210019e6
# aws ecs create-service --cluster cluster-abcjobs-qa --cli-input-json file://aws/scripts/services/service-candidatos-cmd.json
