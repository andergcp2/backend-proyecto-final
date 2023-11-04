variable "aws_profile" {
  # aws configure --profile abcjobs
  description = "profile in ~/.aws/credentials"
  type        = string
}
variable "aws_region" {
  type = string
}
variable "aws_cuenta" {
  type = string
}
variable "project" {
  type = string
}
variable "team" {
  type = string
}
variable "environment" {
  type = string
}

variable "public_subnets" {
  description = "List of public subnets"
  type        = list(string)
}

variable "private_subnets" {
  description = "List of private subnets"
  type        = list(string)
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "image_mutability" {
  description = "Provide image mutability"
  type        = string
  default     = "MUTABLE"
}

variable "encrypt_type" {
  description = "Provide type of encryption here"
  type        = string
  default     = "AES256"
  #default     = "KMS"
}

variable "microservices" {
  description = "The list of ecr names to create"
  type        = list(string)
  default     = null
}