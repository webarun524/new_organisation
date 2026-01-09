"""Tests for ApprovalService class."""

import pytest
from httpx import AsyncClient, HTTPStatusError, Request, Response

from lambdas.approval_handler.services.approval import ApprovalService


def create_mock_request(url: str = "https://example.com") -> Request:
    """Create a mock httpx Request for testing."""
    return Request("GET", url)


class TestApprovalService:
    """Test suite for ApprovalService."""

    @pytest.mark.asyncio
    async def test_approve_success(self, sample_parsed_message):
        """Test successful approval request."""
        mock_request = create_mock_request()
        mock_response = Response(
            status_code=200,
            json={"status": "approved"},
            request=mock_request,
        )

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            # Mock the _get method to return our mock response
            async def mock_get(url, *args, **kwargs):
                assert (
                    url
                    == "https://subscribe.example.com/v1/Approve?ApprovalRequestId=test-approval-request-id-123"
                )
                return mock_response

            service._get = mock_get

            response = await service.approve(sample_parsed_message)

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_approve_builds_correct_url(self, sample_parsed_message):
        """Test that approve builds the correct URL."""
        urls_called = []

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            async def capture_url(url, *args, **kwargs):
                urls_called.append(url)
                return Response(status_code=200, request=create_mock_request())

            service._get = capture_url

            await service.approve(sample_parsed_message)

            assert len(urls_called) == 1
            assert (
                urls_called[0]
                == "https://subscribe.example.com/v1/Approve?ApprovalRequestId=test-approval-request-id-123"
            )

    @pytest.mark.asyncio
    async def test_approve_http_error(self, sample_parsed_message):
        """Test approval handles HTTP errors correctly."""

        mock_response = Response(
            status_code=500,
            text="Internal Server Error",
            request=create_mock_request(),
        )

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            async def mock_get_error(url, *args, **kwargs):
                return mock_response

            service._get = mock_get_error

            with pytest.raises(HTTPStatusError):
                await service.approve(sample_parsed_message)

    @pytest.mark.asyncio
    async def test_approve_client_error_4xx(self, sample_parsed_message):
        """Test approval handles 4xx client errors."""
        mock_response = Response(
            status_code=404,
            text="Not Found",
            request=create_mock_request(),
        )

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            async def mock_get_error(url, *args, **kwargs):
                return mock_response

            service._get = mock_get_error

            with pytest.raises(HTTPStatusError):
                await service.approve(sample_parsed_message)

    @pytest.mark.asyncio
    async def test_process_records_single_record(
        self, sample_sns_records, author_email
    ):
        """Test processing a single SNS record."""
        mock_response = Response(
            status_code=200,
            text='{"status": "approved"}',
            request=create_mock_request(),
        )

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            async def mock_get(url, *args, **kwargs):
                return mock_response

            service._get = mock_get

            results = await service.process_records(
                sample_sns_records, author_email=author_email
            )

            assert len(results) == 1
            assert results[0]["status_code"] == 200
            assert results[0]["body"] == '{"status": "approved"}'

    @pytest.mark.asyncio
    async def test_process_records_multiple_records(
        self, sample_sns_record, author_email
    ):
        """Test processing multiple SNS records concurrently."""

        records = [sample_sns_record, sample_sns_record, sample_sns_record]

        call_count = 0

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            async def mock_get(url, *args, **kwargs):
                nonlocal call_count
                call_count += 1
                return Response(
                    status_code=200,
                    text=f'{{"result": "approved_{call_count}"}}',
                    request=create_mock_request(),
                )

            service._get = mock_get

            results = await service.process_records(records, author_email=author_email)

            assert len(results) == 3
            assert call_count == 3
            assert all(result["status_code"] == 200 for result in results)

    @pytest.mark.asyncio
    async def test_process_records_with_parsing_error(self, author_email):
        """Test process_records handles parsing errors."""
        invalid_record = {
            "Sns": {
                "TopicArn": "arn:aws:sns:test",
                "MessageId": "msg-123",
                "Message": "Invalid message without required fields",
            }
        }

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            # Execute and assert exception is raised
            with pytest.raises(ValueError):
                await service.process_records(
                    [invalid_record], author_email=author_email
                )

    @pytest.mark.asyncio
    async def test_process_records_mixed_results(self, sample_sns_record, author_email):
        """Test process_records with mixed success and failure responses."""
        records = [sample_sns_record, sample_sns_record]

        call_count = 0

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            async def mock_get_mixed(url, *args, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    return Response(
                        status_code=200, text="success", request=create_mock_request()
                    )
                else:
                    # Second call returns error
                    return Response(
                        status_code=500, text="error", request=create_mock_request()
                    )

            service._get = mock_get_mixed

            results = await service.process_records(records, author_email=author_email)

            assert len(results) == 2
            assert results[0]["status_code"] == 200
            assert results[1]["status_code"] == 500

    @pytest.mark.asyncio
    async def test_process_records_returns_serializable_results(
        self, sample_sns_records, author_email
    ):
        """Test that process_records returns JSON-serializable results."""
        import json

        async with AsyncClient() as client:
            service = ApprovalService(client=client)

            async def mock_get(url, *args, **kwargs):
                return Response(
                    status_code=200, text="test response", request=create_mock_request()
                )

            service._get = mock_get

            results = await service.process_records(
                sample_sns_records, author_email=author_email
            )

            json_str = json.dumps(results)
            assert json_str is not None
            assert isinstance(results[0], dict)
            assert "status_code" in results[0]
            assert "body" in results[0]
