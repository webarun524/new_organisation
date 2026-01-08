## v0.33.0 (2025-12-29)


- feat: Buildspec OP exit capture

## v0.32.1 (2025-12-29)


- Merge remote-tracking branch 'origin/main' into bugfix/DATAOPS-11169_bb-pipe-credentials
- fix: Strip HTTPS protocol from URL in policy conditions
- fix: Safer echo in step
- fix: Remove JQ call from pipe
- fix: Debug OICD BB token

## v0.32.0 (2025-12-23)


- fix: fix zipping
- feat: split buildspec
- DATAOPS-11307


## v0.31.0 (2025-12-22)


- fix: Replace shared reference in report gen script
- DATAOPS-10931

## v0.30.0 (2025-12-22)


- feat: Execution handler SFN
- DATAOPS-10931

## v0.29.0 (2025-12-22)


- Merge origin/main into feature/DATAOPS-11169_teardown-tests
- feat: Deployment Data Extractor lambda logic
- feat: Deployment Data Extractor lambda infra
- fix: Lacking Cognito permission in Lambda rotator
- DATAOPS-11169

## v0.28.0 (2025-12-19)


- feat: connect reporting lambda to sfn
- feat: add unit tests for reporter handler
- fix: references and paths in sfn
- DATAOPS-11182

## v0.27.0 (2025-12-18)


- feat: Reporter lambda
- DATAOPS-11181

## v0.26.0 (2025-12-18)


- feat: Fallback and default timeout e2e tests
- DATAOPS-11391

## v0.25.0 (2025-12-17)


- feat: Data portal activation
- DATAOPS-11168

## v0.24.0 (2025-12-17)


- fix: Indent in buildspec fix
- feat: Fetch DP password from CodeBuild directly
- fix: Naming fixes
- chore: Add Lambda calls to utility scripts
- DATAOPS-11174

## v0.23.0 (2025-12-17)


- feat: data portal e2e tests
- DATAOPS-11168

## v0.22.0 (2025-12-11)


- feat: Auth DP playwright tests
- feat: Add SFN validator outputs
- feat: E2E logs. Teardown test mark. Test params unification.
- DATAOPS-11171

## v0.21.1 (2025-12-15)


- chore: Parametrize ENV setup branch
- DATAOPS-11171

## v0.21.0 (2025-12-11)


- fix: approval handler
- feat: add error descriptive error handling to sfn definition
- feat: break sfn steps into smaller chunks
- DATAOPS-11361

## v0.20.0 (2025-12-10)


- feat: SFN execution params lambda
- feat: Dry run logic
- feat: Remove unused SFN params and add DryRun param
- DATAOPS-11361

## v0.19.1 (2025-12-10)


- fix: improve pooling mechanism
- fix: add event filtering by email and fix for approval lambda
- DATAOPS-11316

## v0.19.0 (2025-12-09)


- feat: init db record lambda
- DATAOPS-10931

## v0.18.1 (2025-12-09)


- fix: Infra SFN fixes
- fix: Add inputs to BB pipeline
- DATAOPS-11167

## v0.18.0 (2025-12-09)


- feat: Data Portal TF stack. Shared Route53 script.
- DATAOPS-11167

## v0.17.1 (2025-12-04)


- fix: bitbucket sfn starter pipeline: missing token, spare env.
- fix: buildspec missing deploymentId
- fix: sfn missing error handlings and retries
- feat: make codebuild upload test results to s3
- feat: make codebuild trigger lambda for dynamo record update

## v0.17.0 (2025-12-03)


- feat: bitbucket pipeline for running sfn
- feat: bitbucket permissions for running sfn
- DATAOPS-11190

## v0.16.1 (2025-12-02)


- fix: Adjust deploy.sh and destroy.sh scripts to new TF vars
- fix: Correct SSM param names

## v0.16.0 (2025-12-02)


- feat: codebuild for running e2e tests
- DATAOPS-11172

## v0.15.0 (2025-11-28)


- feat: Add lambda execution permission. Adjust URL mapping
- feat: Config composer. Env parametrization refactor
- feat: Make backplane_account_id dynamic
- feat: Injectable Env code. Readme adjustments. TfVars examples. Review fixes.
- feat: Unit tests. Backplane infra changes. Deployment env code requirement.
- feat: Backplane auth seeder lambda
- feat: Auth backplane resources management
- DATAOPS-11170

## v0.14.0 (2025-11-26)


- feat: SFN: data portal http checker loop
- DATAOPS-10933

## v0.13.0 (2025-11-26)


- feat: connect commit collector lambda to SFN
- fix: move Environment type to shared.domain, update types
- DATAOPS-11175

## v0.12.0 (2025-11-24)


- feat: Playwright python tests frame and auth
- DATAOPS-11170
- chore: Formatting corrections

## v0.11.0 (2025-11-21)


- feat: bitbucket deployment pipeline status checker lambda
- DATAOPS-11188

## v0.10.0 (2025-11-21)


- feat: lambda for triggering bitbucket deployments pipeline
- DATAOPS-11179

## v0.9.1 (2025-11-19)

- chore: Combine test report resources
- DATAOPS-11166

## v0.9.0 (2025-11-19)


- feat: setup trigger lambda
- DATAOPS-11179

## v0.8.0 (2025-11-17)


- fix: Move pynamodb to runtime deps
- feat: Test Execution Record Handler

## v0.7.0 (2025-11-14)


- feat: sns topic ans ses for sending final report
- DATAOPS-11163

## v0.6.0 (2025-11-10)

- feat: commit hash collector lambda

## v0.5.0 (2025-11-06)


- feat: E2E test suite SFN frame

## v0.4.1 (2025-11-07)

- fix: Disable adding tags by commitizen

## v0.4.0 (2025-11-06)

- feat: Move add version tag to before quality tests

## v0.3.2 (2025-11-06)

- feat: Add tags with version

## v0.3.1 (2025-11-06)

- feat: Create E2E DynamoDB Schema
- DATAOPS-11165

## v0.3.0 (2025-11-05)

- feat: approval lambda
- DATAOPS-11183

## v0.2.3 (2025-11-04)

- verify repo setup

## v0.2.2 (2025-11-03)

- fix: don't check cz on main

## v0.2.1 (2025-11-03)

- fix: bitbucket pipeline

## v0.2.0 (2025-11-03)

- [feat] configure repository
- DATAOPS-11162
