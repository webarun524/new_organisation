resource "aws_codebuild_project" "this" {
  name         = "${var.resource_prefix}-${var.project_name}"
  service_role = aws_iam_role.codebuild_role.arn
  tags         = local.merged_tags

  artifacts {
    type           = "S3"
    location       = var.artifacts_bucket != null ? var.artifacts_bucket : aws_s3_bucket.e2e_artifacts.bucket
    path           = "/artifacts"
    namespace_type = "BUILD_ID"
    packaging      = "ZIP"
  }

  environment {
    compute_type                = var.build_compute_type
    image                       = var.build_image
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"

    dynamic "environment_variable" {
      for_each = var.environment_variables
      content {
        name  = environment_variable.value.name
        value = environment_variable.value.value
        type  = environment_variable.value.type
      }
    }
  }

  source {
    type      = "S3"
    location  = "${aws_s3_bucket.e2e_artifacts.bucket}/e2e-source.zip"
    buildspec = var.buildspec != null ? file("${path.root}/../../${var.buildspec}") : null
  }

  depends_on = [aws_s3_object.e2e_source]
}
