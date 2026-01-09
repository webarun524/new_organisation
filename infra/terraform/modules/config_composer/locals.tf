locals {
  # Common
  function_name           = "config-composer"
  merged_tags             = merge(var.tags, { Module = var.module_name })
  ssm_format_service_name = "/${replace(var.service_name, "-", "/")}"

  # OP credentials
  e2e_test_account_admin_name       = "e2e_test_org@dataops.47lining.com"
  test_inbox_address_parameter_name = "${local.ssm_format_service_name}/test_inbox_address"
  test_inbox_password_secret_name   = "${local.ssm_format_service_name}/test_inbox_password"

  # OP mailbox
  test_inbox_address                   = "https://webmail.mail.${var.aws_region}.awsapps.com/workmail/?organization=osdu-47lining"
  test_admin_user_name_parameter_name  = "${local.ssm_format_service_name}/test_admin_user_name"
  test_admin_user_password_secret_name = "${local.ssm_format_service_name}/test_admin_user_password"

  # OP Urls
  operations_portal_url_template = "https://portal.mb-<env>.${var.aws_region}.prod.saas.dataops.47lining.com"
  operations_portal_urls = {
    proto         = "https://portal.mb-proto.${var.aws_region}.dev.saas.dataops.47lining.com"
    proto2        = "https://portal.mb-proto2.${var.aws_region}.dev.saas.dataops.47lining.com"
    proto3        = "https://portal.mb-proto3.${var.aws_region}.dev.saas.dataops.47lining.com"
    dev           = "https://portal.mb.${var.aws_region}.dev.saas.dataops.47lining.com"
    qa            = "https://portal.mb-qa.${var.aws_region}.test.saas.dataops.47lining.com"
    preprod       = "https://portal.mb.${var.aws_region}.test.saas.dataops.47lining.com"
    utility       = "https://portal.mb-utility.${var.aws_region}.prod.saas.dataops.47lining.com"
    edi-qa        = "https://portal.enterprise-mb.awsenergy.47lining.com"
    customer-prod = "https://portal.mb.${var.aws_region}.prod.saas.dataops.47lining.com"
  }
  operations_portal_url = lookup(
    local.operations_portal_urls,
    var.deployment_environment_code,
    replace(local.operations_portal_url_template, "<env>", var.deployment_environment_code)
  )
  operations_portal_url_parameter_name = "${local.ssm_format_service_name}/operations_portal_url"

  # BitBucket
  deployment_to_bb_code = tomap({
    proto         = "vproto"
    proto2        = "vproto2"
    proto3        = "vproto3"
    dev           = "vdev"
    qa            = "vqa"
    preprod       = "vpreprod"
    utility       = "vutil"
    edi-qa        = "vediqa"
    customer-prod = "release"
  })
  bb_env_code = lookup(
    local.deployment_to_bb_code,
    var.deployment_environment_code,
    "v${var.deployment_environment_code}"
  )
  bb_env_code_parameter_name = "${local.ssm_format_service_name}/bb_env_code"
  bb_code_to_name = tomap({
    vproto   = "Prototype"
    vproto2  = "Proto2"
    vproto3  = "Proto3"
    vdev     = "Dev"
    vqa      = "QA"
    vediqa   = "EDIEnterpriseQA"
    vpreprod = "Preprod"
    vutil    = "Utility"
  })
  bb_env_name = lookup(
    local.bb_code_to_name,
    local.bb_env_code,
    title(var.deployment_environment_code)
  )
  bb_env_name_parameter_name = "${local.ssm_format_service_name}/bb_env_name"

  # DP password
  dp_password_rotator_function_name      = "dp-password-rotator"
  dp_temp_password_secret_name           = "/dataops/workload/subscriber-temporary-password"
  dp_password_secret_name                = "${local.ssm_format_service_name}/data-portal-password"
  dp_cognito_user_pool_id_parameter_name = "/osdu/cognito/osdu/user-pool/id"
}
