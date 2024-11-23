terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_s3_bucket" "movie-list-kafka-monolith" {
  bucket = "movie-list-kafka-monolith"
}

resource "aws_security_group" "ssh_access" {
  name = "kafka-ec2-sg"
  description = "adds appropriate ssh permission"
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port = 22
    to_port = 22
    protocol = "tcp"
  }
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port = 0
    to_port = 0
    protocol = "-1"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "glue_role" {
  name = "glue_job_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        },
    ]
})
}

resource "aws_instance" "stream_server" {
  ami           = "ami-06d2149e11dd4bec4"
  instance_type = "t2.micro"
  tags = {
    Name = var.instance_name
  }
  user_data = file("scripts/start_script.sh")
  security_groups = [aws_security_group.ssh_access.name]
  key_name = "KafkaKeyPair"
}
