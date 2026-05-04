variable "instance_type" {
  default = "t2.micro"
}

variable "db_name" {
  default = "etl_db"
}

variable "db_user" {
  default = "admin"
}

variable "db_password" {
  default = "superdupercontraseniaBD" #si es esa, y por tiempo y pereza va hardcodeada en vez de como secreto
}