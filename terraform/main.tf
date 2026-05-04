# iniciar instancia ec2

resource "aws_instance" "flask-api-devops" {
  ami           = "ami-0c55b159cbfafe1f0" 
  instance_type = var.instance_type

  tags = {
    Name = "flask-api-devops"
  }
}

# iniciar instancia s3
resource "aws_s3_bucket" "data_bucket" {
  bucket = "sapsimdata-demo-terraform"

  tags = {
    Name = "sapsimdata"
  }
}

# iniciar instancia de rds
resource "aws_db_instance" "devopsbinstance" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t3.micro"
  db_name              = var.db_name
  username             = var.db_user
  password             = var.db_password
  skip_final_snapshot  = true

  publicly_accessible = true
}

#crear security group y policies del ec2 para api
resource "aws_security_group" "api_sg" {
  name = "api-security-group"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# crear rol iam para ec2 con seguimiento en cloud formation (logs de monitoreo)
resource "aws_iam_role" "ec2_role" {
  name = "ec2-cloudwatch-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

#attachear politicas al rol
resource "aws_iam_role_policy_attachment" "cw_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}