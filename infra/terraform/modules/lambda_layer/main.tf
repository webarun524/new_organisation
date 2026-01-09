# Lambda Layer for shared Python modules and dependencies

resource "null_resource" "build_lambda_layer" {
  triggers = {
    # Rebuild when shared directory contents change
    shared_dir_hash = sha256(join("", [
      for f in fileset("${path.module}/../../../../src/shared", "**") :
      filesha256("${path.module}/../../../../src/shared/${f}")
    ]))
    # Rebuild when requirements change
    requirements_hash = filesha256("${path.module}/../../../../src/shared/requirements.txt")
    # Rebuild when build script changes
    build_script_hash = filesha256("${path.module}/build_layer.sh")
  }

  provisioner "local-exec" {
    command     = "./build_layer.sh"
    working_dir = path.module
  }
}

resource "aws_lambda_layer_version" "shared_layer" {
  filename            = "${path.module}/../../build/layer_build/lambda_layer.zip"
  layer_name          = "${var.resource_prefix}-shared-layer"
  description         = "Shared Python modules and dependencies for ${var.resource_prefix}"
  compatible_runtimes = ["python${var.python_version}"]
  source_code_hash    = null_resource.build_lambda_layer.id
  depends_on          = [null_resource.build_lambda_layer]

  lifecycle {
    create_before_destroy = true
  }
}

data "aws_lambda_layer_version" "existing_layer" {
  layer_name = "${var.resource_prefix}-shared-layer"
  depends_on = [aws_lambda_layer_version.shared_layer]
}
