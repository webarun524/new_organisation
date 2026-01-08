import boto3

from src.lambdas.config_composer.services.ssm import (
    fetch_required_ssm_params,
)


def test_fetch_required_ssm_params(ssm_client, aws_region):
    service_name = "test-service"
    base = service_name.replace("-", "/")
    admin_param = f"/{base}/test_admin_user_name"
    ops_param = f"/{base}/operations_portal_url"
    bb_code_param = f"/{base}/bb_env_code"
    bb_name_param = f"/{base}/bb_env_name"

    # create parameters in the moto-backed client
    ssm_client.put_parameter(Name=admin_param, Value="admin@example.com", Type="String")
    ssm_client.put_parameter(Name=ops_param, Value="https://ops.example", Type="String")
    ssm_client.put_parameter(Name=bb_code_param, Value="vdev", Type="String")
    ssm_client.put_parameter(Name=bb_name_param, Value="Dev", Type="String")

    # wrap the real client in a session-like object that ensures get_parameters returns ARN
    class SessionWithARN:
        def __init__(self, real_client, region):
            self._real = real_client
            self.region_name = region

        def client(self, svc_name):
            if svc_name != "ssm":
                return boto3.Session(region_name=self.region_name).client(svc_name)

            real = self._real

            class Wrapper:
                def get_parameters(self, Names, WithDecryption=False):
                    resp = real.get_parameters(
                        Names=Names, WithDecryption=WithDecryption
                    )
                    for p in resp.get("Parameters", []):
                        p.setdefault(
                            "ARN",
                            f"arn:aws:ssm:{aws_region}:000000000000:parameter{p['Name']}",
                        )
                    return resp

            return Wrapper()

    session = SessionWithARN(ssm_client, aws_region)
    ssm_values = fetch_required_ssm_params(session, "test-service")  # type: ignore
    assert ssm_values.admin_username == "admin@example.com"
    assert ssm_values.admin_username_arn.startswith("arn:aws:ssm")
    assert ssm_values.bb_env_code == "vdev"
    assert ssm_values.bb_env_name == "Dev"
