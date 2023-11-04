variable "services" {
  description = "The list of service to create"
  type        = list(string)
  default     = null
}

variable "project" {
  type    = string
}
variable "environment" {
  type    = string
}

variable "public_subnets" {
  type        = list(string)
}
variable "private_subnets" {
  type        = list(string)
}
variable "availability_zones" {
  type        = list(string)
}