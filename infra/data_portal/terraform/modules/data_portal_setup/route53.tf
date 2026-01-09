resource "aws_route53_zone" "public_hz" {
  name    = var.domain_name
  comment = "Public hosted zone for automated test suite"
}
