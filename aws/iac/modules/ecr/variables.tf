variable "repositories" {
  description = "The list of ecr names to create"
  type        = list(string)
  default     = null
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

variable "project" {
  type    = string
}

variable "environment" {
  type    = string
}