# Runbook Design

## Overview

This document describes the structure and format of operational runbooks used by the bedrock-ops-copilot.

## Runbook Structure

Runbooks are stored as YAML files with optional Markdown content. Each runbook has a front-matter section with metadata followed by the runbook content.

### YAML Front-Matter Schema

```yaml
---
id: string
service: string
action: string
risk: HIGH|MEDIUM|LOW
prerequisites:
  - string
tags:
  - string
version: string
---
```

### Field Descriptions

#### id

- Type: String
- Required: Yes
- Description: Unique identifier for the runbook

#### service

- Type: String
- Required: Yes
- Description: AWS service or application the runbook applies to

#### action

- Type: String
- Required: Yes
- Description: Action the runbook performs

#### risk

- Type: String (Enum)
- Required: Yes
- Description: Risk level of executing this runbook
- Values: HIGH, MEDIUM, LOW

#### prerequisites

- Type: Array of Strings
- Required: No
- Description: Prerequisites that must be met before executing

#### tags

- Type: Array of Strings
- Required: No
- Description: Tags for categorizing and searching runbooks

#### version

- Type: String
- Required: No
- Description: Version of the runbook

## Sample Runbook

```yaml
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
```

## Runbook Selection Logic

The triager function selects runbooks based on:

1. Matching service from incident envelope
2. Matching action from incident type
3. Risk level appropriate for incident severity
4. Prerequisites met by the environment

## Runbook Storage

Runbooks are stored in the `copilot-runbooks` S3 bucket and are versioned. The triager function retrieves runbooks from this bucket during incident processing.
