resource "aws_ecr_repository" "ecr" {
  for_each             = toset(var.ecr_name)
  name                 = join("-", [each.key, "repo"])
  image_tag_mutability = "MUTABLE"
  #image_tag_mutability = "IMMUTABLE"
  #image_tag_mutability = var.image_mutability

  encryption_configuration {
    encryption_type = var.encrypt_type
  }

  image_scanning_configuration {
    scan_on_push = false
  }

  tags = var.tags
}
