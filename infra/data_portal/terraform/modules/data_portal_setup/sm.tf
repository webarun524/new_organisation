resource "random_password" "dp_password" {
  length           = 12
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret" "dp_password" {
  name = local.dp_password_secret_name
}

resource "aws_secretsmanager_secret_version" "dp_password" {
  secret_id     = aws_secretsmanager_secret.dp_password.id
  secret_string = random_password.dp_password.result
}
