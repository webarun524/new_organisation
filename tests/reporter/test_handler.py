import json
import os
from unittest.mock import MagicMock, patch

from botocore.exceptions import ClientError

os.environ.setdefault(
    "E2E_FINAL_REPORT_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789:test-topic"
)
os.environ.setdefault("EXECUTION_RECORD_LAMBDA_NAME", "test-lambda")
os.environ.setdefault("S3_REPORT_BUCKET", "test-bucket")
os.environ.setdefault("AWS_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

from src.lambdas.reporter.handler import lambda_handler
from src.lambdas.reporter.models.errors import (
    EnvironmentValidationError,
    ParamsValidationError,
)


def _create_mock_context():
    """Create a mock Lambda context."""
    return MagicMock()


def _create_valid_event():
    """Create a valid event for the handler."""
    return {
        "Id": "test-execution-id-123",
        "IsSuccess": True,
        "ErrorDetails": None,
    }


def _create_mock_execution_record():
    """Create a mock execution record."""
    return {
        "Id": "test-execution-id-123",
        "Status": "deployedServices",
        "WorkloadVersion": "5.0.1",
        "DataPortalUrl": "https://data-portal.example.com",
        "DeploymentId": "test-deployment-id",
        "SubscriptionTestReportUrl": "https://reports.example.com/subscription",
        "VerificationTestReportUrl": "https://reports.example.com/verification",
        "TeardownTestReportUrl": "https://reports.example.com/teardown",
        "FailureReason": None,
        "CreatedAt": "2025-12-19T12:00:00+00:00",
        "UpdatedAt": "2025-12-19T13:00:00+00:00",
        "DeployedServices": {
            "dataops-mb-vpc": "hash1",
            "dataops-mb-metering-service": "hash2",
        },
    }


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportUploader")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_happy_path_success(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_report_uploader,
    mock_boto3,
):
    """Test successful report generation when execution succeeds."""
    event = _create_valid_event()
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.return_value.to_html.return_value = (
        "<html>success report</html>"
    )
    mock_report_creator.return_value.to_json.return_value = {"message": "success"}
    mock_report_uploader.return_value.main.return_value = (
        "https://s3.example.com/report.html"
    )

    mock_sns_client = MagicMock()
    mock_boto3.client.return_value = mock_sns_client

    response = lambda_handler(event, context)

    assert response["statusCode"] == 200
    body = (
        json.loads(response["body"])
        if isinstance(response["body"], str)
        else response["body"]
    )
    assert "message" in body
    assert event["Id"] in str(body)


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportUploader")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_happy_path_failure(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_report_uploader,
    mock_boto3,
):
    """Test successful report generation when execution fails."""
    event = {
        "Id": "test-execution-id-123",
        "IsSuccess": False,
        "ErrorDetails": "Test deployment failed",
    }
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()
    mock_record["Status"] = "failed"

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.return_value.to_html.return_value = (
        "<html>failure report</html>"
    )
    mock_report_creator.return_value.to_json.return_value = {"message": "failed"}
    mock_report_uploader.return_value.main.return_value = (
        "https://s3.example.com/report.html"
    )

    mock_sns_client = MagicMock()
    mock_boto3.client.return_value = mock_sns_client

    response = lambda_handler(event, context)

    assert response["statusCode"] == 200
    body = (
        json.loads(response["body"])
        if isinstance(response["body"], str)
        else response["body"]
    )
    assert event["Id"] in str(body)


@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_environment_validation_error(mock_validator):
    """Test handler when environment validation fails."""
    event = _create_valid_event()
    context = _create_mock_context()

    mock_validator.validate_environment.side_effect = EnvironmentValidationError(
        "Missing environment variables"
    )

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Missing environment variables" in str(response["body"])


@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_params_validation_error(mock_validator):
    """Test handler when request parameters validation fails."""
    event = {"incomplete": "event"}
    context = _create_mock_context()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.side_effect = ParamsValidationError(
        "Id: field required"
    )

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Id: field required" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_execution_record_lambda_invocation_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_boto3,
):
    """Test handler when execution record lambda invocation fails with AWS error."""
    event = _create_valid_event()
    context = _create_mock_context()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    error_response = {"Error": {"Code": "ServiceException", "Message": "Service error"}}
    boto_error = ClientError(error_response, "InvokeFunction")
    mock_report_lambda_handler.side_effect = boto_error

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to retrieve execution record" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_execution_record_lambda_invocation_unexpected_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_boto3,
):
    """Test handler when execution record lambda invocation fails with unexpected error."""
    event = _create_valid_event()
    context = _create_mock_context()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.side_effect = Exception(
        "Unexpected error retrieving record"
    )

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to retrieve execution record" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_report_creation_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_boto3,
):
    """Test handler when report creation fails."""
    event = _create_valid_event()
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.side_effect = Exception("Failed to create report")

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to generate report" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportUploader")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_report_upload_boto_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_report_uploader,
    mock_boto3,
):
    """Test handler when report upload fails with AWS error."""
    event = _create_valid_event()
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.return_value.to_html.return_value = "<html>report</html>"
    mock_report_creator.return_value.to_json.return_value = {"message": "success"}

    error_response = {"Error": {"Code": "NoSuchBucket", "Message": "Bucket not found"}}
    boto_error = ClientError(error_response, "PutObject")
    mock_report_uploader.return_value.main.side_effect = boto_error

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to upload report" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportUploader")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_report_upload_unexpected_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_report_uploader,
    mock_boto3,
):
    """Test handler when report upload fails with unexpected error."""
    event = _create_valid_event()
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.return_value.to_html.return_value = "<html>report</html>"
    mock_report_creator.return_value.to_json.return_value = {"message": "success"}
    mock_report_uploader.return_value.main.side_effect = Exception(
        "Failed to upload report"
    )

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to upload report" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportUploader")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_sns_creation_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_report_uploader,
    mock_boto3,
):
    """Test handler when SNS message creation fails."""
    event = _create_valid_event()
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.return_value.to_html.return_value = "<html>report</html>"
    mock_report_creator.return_value.to_json.side_effect = Exception(
        "Failed to create SNS message"
    )
    mock_report_uploader.return_value.main.return_value = (
        "https://s3.example.com/report.html"
    )

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to create SNS message" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportUploader")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_sns_publish_boto_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_report_uploader,
    mock_boto3,
):
    """Test handler when SNS publish fails with AWS error."""
    event = _create_valid_event()
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.return_value.to_html.return_value = "<html>report</html>"
    mock_report_creator.return_value.to_json.return_value = {"message": "success"}
    mock_report_uploader.return_value.main.return_value = (
        "https://s3.example.com/report.html"
    )

    error_response = {"Error": {"Code": "NotFound", "Message": "Topic not found"}}
    boto_error = ClientError(error_response, "Publish")

    mock_sns_client = MagicMock()
    mock_sns_client.publish.side_effect = boto_error
    mock_boto3.client.return_value = mock_sns_client

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to publish to SNS" in str(response["body"])


@patch("src.lambdas.reporter.handler.boto3")
@patch("src.lambdas.reporter.handler.ReportUploader")
@patch("src.lambdas.reporter.handler.ReportCreator")
@patch("src.lambdas.reporter.handler.ReportLambdaHandler")
@patch("src.lambdas.reporter.handler.Validator")
def test_lambda_handler_sns_publish_unexpected_error(
    mock_validator,
    mock_report_lambda_handler,
    mock_report_creator,
    mock_report_uploader,
    mock_boto3,
):
    """Test handler when SNS publish fails with unexpected error."""
    event = _create_valid_event()
    context = _create_mock_context()
    mock_record = _create_mock_execution_record()

    mock_validator.validate_environment.return_value = None
    mock_validator.validate_parameters.return_value = MagicMock(
        Id=event["Id"],
        IsSuccess=event["IsSuccess"],
        ErrorDetails=event["ErrorDetails"],
    )

    mock_report_lambda_handler.return_value.main.return_value = mock_record
    mock_report_creator.return_value.to_html.return_value = "<html>report</html>"
    mock_report_creator.return_value.to_json.return_value = {"message": "success"}
    mock_report_uploader.return_value.main.return_value = (
        "https://s3.example.com/report.html"
    )

    mock_sns_client = MagicMock()
    mock_sns_client.publish.side_effect = Exception("Unexpected SNS error")
    mock_boto3.client.return_value = mock_sns_client

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Failed to publish to SNS" in str(response["body"])
