# Load balancer security group. CIDR and port ingress can be changed as required.
resource "aws_security_group" "lb_sg" {
  description = "LoadBalancer Security Group"
  vpc_id = aws_vpc.this.id
  ingress {
    description      = "Allow from anyone on port 80"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

# ECS cluster security group.
resource "aws_security_group" "ecs_sg" {
  description = "ECS Security Group"
  vpc_id = aws_vpc.this.id
  egress {
    description      = "Allow all outbound traffic by default"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "sg_ingress_rule_all_to_lb" {
  type	= "ingress"
  description = "Allow from anyone on port 80"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  security_group_id = aws_security_group.lb_sg.id
}

# Load balancer security group egress rule to ECS cluster security group.
resource "aws_security_group_rule" "sg_egress_rule_lb_to_ecs_cluster" {
  type	= "egress"
  description = "Target group egress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  security_group_id = aws_security_group.lb_sg.id
  source_security_group_id = aws_security_group.ecs_sg.id
}

# ECS cluster security group ingress from the load balancer.
resource "aws_security_group_rule" "sg_ingress_rule_ecs_cluster_from_lb" {
  type	= "ingress"
  description = "Ingress from Load Balancer"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  security_group_id = aws_security_group.ecs_sg.id
  source_security_group_id = aws_security_group.lb_sg.id
}
