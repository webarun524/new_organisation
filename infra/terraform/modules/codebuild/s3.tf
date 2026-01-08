resource "aws_s3_bucket" "e2e_artifacts" {
  bucket = "${var.resource_prefix}-${var.project_name}-artifacts"
  tags   = local.merged_tags
}

resource "aws_s3_bucket_versioning" "e2e_artifacts" {
  bucket = aws_s3_bucket.e2e_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "e2e_artifacts" {
  bucket = aws_s3_bucket.e2e_artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "e2e_artifacts" {
  bucket = aws_s3_bucket.e2e_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
