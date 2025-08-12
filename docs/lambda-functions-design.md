# Lambda Functions Design

## Overview

This document describes the design of the two Lambda functions in the bedrock-ops-copilot: Triager and Approver.

## Triager Function

### Purpose

Processes incoming incident events from EventBridge, analyzes them using Amazon Bedrock (when enabled), and sends a notification to Slack via Chatbot.

### Workflow

1. Receive incident event from EventBridge
2. Validate incident envelope structure
3. Select appropriate runbook based on incident type
4. If FEATURE_BEDROCK is enabled:
   - Call Amazon Bedrock to generate incident summary
   - Otherwise, use local stub that returns deterministic summary
5. If FEATURE_ATHENA is enabled:
   - Call Athena enrichment function
   - Otherwise, use static enrichment data
6. Store incident summary in S3 artifacts bucket
7. Write incident to DynamoDB timeline
8. Publish message to SNS topic for Slack notification

### Environment Variables

- RUNBOOKS_BUCKET: S3 bucket containing runbooks
- DDB_TABLE: DynamoDB table name for incident timeline
- BEDROCK_MODEL: Bedrock model ID to use for summarization
- FEATURE_BEDROCK: Boolean flag to enable Bedrock integration
- FEATURE_ATHENA: Boolean flag to enable Athena enrichment

### Dependencies

- S3 client for accessing runbooks and storing artifacts
- DynamoDB client for timeline storage
- Bedrock client (optional) for summarization
- SNS client for Slack notifications

## Approver Function

### Purpose

Handles approval responses from Slack and executes safe actions using SSM Automation.

### Workflow

1. Receive approval event from Slack via API Gateway
2. Validate approval payload
3. If in dry-run mode:
   - Log intended action without executing
4. Otherwise:
   - Start SSM Automation execution with parameters
   - Monitor execution status
5. Update incident timeline in DynamoDB
6. Store execution artifacts in S3

### Environment Variables

- DRY_RUN: Boolean flag to enable dry-run mode
- SSM_DOCUMENT_NAME: Name of the SSM Automation document to execute

### Dependencies

- SSM client for automation execution
- DynamoDB client for timeline updates
- S3 client for storing artifacts

## Feature Flags Implementation

### Bedrock Stub

When FEATURE_BEDROCK is false, the triager function uses a local stub that returns a deterministic summary instead of calling the actual Bedrock API.

### Athena Stub

When FEATURE_ATHENA is false, the triager function returns static enrichment data instead of querying Athena.

## Error Handling

Both functions implement comprehensive error handling:

- Invalid incident envelopes are rejected with descriptive errors
- Failed Bedrock calls fall back to stubbed responses
- Failed SSM executions are logged and retried if appropriate
- All errors are logged with structured data for debugging
