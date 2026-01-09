import pytest

from src.shared import utils


def test_create_response():
    result = utils.create_response(200, {"foo": "bar"})
    assert result["statusCode"] == 200
    assert result["body"] == {"foo": "bar"}


def test_create_error_response_default_type():
    result = utils.create_error_response(400, "bad request")
    assert result["statusCode"] == 400
    assert result["body"]["error"] == "Error"
    assert result["body"]["message"] == "bad request"


def test_create_error_response_custom_type():
    result = utils.create_error_response(404, "not found", error_type="NotFound")
    assert result["statusCode"] == 404
    assert result["body"]["error"] == "NotFound"
    assert result["body"]["message"] == "not found"


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("CamelCase", "camel_case"),
        ("HTTPRequest", "http_request"),
        ("already_snake_case", "already_snake_case"),
        ("lowercase", "lowercase"),
        ("JSON2Dict", "json2_dict"),
        ("MyHTTPClass", "my_http_class"),
    ],
)
def test_to_snake_case(input_str, expected):
    assert utils.to_snake_case(input_str) == expected
