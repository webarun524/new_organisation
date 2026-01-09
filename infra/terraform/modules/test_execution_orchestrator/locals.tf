locals {
  template_vars = {
    SetupLambdaName                   = var.setup_lambda_name,
    DeploymentCheckerLambdaName       = var.checker_lambda_arn,
    CommitCollectorLambdaName         = var.commit_collector_lambda_name,
    ReporterLambdaName                = var.reporter_lambda_name,
    DeploymentEnvironment             = var.deployment_environment_code,
    DataPortalConnectionArn           = resource.aws_cloudwatch_event_connection.data_console.arn,
    ConfigComposerLambdaName          = var.config_composer_lambda_name,
    PasswordRotatorLambdaName         = var.password_rotator_lambda_name,
    E2eTestsProjectArn                = var.e2e_tests_project_arn,
    E2eTestsProjectName               = var.e2e_tests_project_name,
    Region                            = var.region,
    ExecutionRecordLambdaName         = var.execution_record_lambda_name,
    SfnValidatorFunctionName          = module.execution_params_validator_function.function_name,
    DeploymentDataExtractorLambdaName = var.dde_lambda_name
  }

  # Load all phase files
  validation_states        = jsondecode(templatefile("${path.module}/definitions/01_validation.json.tpl", local.template_vars))
  initialization_states    = jsondecode(templatefile("${path.module}/definitions/02_initialization.json.tpl", local.template_vars))
  environment_setup_states = jsondecode(templatefile("${path.module}/definitions/03_environment_setup.json.tpl", local.template_vars))
  commit_collection_states = jsondecode(templatefile("${path.module}/definitions/04_commit_collection.json.tpl", local.template_vars))
  operations_portal_states = jsondecode(templatefile("${path.module}/definitions/05_operations_portal.json.tpl", local.template_vars))
  data_portal_states       = jsondecode(templatefile("${path.module}/definitions/06_data_portal.json.tpl", local.template_vars))
  teardown_states          = jsondecode(templatefile("${path.module}/definitions/07_teardown.json.tpl", local.template_vars))
  reporting_states         = jsondecode(templatefile("${path.module}/definitions/08_reporting.json.tpl", local.template_vars))

  # Merge all phases
  e2e_main_definition = {
    States = merge(
      local.validation_states,
      local.initialization_states,
      local.environment_setup_states,
      local.commit_collection_states,
      local.operations_portal_states,
      local.data_portal_states,
      local.teardown_states,
      local.reporting_states
    )
  }

  merged_tags   = merge(var.tags, { Module = var.module_name })
  function_name = "execution-params-validator"
}
