data "archive_file" "e2e_source" {
  type        = "zip"
  source_dir  = "${path.module}/../../../.."
  output_path = "${path.module}/../../build/e2e-source.zip"
  excludes = [
    "infra",
    ".git",
    ".github",
    ".venv",
    "venv",
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    ".vscode",
    ".idea",
    "*.md",
    ".gitignore",
  ]
}

resource "aws_s3_object" "e2e_source" {
  bucket = aws_s3_bucket.e2e_artifacts.id
  key    = "e2e-source.zip"
  source = data.archive_file.e2e_source.output_path
  etag   = data.archive_file.e2e_source.output_md5

  depends_on = [
    aws_s3_bucket.e2e_artifacts,
    aws_s3_bucket_versioning.e2e_artifacts,
  ]
}
