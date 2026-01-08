locals {
  test_execution_record_handler_function_name = "execution-record-handler"
  merged_tags                                 = merge(var.tags, { Module = var.module_name })
  table_name                                  = "${var.resource_prefix}-test-execution-records"
  hash_key_name                               = "Id"
  secondary_index_name                        = "Status-CreatedAt-Index"
}
