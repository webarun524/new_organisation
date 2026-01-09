import pytest

from src.lambdas.execution_params_validator.models.sfn_params import SfnParams


@pytest.fixture
def valid_params(mock_sfn_exec_params):
    return {
        "osdu_version": mock_sfn_exec_params["OsduVersion"],
        "enterprise_product_type_active": mock_sfn_exec_params[
            "EnterpriseProductTypeActive"
        ],
        "data_portal_account_id": mock_sfn_exec_params["DataPortalAccountId"],
        "deployment_role_name": mock_sfn_exec_params["DeploymentRoleName"],
        "data_portal_domain": mock_sfn_exec_params["DataPortalDomain"],
        "data_portal_hosted_zone_id": mock_sfn_exec_params["DataPortalHostedZoneId"],
        "dry_run": mock_sfn_exec_params["DryRun"],
        "skip_env_setup": mock_sfn_exec_params["SkipEnvSetup"],
        "teardown_trigger_active": mock_sfn_exec_params.get("TeardownTriggerActive"),
    }


def test_sfn_params_valid(valid_params):
    params = SfnParams(**valid_params)
    assert params.osdu_version == valid_params["osdu_version"]
    assert params.data_portal_domain == valid_params["data_portal_domain"]
    assert isinstance(params.enterprise_product_type_active, bool)
    assert params.dry_run is False


def test_sfn_params_invalid_domain(valid_params):
    invalid = valid_params.copy()
    invalid["data_portal_domain"] = "not_a_domain"
    with pytest.raises(ValueError) as exc:
        SfnParams(**invalid)
    assert "must be a valid domain" in str(exc.value)


def test_sfn_params_invalid_account_id(valid_params):
    invalid = valid_params.copy()
    invalid["data_portal_account_id"] = "123"
    with pytest.raises(ValueError):
        SfnParams(**invalid)


def test_sfn_params_empty_role(valid_params):
    invalid = valid_params.copy()
    invalid["deployment_role_name"] = "   "
    with pytest.raises(ValueError) as exc:
        SfnParams(**invalid)
    assert "cannot be empty" in str(exc.value)


@pytest.mark.parametrize(
    "missing_field",
    [
        "osdu_version",
        "enterprise_product_type_active",
        "data_portal_account_id",
        "deployment_role_name",
        "data_portal_domain",
        "data_portal_hosted_zone_id",
        "dry_run",
        "skip_env_setup",
    ],
)
def test_sfn_params_missing_fields(valid_params, missing_field):
    invalid = valid_params.copy()
    invalid.pop(missing_field)
    with pytest.raises(Exception) as exc:
        SfnParams(**invalid)
    assert missing_field.replace("_", " ") in str(exc.value) or missing_field in str(
        exc.value
    )
