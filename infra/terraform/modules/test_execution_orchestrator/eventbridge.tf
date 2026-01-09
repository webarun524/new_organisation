resource "aws_cloudwatch_event_connection" "data_console" {
  name               = "data-console-connection"
  description        = "To permit SFN to call data portal to check deployment status"
  authorization_type = "API_KEY"

  auth_parameters {
    api_key {
      key   = "Authorization"
      value = "none"
    }
  }
}
