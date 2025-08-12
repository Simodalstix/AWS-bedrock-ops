# Testing Strategy

## Overview

This document describes the testing approach for the bedrock-ops-copilot, including unit tests, integration tests, and dry-run capabilities.

## Unit Tests

### Incident Envelope Validation

- Test valid incident envelopes pass validation
- Test invalid envelopes are properly rejected
- Test edge cases and boundary conditions
- Test all required fields are checked

### Runbook Selection Logic

- Test runbook selection based on service matching
- Test runbook selection based on action matching
- Test runbook selection based on risk level
- Test runbook selection with no matching runbooks

### Feature Flag Behavior

- Test Bedrock stub behavior when FEATURE_BEDROCK=false
- Test Athena stub behavior when FEATURE_ATHENA=false
- Test actual Bedrock calls when FEATURE_BEDROCK=true
- Test actual Athena queries when FEATURE_ATHENA=true

## Integration Tests

### End-to-End Workflow

- PutEvents to EventBridge bus
- Verify TriagerFn processes the event
- Check DynamoDB timeline for new entries
- Verify SNS message publication
- Validate S3 artifact storage

### Approval Workflow

- Simulate Slack approval interaction
- Verify ApproverFn processes the approval
- Check SSM Automation execution (dry-run mode)
- Validate timeline updates in DynamoDB

### Error Handling

- Test error paths in the workflow
- Verify proper error logging and metrics
- Check incident state management during errors

## Dry-Run Mode

### Triager Function

- No specific dry-run mode needed
- Already uses stubbed Bedrock when FEATURE_BEDROCK=false

### Approver Function

- When DRY_RUN=true, SSM Automation is not actually executed
- Logs the intended action without making changes
- Useful for testing approval workflow without affecting production

## Test Data

### Sample Incident Envelopes

- High severity ALARM type incidents
- Medium severity DEPLOY type incidents
- Low severity SECURITY type incidents
- Custom type incidents

### Sample Runbooks

- Lambda scaling runbooks
- EC2 reboot runbooks
- RDS maintenance runbooks
- Custom service runbooks

## Testing Tools

### Local Testing

- AWS SAM CLI for local Lambda testing
- moto for mocking AWS services
- pytest for test framework

### Cloud Testing

- AWS CloudFormation StackSets for multi-account testing
- AWS CodeBuild for CI testing
- Manual testing in development accounts

## Test Execution

### Automated Tests

- Run with `make test` target
- Execute in CI/CD pipeline
- Generate test reports

### Manual Tests

- Run with `make test-integration` target
- Require deployed infrastructure
- Validate actual AWS service interactions

## Test Coverage Goals

- Unit test coverage: 80%+
- Integration test coverage: Key workflows
- Error path testing: All major failure scenarios
- Feature flag testing: All combinations of flags
