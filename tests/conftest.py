"""Shared fixtures for approval handler tests."""

import datetime
import uuid

import boto3
import pytest
from moto import mock_aws
from pydantic import BaseModel, ValidationError

from lambdas.approval_handler.models.message import (
    ParsedMessage,
    ProductDeployment,
    TechnicalContact,
)
from shared.domain.models.status import StatusList


@pytest.fixture
def sample_sns_message():
    """Sample SNS message content (matches original test data)."""
    return """This message was sent as a part of Customer's Product Deployment creation.
Please check the following information and use the Approve or Reject link.

Organization Info:
{
    "AWSMarketplaceCustomerIdentifier": "47l_internal_org",
    "AWSMarketplaceMocked": false,
    "CommercialSupportContact": {
        "Email": "john2.doe2@testing.com",
        "FirstName": "John2",
        "JobTitle": "47L Engineering Manager",
        "LastName": "Doe2",
        "ToS": true
    },
    "CompanyInformation": {
        "Address": "2535 Augustine Drive",
        "City": "Santa Clara",
        "Country": "USA",
        "Name": "Hitachi Digital Services",
        "PostalCode": "95054",
        "State": "CA",
        "Url": "https://www.HitachiVantara.com"
    },
    "CreatedAt": "2025-04-28T12:40:01.000000+0000",
    "DisplayComponentVersions": true,
    "IsAWSMarketplaceSubscription": false,
    "MaxNumberOfUsers": 50,
    "OrganizationId": "10c13d6c5a5a4a02b180ffe402dc436e",
    "OrganizationType": "ENTERPRISE",
    "ShortUUID": "10c13d6c5a5a",
    "Status": "ACTIVE",
    "TargetAccountValidationEnabled": true,
    "UpdatedAt": "2025-04-28T12:40:01.000000+0000",
    "WorkloadVersionSelectionEnabled": true
}


Product Deployment Info:
{
    "CreatedAt": "2025-10-27T13:51:57.234278+0000",
    "CreatedByUserId": "544864d8-c061-7057-7af5-358488e456c5",
    "InternalProductCode": "EDI_ENTERPRISE_CM",
    "OrganizationId": "10c13d6c5a5a4a02b180ffe402dc436e",
    "ProductDeploymentId": "8c2befe5a86a46748a247ea0a542b94d",
    "ProductFulfillmentInformation": {
        "CustomDomain": "fe-test.edi.internal0.dataops.47lining.com",
        "ExternalId": "10c13d6c5a5a4a02b180ffe402dc436e-8c2befe5a86a46748a247ea0a542b94d",
        "HostedZoneId": "Z054965637BOMEE5JE1QA",
        "IdpProperties": {
            "deployDefaultCognito": true,
            "servicePrincipalScopeSuffix": "osduOnAWSService"
        },
        "IsPrivatelyNetworked": false,
        "LoadSampleData": false,
        "ProductVersion": "osdu-r3m25",
        "Region": "us-east-1",
        "RoleName": "deployment_proto_1_role",
        "TargetAccountId": "391767403170"
    },
    "Status": "PENDING_DEPLOYMENT_APPROVAL",
    "TechnicalContact": {
        "Email": "john.doe@testing.com",
        "FirstName": "John",
        "JobTitle": "dev",
        "LastName": "Doe"
    },
    "UpdatedAt": "2025-10-27T13:54:10.455913+0000",
    "WorkloadVersion": "5.0.1.dev+20251017"
}


Approve: https://subscribe.mb-proto2.us-east-1.dev.saas.dataops.47lining.com/v1/Approve?ApprovalRequestId=

Reject: https://subscribe.mb-proto2.us-east-1.dev.saas.dataops.47lining.com/v1/Reject?ApprovalRequestId=

Approval Request Id: ucsq2-yIO9X9keJI8GGdf9vz6PSbfkmGw827wdFD_y4

To Approve or Reject, please copy/paste into a web browser the Approve or Reject
URL with the Approval Request ID appended.

This is an automatically generated email."""


@pytest.fixture
def sample_sns_record(sample_sns_message):
    """Sample SNS record structure."""
    return {
        "Sns": {
            "TopicArn": "arn:aws:sns:us-east-1:123456789:test-topic",
            "MessageId": "test-message-id-123",
            "Message": sample_sns_message,
        }
    }


@pytest.fixture
def sample_sns_records(sample_sns_record):
    """Sample list of SNS records."""
    return [sample_sns_record]


@pytest.fixture
def sample_technical_contact():
    """Sample technical contact."""
    return TechnicalContact(
        Email="john.doe@testing.com",
        FirstName="John",
        JobTitle="dev",
        LastName="Doe",
    )


@pytest.fixture
def sample_product_deployment(sample_technical_contact):
    """Sample product deployment."""
    return ProductDeployment(
        CreatedByUserId="544864d8-c061-7057-7af5-358488e456c5",
        InternalProductCode="EDI_ENTERPRISE_CM",
        OrganizationId="10c13d6c5a5a4a02b180ffe402dc436e",
        ProductDeploymentId="8c2befe5-a86a-4674-8a24-7ea0a542b94d",
        Status="PENDING_DEPLOYMENT_APPROVAL",
        TechnicalContact=sample_technical_contact,
        WorkloadVersion="5.0.1.dev+20251017",
    )


@pytest.fixture
def author_email():
    """Sample author email for approval filtering."""
    return "john.doe@testing.com"


@pytest.fixture
def sample_parsed_message(sample_product_deployment):
    """Sample parsed message (for unit testing ApprovalService)."""
    return ParsedMessage(
        product_deployment_info=sample_product_deployment,
        approve_url="https://subscribe.example.com/v1/Approve?ApprovalRequestId",
        reject_url="https://subscribe.example.com/v1/Reject?ApprovalRequestId",
        approval_request_id="test-approval-request-id-123",
    )


@pytest.fixture
def full_execution_record_payload():
    return {
        "Id": str(uuid.uuid4()),
        "Status": StatusList.operationsPortalTestsDone.value,
        "WorkloadVersion": "5.0.1",
        "CreatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "UpdatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "DeployedServices": {
            "dataops-mb-vpc": str(uuid.uuid4()),
            "dataops-mb-metering-service": str(uuid.uuid4()),
        },
        "DataPortalUrl": "https://data-portal.example.com",
        "DeploymentId": str(uuid.uuid4()),
        "SubscriptionTestReportUrl": "https://reports.example.com/subscription-test",
        "VerificationTestReportUrl": "https://reports.example.com/verification-test",
        "TeardownTestReportUrl": "https://reports.example.com/teardown-test",
        "FailureReason": "Reason",
    }


@pytest.fixture
def aws_region():
    return "us-east-1"


@pytest.fixture
def assumed_session(aws_region):
    return boto3.Session(
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
        aws_session_token="tok",
        region_name=aws_region,
    )


@pytest.fixture
def secretsmanager(assumed_session, aws_region):
    with mock_aws():
        client = boto3.client(
            "secretsmanager",
            region_name=aws_region,
        )
        yield client


@pytest.fixture
def ssm_client(assumed_session, aws_region):
    with mock_aws():
        client = boto3.client(
            "ssm",
            region_name=aws_region,
        )
        yield client


@pytest.fixture
def dynamodb_resource(assumed_session, aws_region):
    with mock_aws():
        resource = boto3.resource(
            "dynamodb",
            region_name=aws_region,
        )
        yield resource


@pytest.fixture
def ses_client(assumed_session, aws_region):
    with mock_aws():
        client = boto3.client(
            "ses",
            region_name=aws_region,
        )
        yield client


@pytest.fixture
def cognito_client(aws_region):
    with mock_aws():
        yield boto3.client("cognito-idp", region_name=aws_region)


@pytest.fixture
def mock_sfn_exec_params() -> dict:
    return {
        "OsduVersion": "r3m25",
        "EnterpriseProductTypeActive": False,
        "DataPortalAccountId": "018955241485",
        "DeploymentRoleName": "edi-e2e-tests-custom-fulfillment-role",
        "DataPortalDomain": "e2e-test-suite.edi.internal0.dataops.47lining.com",
        "DataPortalHostedZoneId": "Z03189402G93GYQF24E39",
        "DryRun": False,
        "SkipEnvSetup": False,
        "TeardownTriggerActive": False,
    }


@pytest.fixture
def make_validation_error() -> ValidationError:
    class DummyModel(BaseModel):
        foo: int

    try:
        DummyModel.model_validate({"foo": "wrong"})
    except ValidationError as e:
        return e
    return ValidationError([], DummyModel)
