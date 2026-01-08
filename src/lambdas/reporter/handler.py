import json
import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import BotoCoreError, ClientError

from shared.utils import create_error_response, create_response

from .models.const import (
    E2E_FINAL_REPORT_TOPIC_ARN,
    EXECUTION_RECORD_LAMBDA_NAME,
    S3_REPORT_BUCKET,
)
from .models.errors import EnvironmentValidationError, ParamsValidationError
from .services.report_creator import ReportCreator
from .services.report_lambda_handler import ReportLambdaHandler
from .services.report_uploader import ReportUploader
from .services.validator import Validator

logger = Logger(service="final_reporter")


def lambda_handler(event: dict, context: LambdaContext) -> Dict[str, Any]:
    logger.info("Starting E2E report generation", event)

    try:
        Validator.validate_environment()
        parameters = Validator.validate_parameters(event)
    except EnvironmentValidationError as e:
        logger.error(str(e))
        return create_error_response(500, str(e))
    except ParamsValidationError as e:
        logger.error(str(e))
        return create_error_response(500, str(e))

    execution_id = parameters.Id
    is_success = parameters.IsSuccess
    error_details = parameters.ErrorDetails

    logger.info(f"Processing execution report: {execution_id}")

    # Retrieve execution record
    lambda_client = boto3.client("lambda")
    record_handler_lambda = os.getenv(EXECUTION_RECORD_LAMBDA_NAME)
    bucket_name = os.getenv(S3_REPORT_BUCKET)

    try:
        logger.info(f"Invoking execution record lambda: {record_handler_lambda}")
        report_lambda_handler = ReportLambdaHandler(
            execution_id=execution_id,
            function_name=record_handler_lambda,
            lambda_client=lambda_client,
        )
        record = report_lambda_handler.main()
        logger.info("Successfully retrieved execution record")
    except (BotoCoreError, ClientError) as e:
        logger.error(f"AWS service error retrieving execution record: {str(e)}")
        return create_error_response(
            500, f"Failed to retrieve execution record: {str(e)}"
        )
    except Exception as error:
        logger.exception("Unexpected error retrieving execution record")
        return create_error_response(
            500, f"Failed to retrieve execution record: {str(error)}"
        )

    # Create report
    try:
        logger.info("Creating report from execution record")
        report_creator = ReportCreator(
            {
                **record,
                "Status": "success" if is_success else "failed",
                "failure_reason": error_details,
            }
        )
        html_report = report_creator.to_html()
        logger.info("Successfully generated HTML report")
    except Exception as error:
        logger.exception("Error generating HTML report")
        return create_error_response(500, f"Failed to generate report: {str(error)}")

    # Upload report to S3
    s3_client = boto3.client("s3")
    report_uploader = ReportUploader(s3_client=s3_client, bucket_name=bucket_name)

    try:
        logger.info(f"Uploading report to S3 bucket: {bucket_name}")
        file_name = f"{execution_id}-report"
        presigned_url = report_uploader.main(
            html_report=html_report, file_name=file_name
        )
        logger.info("Successfully uploaded report to S3")
    except (BotoCoreError, ClientError) as e:
        logger.error(f"AWS service error uploading report: {str(e)}")
        return create_error_response(500, f"Failed to upload report: {str(e)}")
    except Exception as error:
        logger.exception("Unexpected error uploading report")
        return create_error_response(500, f"Failed to upload report: {str(error)}")

    # Publish report to SNS
    try:
        logger.info("Creating SNS message from report")
        sns_message = report_creator.to_json(report_url=presigned_url)
    except Exception as error:
        logger.exception("Error creating SNS message")
        return create_error_response(500, f"Failed to create SNS message: {str(error)}")

    sns_client = boto3.client("sns")
    topic_arn = os.getenv(E2E_FINAL_REPORT_TOPIC_ARN)

    try:
        final_status = record.get("Status", "unknown")
        logger.info(f"Publishing report to SNS with status: {final_status}")

        sns_client.publish(
            TopicArn=topic_arn,
            Subject=f"E2E Final Report - {final_status}",
            Message=json.dumps(sns_message, indent=2),
            MessageAttributes={
                "status": {"DataType": "String", "StringValue": final_status},
                "report_id": {
                    "DataType": "String",
                    "StringValue": execution_id,
                },
            },
        )

        logger.info(
            f"Successfully published E2E report to SNS for execution: {execution_id}"
        )

        return create_response(
            status_code=200,
            body={
                "message": "Successfully published E2E final report status to SNS",
                "execution_id": execution_id,
                "status": final_status,
            },
        )

    except (BotoCoreError, ClientError) as e:
        logger.error(f"AWS service error publishing to SNS: {str(e)}")
        return create_error_response(500, f"Failed to publish to SNS: {str(e)}")
    except Exception as e:
        logger.exception("Unexpected error publishing to SNS")
        return create_error_response(500, f"Failed to publish to SNS: {str(e)}")
