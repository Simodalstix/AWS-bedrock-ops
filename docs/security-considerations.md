# Security Considerations

## Overview

This document describes the security design and considerations for the bedrock-ops-copilot.

## IAM Least Privilege

### Triager Function Permissions

- logs:\* - For CloudWatch logging
- bedrock:InvokeModel - Only when FEATURE_BEDROCK=true, with condition on model ID
- s3:GetObject, s3:PutObject - Only on specific buckets (artifacts/runbooks)
- dynamodb:PutItem, dynamodb:Query - Only on IncidentTimeline table
- sns:Publish - Only on specific SNS topic for Slack notifications
- events:PutEvents - Only to emit closure events

### Approver Function Permissions

- ssm:StartAutomationExecution, ssm:GetAutomationExecution - For executing runbooks
- lambda:PutProvisionedConcurrencyConfig - Scoped to specific Lambda functions only
- cloudwatch:PutMetricData - For structured metrics

## Data Protection

### S3 Encryption

- All S3 buckets use SSE-KMS encryption
- copilot-artifacts bucket versioned for data protection
- copilot-runbooks bucket for deployment assets

### DynamoDB Encryption

- IncidentTimeline table uses DynamoDB encryption at rest
- No sensitive data stored in plaintext

### KMS Keys

- Customer-managed KMS keys for S3 encryption
- Key rotation policies enabled
- Least privilege access to keys

## Network Security

### VPC Configuration

- Optional VPC endpoints behind feature flag
- PrivateLink support for AWS service access
- No direct internet access from Lambda functions

### API Gateway Security

- ApproverFn exposed via API Gateway
- IAM authentication for API endpoints
- Request validation at the API Gateway level

## Feature Flags Security

### Bedrock Integration

- FEATURE_BEDROCK flag controls access to Bedrock
- Conditional IAM permissions based on model ID
- Default disabled for development environments

### Athena Integration

- FEATURE_ATHENA flag controls access to Athena
- Minimal IAM permissions for querying
- Default disabled for development environments

## Secure Development Practices

### Environment Variables

- No secrets stored in environment variables
- All sensitive configuration via AWS Systems Manager Parameter Store
- KMS encryption for sensitive parameters

### Code Security

- Static code analysis in CI/CD pipeline
- Dependency vulnerability scanning
- Regular security assessments

## Incident Response Security

### Evidence Handling

- Immutable logging to CloudWatch
- S3 versioning for artifact storage
- Audit trail in DynamoDB timeline

### Approval Workflow

- Explicit approval required for actions
- Approval simulation in development
- Detailed logging of all actions taken

## Compliance Considerations

### Data Retention

- Lifecycle policies for S3 objects
- DynamoDB TTL for old incident records
- Compliance with data retention policies

### Audit Logging

- CloudTrail for AWS API calls
- Structured application logs
- Metrics for monitoring and alerting
