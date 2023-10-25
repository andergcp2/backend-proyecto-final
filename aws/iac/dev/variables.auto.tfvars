aws_profile = "abcjobs"
aws_region  = "us-east-1"

project     = "abcjobs"
team        = "team-18"
environment = "dev"

availability_zones = ["us-east-1a", "us-east-1b"]
public_subnets     = ["10.10.100.0/24", "10.10.101.0/24"]
private_subnets    = ["10.10.0.0/24", "10.10.1.0/24"]

image_mutability = "MUTABLE"

microservices = [
  "candidatos-qry",
  "pruebas-qry",
  "preguntas-qry"
]