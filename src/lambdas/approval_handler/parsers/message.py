import json
import re

from lambdas.approval_handler.models.message import ParsedMessage


class MessageParser:
    """Parser for SNS approval messages."""

    @staticmethod
    def parse(message: str) -> ParsedMessage:
        """
        Parse an SNS approval message.
        """
        try:
            # Extract Product Deployment Info JSON
            deploy_match = re.search(
                r"Product Deployment Info:\s*(\{.*?\})\s*Approve:",
                message,
                re.DOTALL,
            )
            if not deploy_match:
                raise ValueError("Product Deployment Info not found in message")
            product_deployment_info = json.loads(deploy_match.group(1))

            # Extract Approve URL
            approve_match = re.search(
                r"Approve:\s*(https://[^\s]+\?ApprovalRequestId=)", message
            )
            if not approve_match:
                raise ValueError("Approve URL not found in message")
            approve_url = approve_match.group(1).rstrip("=")

            # Extract Reject URL
            reject_match = re.search(
                r"Reject:\s*(https://[^\s]+\?ApprovalRequestId=)", message
            )
            if not reject_match:
                raise ValueError("Reject URL not found in message")
            reject_url = reject_match.group(1).rstrip("=")

            # Extract Approval Request ID
            request_id_match = re.search(r"Approval Request Id:\s*([^\s]+)", message)
            if not request_id_match:
                raise ValueError("Approval Request ID not found in message")
            approval_request_id = request_id_match.group(1)

            return ParsedMessage(
                product_deployment_info=product_deployment_info,
                approve_url=approve_url,
                reject_url=reject_url,
                approval_request_id=approval_request_id,
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON in message: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse message: {e}")
