provider "aws" {
  region     = "eu-west-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_use_path_style           = true

  endpoints {
    s3     = "http://localhost:4566"
    lambda = "http://localhost:4566"
    iam    = "http://localhost:4566"
  }
}

locals {
  python_version = "python3.11"
}

resource "aws_s3_bucket" "default" {
  bucket        = "northcoders"
  force_destroy = true
}

resource "null_resource" "build_layer" {
  triggers = {
    source_hash = filesha256("${path.module}/../../../src/obfuscator/main.py")
  }

  provisioner "local-exec" {
    command = <<EOT
      rm -rf build/layer && mkdir -p build/layer/python
      cp -r ../../../src/obfuscator build/layer/python/
    EOT
  }
}

data "archive_file" "layer_code" {
  type        = "zip"
  source_dir  = "${path.module}/build/layer"
  output_path = "${path.module}/layer.zip"
  excludes    = ["**/__pycache__/*"]

  depends_on = [null_resource.build_layer]
}

data "archive_file" "app_code" {
  type        = "zip"
  source_dir  = "${path.module}/../../../example"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_layer_version" "default" {
  layer_name          = "obfuscator"
  compatible_runtimes = [local.python_version]
  filename            = data.archive_file.layer_code.output_path
  source_code_hash    = data.archive_file.layer_code.output_base64sha256
}
