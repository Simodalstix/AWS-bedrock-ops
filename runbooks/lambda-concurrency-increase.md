---
id: lambda-concurrency-increase
service: AWS Lambda
action: Increase provisioned concurrency
risk: LOW
prerequisites:
  - Lambda function must have provisioned concurrency configured
tags:
  - lambda
  - performance
  - scaling
version: 1.0
---

# Increase Lambda Provisioned Concurrency

This runbook increases the provisioned concurrency for a Lambda function to handle increased load.

## Parameters

- FunctionName: Name of the Lambda function
- Concurrency: New concurrency value

## Steps

1. Validate parameters
2. Call lambda:PutProvisionedConcurrencyConfig
3. Verify the change was applied successfully
4. Monitor function metrics for stabilization

## Implementation

When executed via the bedrock-ops-copilot, this runbook will be triggered automatically when:

- An incident is detected with HIGH severity
- The affected resource is a Lambda function
- Metrics indicate the need for increased concurrency

The system will:

1. Validate the function has provisioned concurrency enabled
2. Calculate appropriate concurrency level based on current load
3. Execute the change with proper IAM permissions
4. Monitor the function for stabilization
5. Rollback if issues are detected
