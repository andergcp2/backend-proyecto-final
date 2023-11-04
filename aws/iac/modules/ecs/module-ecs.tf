resource "aws_ecs_cluster" "this" {
  name = "${var.project}-${var.environment}-cluster"
  tags = {
    Name        = "${var.project}-ecs"
    Environment = var.environment
  }
}

resource "aws_cloudwatch_log_group" "this" {
  name = "${var.project}-${var.environment}-logs"

  tags = {
    Application = var.project
    Environment = var.environment
  }
}

# resource "aws_ecr_repository" "cluster" {
#   for_each             = toset(var.services)
#   name                 = join("-", [each.key, "repo"])
# }

