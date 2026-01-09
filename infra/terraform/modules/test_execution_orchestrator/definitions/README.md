# E2E Test Orchestration State Machine Definitions

This directory contains the Step Functions state machine definition split into 8 logical phase files for improved maintainability and readability.

## Overview

The E2E test orchestration state machine is split into separate JSON template files organized by workflow phases:

```
01_validation.json.tpl           → Input parameter validation
02_initialization.json.tpl       → Database and configuration initialization
03_environment_setup.json.tpl    → Environment deployment with polling
04_commit_collection.json.tpl    → Repository commit hash collection
05_operations_portal.json.tpl    → Operations Portal test execution
06_data_portal.json.tpl          → Data Portal deployment, verification, and testing
07_teardown.json.tpl             → Teardown execution and verification
08_reporting.json.tpl            → Final reporting and error handling
```

In `locals.tf`, the phase files are loaded and merged


## State Flow Diagram

```
Validate Input
    ↓
Initialize E2E DB Record
    ↓
Compose Config
    ↓
Skip Env Setup Decision
    ├→ [Yes] Collect Commit Hashes
    └→ [No]  Trigger Environment Setup (with polling loop)
            ↓
         Collect Commit Hashes
    ↓
Operations Portal Tests
    ↓
Dry Run Decision
    ├→ [Yes] Success Path (Database Update → Report → Success)
    └→ [No]  Data Portal Website Pooler Init (with polling)
            ↓
         Data Portal Website Pooler
            ↓
         Login Credentials Extraction
            ↓
         Data Portal Tests
            ↓
         Teardown Tests
            ↓
         Data Portal Website Teardown Pooler
            ↓
         Success Path (Database Update → Report → Success)

[Any Failure] → Failure Path (Database Update → Report → Test Suite Failure)
```

## Adding New States

When adding new states to the workflow:

1. **Determine the appropriate phase file** based on the logical workflow stage
2. **Add the state definition** to the corresponding `.json.tpl` file
3. **Update state references** in other files if the new state appears in "Next" or "Default" fields
4. **Follow error handling patterns**:
   - Use `Catch` blocks with `ErrorEquals: ["States.ALL"]` for generic error handling
   - Create an "Enrich {StateName} Error" Pass state to standardize error information
5. **Test locally** by running `terraform plan` to validate the merged definition
