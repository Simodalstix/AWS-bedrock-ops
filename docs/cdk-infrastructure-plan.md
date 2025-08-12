# CDK Infrastructure Plan

## Overview

This document describes the AWS infrastructure components that will be provisioned using AWS CDK for the bedrock-ops-copilot.

## CopilotCoreStack

### EventBus

- Name: ops-copilot-bus
- Policies:
  - Organization PutEvents policy (off by default)
  - Development-only open policy (for testing)

### Lambda Functions

#### TriagerFn

- Trigger: EventBridge rule on ops-copilot-bus
- Environment Variables:
  - RUNBOOKS_BUCKET: S3 bucket for runbooks
  - DDB_TABLE: DynamoDB table name
  - BEDROCK_MODEL: Bedrock model ID
  - FEATURE_BEDROCK: Feature flag (default false)
  - FEATURE_ATHENA: Feature flag (default false)
- Permissions:
  - logs:\*
  - bedrock:InvokeModel (when FEATURE_BEDROCK=true)
  - s3:GetObject, s3:PutObject on artifacts/runbooks buckets
  - dynamodb:PutItem, dynamodb:Query on IncidentTimeline table
  - sns:Publish (for Slack notifications)
  - events:PutEvents (emit closure events)

#### ApproverFn

- Trigger: API Gateway endpoint for Slack interactions
- Functionality: Processes approval requests and triggers SSM Automation
- Permissions:
  - ssm:StartAutomationExecution, ssm:GetAutomationExecution
  - lambda:PutProvisionedConcurrencyConfig (scoped to specific resources)
  - cloudwatch:PutMetricData

### DynamoDB

- Table Name: IncidentTimeline
- Primary Key: id (partition key), ts (sort key)
- Billing Mode: On-demand

### S3 Buckets

#### copilot-artifacts

- Versioned
- SSE-KMS encryption
- Lifecycle policies for cost optimization

#### copilot-runbooks

- Deployment asset bucket
- SSE-KMS encryption
- Read-only access for Lambda functions

### SSM Document

- Name: Copilot-SafeAction
- Type: Automation document
- Functionality: Sample action (e.g., increase provisioned concurrency on a named Lambda)

### Chatbot/Slack Integration

- Slack channel configuration placeholder
- SNS topic for publishing messages to Slack
- TriagerFn publishes to this topic

### CloudWatch

- Dashboard with key metrics
- Alarms:
  - Lambda Errors
  - Lambda Throttles
  - No AgeOfOldestMessage alarm needed at this time

## Optional AthEnrichmentStack

### Athena Workgroup

- Minimal configuration
- IAM permissions for querying

### Query Function

- Called by Triager when FEATURE_ATHENA=true
- Returns static enrichment data when disabled
