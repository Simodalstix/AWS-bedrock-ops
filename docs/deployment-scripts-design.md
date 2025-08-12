# Deployment Scripts Design

## Overview

This document describes the deployment scripts and Makefile targets for the bedrock-ops-copilot.

## Makefile Targets

### bootstrap

- Initializes the CDK toolkit stack in the AWS account
- Should be run once per account/region

### synth

- Synthesizes the CDK application and generates CloudFormation templates
- Useful for reviewing changes before deployment

### deploy

- Deploys the CDK stacks to the AWS account
- Creates all infrastructure components
- Default deployment includes only CopilotCoreStack

### deploy-with-athena

- Deploys both CopilotCoreStack and AthEnrichmentStack
- Enables Athena integration features

### destroy

- Destroys the deployed stacks
- Requires confirmation before proceeding
- Does not delete S3 buckets or DynamoDB tables by default (protected resources)

### mock-event

- Sends a sample incident envelope to the EventBridge bus
- Useful for testing the end-to-end workflow
- Uses the script in `scripts/mock_event.py`

### test

- Runs unit tests for Lambda functions
- Validates incident envelope processing
- Checks runbook selection logic

### test-integration

- Runs integration tests
- Verifies EventBridge -> Triager -> DynamoDB/SNS flow
- Requires deployed infrastructure

## Mock Event Script

### Location

`scripts/mock_event.py`

### Functionality

- Generates a sample incident envelope
- Sends the event to the ops-copilot-bus EventBridge bus
- Can be customized with different incident types

### Usage

```bash
make mock-event
# or
python scripts/mock_event.py
```

## Environment Variables

The deployment scripts respect the following environment variables:

### AWS_REGION

- Default: ap-southeast-2
- Can be overridden to deploy to different regions

### AWS_PROFILE

- Default: default
- Specifies which AWS CLI profile to use

### FEATURE_BEDROCK

- Default: false
- Enables or disables Bedrock integration

### FEATURE_ATHENA

- Default: false
- Enables or disables Athena integration

## CDK Context Parameters

### bedrock-model

- Specifies which Bedrock model to use when FEATURE_BEDROCK is true

### athena-workgroup

- Specifies which Athena workgroup to use when FEATURE_ATHENA is true

## Deployment Process

1. Run `make bootstrap` (first time only)
2. Run `make synth` to review changes
3. Run `make deploy` to deploy infrastructure
4. Run `make mock-event` to test the workflow
5. Run `make test` to execute unit tests

## CI/CD Integration

The Makefile is designed to be compatible with CI/CD systems:

- All targets are idempotent
- Error codes are properly returned
- Output is structured for logging systems
