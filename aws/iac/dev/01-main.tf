terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }
  }
  #required_version = ">= 1.0.11"
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

# module "ecr-repo" {
#   source           = "./../modules/ecr"
#   project          = var.project
#   environment      = var.environment
#   repositories     = var.microservices
#   image_mutability = var.image_mutability
# }
