terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

module "ecr-repo" {
  source           = "./../modules/ecr"
  ecr_name         = var.microservices
  tags             = var.tags
  image_mutability = var.image_mutability
}

# locals {
#   project_family = "abcjobs"
#   microservices = {
#     "nginx" = {
#     }
#     "frontend" = {
#     }
#     "backend" = {
#     }
#   }
# }
