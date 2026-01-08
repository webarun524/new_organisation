import io
import json
import zipfile
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.lambdas.deployment_data_extractor import handler as dde_handler


class DummyNoSuchKey(Exception):
    pass


def make_zip_bytes(filename: str, content: bytes) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(filename, content)
    buf.seek(0)
    return buf.read()


def test_validation_error_triggers_400(make_validation_error):
    with patch(
        "src.lambdas.deployment_data_extractor.handler.RequestParams.model_validate"
    ) as mock_validate:
        mock_validate.side_effect = make_validation_error

        resp = dde_handler.lambda_handler({"dummy": "data"}, MagicMock())

    assert resp["statusCode"] == 400
    assert "Invalid request parameters" in resp["body"]["message"]
    assert "ValidationError" in resp["body"]["error"]


def test_missing_env_vars_triggers_500():
    with (
        patch(
            "src.lambdas.deployment_data_extractor.handler.RequestParams.model_validate",
            return_value=MagicMock(execution_id="exec-1"),
        ),
        patch("src.lambdas.deployment_data_extractor.handler.EnvValidator") as mock_env,
    ):
        mock_env.all_env_vars_present.return_value = False

        resp = dde_handler.lambda_handler({"execution_id": "exec-1"}, MagicMock())

    assert resp["statusCode"] == 500
    assert "env_validation" in resp["body"]["message"]


def test_s3_missing_key_triggers_404():
    mock_s3 = MagicMock()
    # craft exceptions container with NoSuchKey
    mock_s3.exceptions = SimpleNamespace(NoSuchKey=DummyNoSuchKey)
    mock_s3.get_object.side_effect = DummyNoSuchKey()

    with (
        patch(
            "src.lambdas.deployment_data_extractor.handler.RequestParams.model_validate",
            return_value=MagicMock(execution_id="exec-2"),
        ),
        patch("src.lambdas.deployment_data_extractor.handler.EnvValidator") as mock_env,
        patch(
            "boto3.client",
        ) as mock_boto_client,
    ):
        mock_env.all_env_vars_present.return_value = True
        mock_boto_client.return_value = mock_s3

        resp = dde_handler.lambda_handler({"execution_id": "exec-2"}, MagicMock())

    assert resp["statusCode"] == 404
    assert "Deployment artifact not found" in resp["body"]["message"]


def test_zip_missing_outputs_json_triggers_404():
    # create zip without outputs.json
    zip_bytes = make_zip_bytes("other.txt", b"hello")

    mock_body = MagicMock()
    mock_body.read.return_value = zip_bytes

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": mock_body}

    with (
        patch(
            "src.lambdas.deployment_data_extractor.handler.RequestParams.model_validate",
            return_value=MagicMock(execution_id="exec-3"),
        ),
        patch("src.lambdas.deployment_data_extractor.handler.EnvValidator") as mock_env,
        patch(
            "boto3.client",
        ) as mock_boto_client,
    ):
        mock_env.all_env_vars_present.return_value = True
        mock_boto_client.return_value = mock_s3

        resp = dde_handler.lambda_handler({"execution_id": "exec-3"}, MagicMock())

    assert resp["statusCode"] == 404
    assert "outputs.json not found" in resp["body"]["message"]


def test_missing_output_keys_triggers_500():
    outputs = {"workloadVersion": "1.0"}  # missing deploymentId
    zip_bytes = make_zip_bytes("outputs.json", json.dumps(outputs).encode())

    mock_body = MagicMock()
    mock_body.read.return_value = zip_bytes

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": mock_body}

    with (
        patch(
            "src.lambdas.deployment_data_extractor.handler.RequestParams.model_validate",
            return_value=MagicMock(execution_id="exec-4"),
        ),
        patch("src.lambdas.deployment_data_extractor.handler.EnvValidator") as mock_env,
        patch(
            "boto3.client",
        ) as mock_boto_client,
    ):
        mock_env.all_env_vars_present.return_value = True
        mock_boto_client.return_value = mock_s3

        resp = dde_handler.lambda_handler({"execution_id": "exec-4"}, MagicMock())

    assert resp["statusCode"] == 500
    assert "Missing expected keys in outputs" in resp["body"]["message"]


def test_success_returns_200_and_payload():
    outputs = {"workloadVersion": "1.2.3", "deploymentId": "dep-123"}
    zip_bytes = make_zip_bytes("outputs.json", json.dumps(outputs).encode())

    mock_body = MagicMock()
    mock_body.read.return_value = zip_bytes

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": mock_body}

    with (
        patch(
            "src.lambdas.deployment_data_extractor.handler.RequestParams.model_validate",
            return_value=MagicMock(execution_id="exec-5"),
        ),
        patch("src.lambdas.deployment_data_extractor.handler.EnvValidator") as mock_env,
        patch(
            "boto3.client",
        ) as mock_boto_client,
    ):
        mock_env.all_env_vars_present.return_value = True
        mock_boto_client.return_value = mock_s3

        resp = dde_handler.lambda_handler({"execution_id": "exec-5"}, MagicMock())

    assert resp["statusCode"] == 200
    assert resp["body"]["workload_version"] == "1.2.3"
    assert resp["body"]["deployment_id"] == "dep-123"
