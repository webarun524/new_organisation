import io
import json
import logging
import os
import zipfile
from typing import Any

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext
from mypy_boto3_s3 import S3Client
from pydantic import ValidationError

from shared.env_validator import EnvValidator
from shared.utils import create_error_response, create_response, to_snake_case

from .models.params import RequestParams

REPORTS_BUCKET_NAME_ENV_VAR = "REPORTS_BUCKET_NAME"
REPORTS_FOLDER_NAME_ENV_VAR = "REPORTS_FOLDER_NAME"
ENV_VARIABLE_KEYS = [
    REPORTS_BUCKET_NAME_ENV_VAR,
    REPORTS_FOLDER_NAME_ENV_VAR,
]
FILE_TO_EXTRACT = "outputs.json"
OUTPUT_KEYS = ["workloadVersion", "deploymentId"]

logger = logging.getLogger("deployment_data_extractor")
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, _context: LambdaContext) -> dict[str, Any]:
    logger.info(f"Processing event in deployment_data_extractor: {event}")

    # Validate request parameters
    try:
        data = RequestParams.model_validate(event)
    except ValidationError as e:
        logger.error(f"Request validation failed: {e}")
        error_details = "; ".join(
            [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        )
        return create_error_response(
            400, f"Invalid request parameters: {error_details}", "ValidationError"
        )

    # Validate environment variables
    if not EnvValidator.all_env_vars_present(ENV_VARIABLE_KEYS):
        return create_error_response(
            500, "env_validation: Missing environment variables"
        )
    logger.info("All required environment variables present")

    # Extract deployment data from S3
    s3: S3Client = boto3.client("s3")

    reports_bucket_name = os.environ.get(REPORTS_BUCKET_NAME_ENV_VAR, "")
    reports_folder_name = os.environ.get(REPORTS_FOLDER_NAME_ENV_VAR, "")
    bucket_file_key = f"{reports_folder_name}/{data.execution_id}.zip"
    logger.info(
        f"Fetching deployment artifact from s3://{reports_bucket_name}/{bucket_file_key}"
    )

    try:
        zipped_deployment_artifact = s3.get_object(
            Bucket=reports_bucket_name, Key=bucket_file_key
        )
    except s3.exceptions.NoSuchKey:
        return create_error_response(
            404,
            f"Deployment artifact not found: s3://{reports_bucket_name}/{bucket_file_key}",
        )

    zip_bytes = zipped_deployment_artifact["Body"].read()

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        if FILE_TO_EXTRACT not in z.namelist():
            return create_error_response(404, f"{FILE_TO_EXTRACT} not found in ZIP")

        with z.open(FILE_TO_EXTRACT) as f:
            outputs = json.load(f)

    # Compose response
    missing_keys = [key for key in OUTPUT_KEYS if key not in outputs]
    if missing_keys:
        return create_error_response(
            500, f"Missing expected keys in outputs: {', '.join(missing_keys)}"
        )

    response_payload = {to_snake_case(key): outputs[key] for key in OUTPUT_KEYS}
    logger.info(f"Extracted deployment data: {response_payload}")
    return create_response(200, response_payload)
