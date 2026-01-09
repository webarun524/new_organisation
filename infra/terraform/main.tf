provider "aws" {
  region = var.aws_region
}

module "lambda_layer" {
  source          = "./modules/lambda_layer"
  tags            = local.tags
  resource_prefix = local.resource_prefix
  python_version  = local.python_version
  module_name     = "lambda-layer"

}

module "test_execution_db" {
  source           = "./modules/test_execution_db"
  tags             = local.tags
  resource_prefix  = local.resource_prefix
  module_name      = "test-execution-db"
  aws_region       = var.aws_region
  lambda_layer_arn = module.lambda_layer.layer_version_arn
  python_version   = local.python_version
}

module "approval_handler" {
  source               = "./modules/approval_handler"
  tags                 = local.tags
  resource_prefix      = local.resource_prefix
  lambda_timeout       = var.approval_lambda_timeout
  lambda_memory_size   = var.lambda_memory_size
  backplane_account_id = var.backplane_account_id
  aws_region           = var.aws_region
  module_name          = "approval-handler"
  lambda_layer_arn     = module.lambda_layer.layer_version_arn
  python_version       = local.python_version
  test_admin_email     = module.config_composer.admin_username_parameter_value
}

module "commit_collector" {
  source             = "./modules/commit_collector"
  tags               = local.tags
  resource_prefix    = local.resource_prefix
  lambda_timeout     = var.commit_collector_lambda_timeout
  lambda_memory_size = var.lambda_memory_size
  aws_region         = var.aws_region
  module_name        = "commit-collector"
  lambda_layer_arn   = module.lambda_layer.layer_version_arn
  python_version     = local.python_version
  bitbucket_token    = var.bitbucket_token
}

module "environment_setup" {
  source                     = "./modules/environment_setup"
  tags                       = local.tags
  resource_prefix            = local.resource_prefix
  setup_lambda_timeout       = var.setup_trigger_lambda_timeout
  setup_lambda_memory_size   = var.lambda_memory_size
  checker_lambda_timeout     = var.setup_trigger_lambda_timeout
  checker_lambda_memory_size = var.lambda_memory_size
  aws_region                 = var.aws_region
  module_name                = "environment_setup"
  lambda_layer_arn           = module.lambda_layer.layer_version_arn
  bitbucket_token            = var.bitbucket_token
  python_version             = local.python_version
}

module "test_execution_orchestrator" {
  source                       = "./modules/test_execution_orchestrator"
  tags                         = local.tags
  resource_prefix              = local.resource_prefix
  module_name                  = "test-execution-orchestrator"
  setup_lambda_name            = module.environment_setup.setup_lambda_function_name
  setup_lambda_arn             = module.environment_setup.setup_lambda_function_arn
  checker_lambda_name          = module.environment_setup.deployment_checker_lambda_function_name
  checker_lambda_arn           = module.environment_setup.deployment_checker_lambda_function_arn
  commit_collector_lambda_arn  = module.commit_collector.lambda_function_arn
  commit_collector_lambda_name = module.commit_collector.lambda_function_name
  config_composer_lambda_arn   = module.config_composer.lambda_function_arn
  config_composer_lambda_name  = module.config_composer.lambda_function_name
  password_rotator_lambda_arn  = module.config_composer.password_rotator_function_arn
  password_rotator_lambda_name = module.config_composer.password_rotator_function_name
  reporter_lambda_name         = module.test_reports.reporter_lambda_function_name
  reporter_lambda_arn          = module.test_reports.reporter_lambda_function_arn
  deployment_environment_code  = var.deployment_environment_code
  e2e_tests_project_arn        = module.e2e_tests.project_arn
  e2e_tests_project_name       = module.e2e_tests.project_name
  e2e_tests_role_arn           = module.e2e_tests.role_arn
  region                       = var.aws_region
  execution_record_lambda_name = module.test_execution_db.terh_lambda_function_name
  execution_record_lambda_arn  = module.test_execution_db.terh_lambda_function_arn
  lambda_timeout               = var.approval_lambda_timeout
  python_version               = local.python_version
  lambda_memory_size           = var.lambda_memory_size
  lambda_layer_arn             = module.lambda_layer.layer_version_arn
  dde_lambda_name              = module.e2e_tests.dde_function_name
  dde_lambda_arn               = module.e2e_tests.dde_function_arn
}

module "test_reports" {
  source                       = "./modules/test_reports"
  resource_prefix              = local.resource_prefix
  tags                         = local.tags
  module_name                  = "test-reports"
  aws_region                   = var.aws_region
  lambda_layer_arn             = module.lambda_layer.layer_version_arn
  lambda_timeout               = var.approval_lambda_timeout
  python_version               = local.python_version
  lambda_memory_size           = var.lambda_memory_size
  execution_record_lambda_name = module.test_execution_db.terh_lambda_function_name
  execution_record_lambda_arn  = module.test_execution_db.terh_lambda_function_arn
}

module "config_composer" {
  source                      = "./modules/config_composer"
  resource_prefix             = local.resource_prefix
  tags                        = local.tags
  module_name                 = "config-composer"
  aws_region                  = var.aws_region
  lambda_layer_arn            = module.lambda_layer.layer_version_arn
  lambda_timeout              = var.approval_lambda_timeout
  python_version              = local.python_version
  lambda_memory_size          = var.lambda_memory_size
  service_name                = var.service_name
  deployment_environment_code = var.deployment_environment_code
}

module "e2e_tests" {
  source                      = "./modules/codebuild"
  project_name                = "e2e-tests"
  buildspec                   = var.e2e_tests_buildspec
  report_bucket_arn           = module.test_reports.report_bucket_arn
  execution_record_lambda_arn = module.test_execution_db.terh_lambda_function_arn

  resource_prefix = local.resource_prefix
  aws_region      = var.aws_region
  module_name     = "e2e-tests"
  tags            = local.tags

  environment_variables = [
    {
      name  = "REPORTS_S3_BUCKET"
      value = module.test_reports.bucket_name
      type  = "PLAINTEXT"
    },
    {
      name  = "EXECUTION_RECORD_LAMBDA_NAME"
      value = module.test_execution_db.terh_lambda_function_name
      type  = "PLAINTEXT"
    }
  ]

  python_version     = local.python_version
  lambda_timeout     = var.approval_lambda_timeout
  lambda_memory_size = var.lambda_memory_size
  lambda_layer_arn   = module.lambda_layer.layer_version_arn
  report_bucket_name = module.test_reports.bucket_name
}

module "bitbucket_trigger_integration" {
  source                      = "./modules/bitbucket_permissions"
  sfn_orchestrator_arn        = module.test_execution_orchestrator.orchestrator_arn
  bitbucket_audience          = var.bitbucket_audience
  bitbucket_thumbprint        = var.bitbucket_thumbprint
  bitbucket_subjects          = var.bitbucket_subjects
  bitbucket_oidc_provider_url = "https://api.bitbucket.org/2.0/workspaces/47lining/pipelines-config/identity/oidc"
  resource_prefix             = local.resource_prefix
  tags                        = local.tags
  module_name                 = "bitbucket-permissions"
}
