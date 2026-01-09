variable "tags" {
  type        = map(string)
  description = "Tags to apply to resources"
}

variable "resource_prefix" {
  type        = string
  description = "Prefix to apply to resource names"
}

variable "module_name" {
  type        = string
  description = "Name of the module"
}

variable "python_version" {
  type        = string
  description = "Python version"
}
