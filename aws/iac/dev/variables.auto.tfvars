aws_profile = "abcjobs"
aws_region = "us-east-1"

microservices = [
  "abcjobs/candidatos-qry",
  "abcjobs/pruebas-qry",
  "abcjobs/preguntas-qry"
]

tags = {
  "project"     = "abcjobs-misw"
  "team"        = "team-18"
  "environment" = "dev"
}

image_mutability = "MUTABLE"