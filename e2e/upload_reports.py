#!/usr/bin/env python3
"""
Upload test reports to S3.

This script zips the contents of the reports directory and uploads
the resulting archive to an S3 bucket.

Usage:
    python upload_reports.py <execution_id> <s3_bucket_name> <test_marker> <execution_record_handler_lambda_name>
"""

import argparse
import sys

import boto3

from e2e.models.enums import TestMarker
from e2e.services.report_lambda_handler import ReportLambdaHandler
from e2e.services.report_uploader import ReportUploader


def main():
    parser = argparse.ArgumentParser(description="Upload test reports to S3")
    parser.add_argument("execution_id", help="Test execution ID")
    parser.add_argument("s3_bucket_name", help="Name of the S3 bucket to upload to")
    parser.add_argument("test_marker", help="Test marker used for test execution")
    parser.add_argument(
        "execution_record_handler_lambda_name",
        help="Name of lambda updating dynamo db report record",
    )
    args = parser.parse_args()

    s3_client = boto3.client("s3")

    report_uploader = ReportUploader(
        s3_client=s3_client, bucket_name=args.s3_bucket_name
    )

    if args.test_marker == TestMarker.data_portal_activation.value:
        raise ValueError("Data Portal Activation tests do not require report upload.")

    report_url = report_uploader.main(
        test_marker=args.test_marker, execution_id=args.execution_id
    )

    lambda_client = boto3.client("lambda")
    report_lambda_handler = ReportLambdaHandler(
        lambda_client=lambda_client,
        function_name=args.execution_record_handler_lambda_name,
    )

    report_lambda_handler.main(
        test_marker=args.test_marker,
        report_url=report_url,
        execution_id=args.execution_id,
    )


if __name__ == "__main__":
    sys.exit(main())
