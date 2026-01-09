"""Tests for MessageParser class."""

import pytest

from lambdas.approval_handler.models.message import ParsedMessage
from lambdas.approval_handler.parsers.message import MessageParser


def test_parse_message_success(sample_sns_message):
    """Test successful parsing of a valid message."""
    result = MessageParser.parse(sample_sns_message)

    assert isinstance(result, ParsedMessage)
    assert (
        result.product_deployment_info.ProductDeploymentId.hex
        == "8c2befe5a86a46748a247ea0a542b94d"
    )
    assert result.product_deployment_info.Status == "PENDING_DEPLOYMENT_APPROVAL"
    assert (
        result.approve_url
        == "https://subscribe.mb-proto2.us-east-1.dev.saas.dataops.47lining.com/v1/Approve?ApprovalRequestId"
    )
    assert (
        result.reject_url
        == "https://subscribe.mb-proto2.us-east-1.dev.saas.dataops.47lining.com/v1/Reject?ApprovalRequestId"
    )
    assert result.approval_request_id == "ucsq2-yIO9X9keJI8GGdf9vz6PSbfkmGw827wdFD_y4"


def test_parse_product_deployment_info(sample_sns_message):
    """Test extraction of product deployment info."""
    result = MessageParser.parse(sample_sns_message)

    deploy_info = result.product_deployment_info
    assert deploy_info.InternalProductCode == "EDI_ENTERPRISE_CM"
    assert deploy_info.TechnicalContact.Email == "john.doe@testing.com"
    assert deploy_info.WorkloadVersion == "5.0.1.dev+20251017"


def test_parse_missing_deployment_info():
    """Test parsing fails when deployment info is missing."""
    invalid_message = """Organization Info:
{}

Product Deployment Info:"""

    with pytest.raises(ValueError, match="Product Deployment Info not found"):
        MessageParser.parse(invalid_message)


def test_parse_missing_approve_url():
    """Test parsing fails when approve URL is missing."""
    invalid_message = """Organization Info:
{}

Product Deployment Info:
{}

Approve:
Reject: https://example.com?ApprovalRequestId=
Approval Request Id: test123"""

    with pytest.raises(ValueError, match="Approve URL not found"):
        MessageParser.parse(invalid_message)


def test_parse_missing_reject_url():
    """Test parsing fails when reject URL is missing."""
    invalid_message = """Organization Info:
{}

Product Deployment Info:
{}

Approve: https://example.com?ApprovalRequestId=
Approval Request Id: test123"""

    with pytest.raises(ValueError, match="Reject URL not found"):
        MessageParser.parse(invalid_message)


def test_parse_missing_approval_request_id():
    """Test parsing fails when approval request ID is missing."""
    invalid_message = """Organization Info:
{}

Product Deployment Info:
{}

Approve: https://example.com?ApprovalRequestId=
Reject: https://example.com?ApprovalRequestId="""

    with pytest.raises(ValueError, match="Approval Request ID not found"):
        MessageParser.parse(invalid_message)


def test_parse_invalid_json():
    """Test parsing fails with invalid JSON."""
    invalid_message = """Product Deployment Info:
{invalid json}

Approve: https://example.com?ApprovalRequestId=
Reject: https://example.com?ApprovalRequestId=
Approval Request Id: test123"""

    with pytest.raises(ValueError, match="Failed to parse JSON in message"):
        MessageParser.parse(invalid_message)
