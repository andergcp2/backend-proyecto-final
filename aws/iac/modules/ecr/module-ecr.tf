resource "aws_ecr_repository" "ecr" {
  for_each             = toset(var.repositories)
  name                 = join("-", [each.key, "repo"])
  image_tag_mutability = var.image_mutability

  encryption_configuration {
    encryption_type = var.encrypt_type
  }

  image_scanning_configuration {
    scan_on_push = false
  }

  tags             = {
    Name        = join("-", [each.key, "ecr"])
    Environment = var.environment
  }  
}
