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

resource "aws_instance" "tf_test_server" {
  ami           = "ami-06d2149e11dd4bec4"
  instance_type = "t2.micro"

  tags = {
    Name = "KafkaTesting"
  }
}