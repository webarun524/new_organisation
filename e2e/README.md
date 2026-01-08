# End-to-end (E2E) tests

## Description

This folder contains Playwright + pytest based end-to-end tests for the two web portals used by the project:

- `operations_portal` — tests that exercise the operations portal UI
- `data_portal` — tests for the data portal UI

Tests live under `e2e/tests` and are organized into these two feature folders.

## Validation

Each test must be marked with or validation fixture will fail the run if a test is not annotated:
- `@pytest.mark.operations_portal`
- `@pytest.mark.data_portal_verification`
- `@pytest.mark.data_portal_teardown`
- `@pytest.mark.data_portal_activation`

Tests run has to be marked with mark or validation will fail:
- `-m operations_portal`
- `-m data_portal_verification`
- `-m data_portal_teardown`
- `-m data_portal_activation`

## Installation / setup

1. Install dependencies from repository root

```bash
poetry install
```

2. Configure environment variables

- Copy `example.env.test` to `.env.test` and update values for local runs.
- The test fixtures validate required environment variables and will raise a helpful error if any are missing.

Required variables include (examples):

- `E2E_USER` - Operations Portal password (vide SSM `/edi/e2e/tests/test_admin_user_name`) - source TF
- `OSDU_VERSION` - OSDU version picked for deployment - source SFN params
- `ENTERPRISE_ACTIVE` - Express or Enterprise product type - source SFN params
- `DRY_RUN_ACTIVE` - Dry run active - run tests but don't trigger deployment - source SFN params
- `REGION` - AWS Region - source TF

- `OP_URL` - Operations Portal password (vide SSM `/edi/e2e/tests/operations_portal_url`) - source TF
- `OP_PASSWORD` — Operations Portal password (vide Secret Manager `/edi/e2e/tests/test_admin_user_password`) - source TF
- `DEPLOYMENT_ID` - Unique deployment identifier, extracted from Operations Portal tests - source Lambda
- `TEARDOWN_TRIGGER_ACTIVE` - Flag that initiates Teardown tests - source SFN params

- `DP_DEPLOYMENT_ROLE_NAME` - Data Portal Deployment role name (vide custom role on Data Portal account) - source SFN params
- `DP_ACCOUNT_ID` - Data Portal Account Id - source SFN params
- `DP_DOMAIN` - Data Portal URL (vide Route53 record on Data Portal account) - source SFN params
- `DP_HOSTED_ZONE_ID` - Data Portal Route53 hosten zone ID - source SFN params
- `DP_PASSWORD` — data portal password (extracted from deployment email) - source Lambda


## Fixtures and types

- Shared test configuration type definitions are in `models.py` (`DpTestConfig`, `OpTestConfig`, etc.).
- `e2e/tests/conftest.py` provides common fixtures (Playwright `browser`, env config, marker checks).
- Each portal folder contains its own `conftest.py` that exposes portal-specific fixtures (e.g., `op_page_unauth`, `op_auth_storage_state`).

## Running tests

- Run all tests:

```bash
poetry run pytest e2e -v -m <mark>
```

- Run only operations portal tests:

```bash
poetry run pytest e2e -m operations_portal -v -m <mark>
```

- Run an individual test (headed mode):

```bash
poetry run pytest e2e/tests/operations_portal/auth/test_login.py::test_sign_in_success -v -m <mark> --headed --browser chromium
```

- Slow-motion runs (useful for debugging):

```bash
poetry run pytest e2e -v -m <mark> --slow_mo=200 --browser chromium
```

## Logging

- Tests use a shared logger in `e2e/tests/logger.py`. Logs are written to `e2e/logs/e2e-tests.log` and printed to the console. Console output is colored for readability.

## Best practices and notes

- Avoid committing secrets to the repo. Use `.env.test` locally and keep it out of source control.
- If a test fails due to missing env vars, check `e2e/example.env.test` (or your local `.env.test`) and the fixture error message.
- Ensure tests are annotated with the correct marker to keep runs organized (`operations_portal` vs `data_portal`).

## Troubleshooting

- If Playwright fails to launch the browser in CI, ensure the CI runner provides Playwright system dependencies or run tests in a container that includes them.
- Running headed and slowed mode can be useful to debug tests
```bash
poetry run pytest e2e/<test> -v -m <mark> --headed --slow_mo=1000 --browser chromium
```
- If IDE autocompletion for Playwright `page` objects is missing, fixtures in `e2e/tests/conftest.py` are typed to help editors provide completions.
