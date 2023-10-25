variable "aws_profile" {
  # aws configure --profile abcjobs
  description = "profile in ~/.aws/credentials"
  type        = string
}
variable "aws_region" {
  type    = string
}
variable "microservices" {
  description = "The list of ecr names to create"
  type        = list(string)
  default     = null
}
variable "tags" {
  description = "The key-value maps for tagging"
  type        = map(string)
  default     = {}
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
