# Create the internal application load balancer (ALB) in the private subnets.
# --ip-address-type ipv4
resource "aws_lb" "ecs_alb" {
  load_balancer_type = "application"
  internal = true
  subnets = var.private_subnets
  security_groups = [aws_security_group.lb_security_group.id]
}

# Create the ALB target group for ECS.
# --target-type alb 
resource "aws_lb_target_group" "alb_ecs_tg" {
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.this.id
}

# Create the ALB listener with the target group.
resource "aws_lb_listener" "ecs_alb_listener" {
  load_balancer_arn = aws_lb.ecs_alb.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.alb_ecs_tg.arn
  }
}
