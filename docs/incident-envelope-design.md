# Incident Envelope Design

## Overview

The incident envelope is the JSON contract that defines the structure of incident events flowing through the system. This document specifies the required fields and their meanings.

## JSON Schema

```json
{
  "id": "uuid",
  "severity": "HIGH|MEDIUM|LOW",
  "signal_type": "ALARM|DEPLOY|SECURITY|CUSTOM",
  "resource_arns": ["arn:aws:lambda:..."],
  "evidence": { "alarmArn": "...", "logsQuery": "...", "traceId": "..." },
  "change_hint": { "pipeline": "...", "commit": "..." },
  "account": "111111111111",
  "region": "ap-southeast-2",
  "title": "string",
  "description": "string"
}
```

## Field Descriptions

### id

- Type: String (UUID)
- Required: Yes
- Description: Unique identifier for the incident

### severity

- Type: String (Enum)
- Required: Yes
- Description: Incident severity level
- Values: HIGH, MEDIUM, LOW

### signal_type

- Type: String (Enum)
- Required: Yes
- Description: Type of signal that triggered the incident
- Values: ALARM, DEPLOY, SECURITY, CUSTOM

### resource_arns

- Type: Array of Strings
- Required: Yes
- Description: AWS ARNs of affected resources

### evidence

- Type: Object
- Required: Yes
- Description: Evidence supporting the incident
- Fields:
  - alarmArn: ARN of the CloudWatch alarm (if applicable)
  - logsQuery: Query to retrieve relevant logs
  - traceId: Distributed tracing identifier

### change_hint

- Type: Object
- Required: No
- Description: Information about recent changes that may be related
- Fields:
  - pipeline: CI/CD pipeline name
  - commit: Commit hash

### account

- Type: String
- Required: Yes
- Description: AWS account ID where the incident occurred

### region

- Type: String
- Required: Yes
- Description: AWS region where the incident occurred

### title

- Type: String
- Required: Yes
- Description: Brief title describing the incident

### description

- Type: String
- Required: Yes
- Description: Detailed description of the incident
