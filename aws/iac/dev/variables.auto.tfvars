aws_profile = "abcjobs"
aws_region = "us-east-1"

microservices = [
  "candidatos-qry",
  "pruebas-qry",
  "preguntas-qry"
]

tags = {
  "project"     = "abcjobs-misw"
  "team"        = "team-18"
  "environment" = "dev"
}

image_mutability = "MUTABLE"