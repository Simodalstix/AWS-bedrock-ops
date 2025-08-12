# Architecture Diagram

## Overview

This document describes the architecture of the bedrock-ops-copilot system with a Mermaid diagram.

## Architecture Diagram

```mermaid
graph TD
    A[EventBridge<br/>ops-copilot-bus] --> B[Triager Lambda]
    B --> C[Amazon Bedrock<br/>(Feature Flag)]
    B --> D[DynamoDB<br/>IncidentTimeline]
    B --> E[S3<br/>copilot-artifacts]
    B --> F[SNS<br/>Slack Notifications]
    B --> G[EventBridge<br/>Closure Events]

    H[Slack<br/>Approval] --> I[Approver Lambda]
    I --> J[SSM Automation<br/>Copilot-SafeAction]
    I --> D
    I --> E

    K[Runbooks<br/>S3 copilot-runbooks] --> B

    L[Chatbot<br/>Slack Channel] --> F

    M[CloudWatch<br/>Dashboard/Alarms] --> B
    M --> I

    N[Athena<br/>Optional Enrichment] --> B

    subgraph AWS Cloud
        A
        B
        C
        D
        E
        F
        G
        H
        I
        J
        K
        L
        M
        N
    end

    subgraph Feature Flags
        O[FEATURE_BEDROCK<br/>Default: false]
        P[FEATURE_ATHENA<br/>Default: false]
        Q[DRY_RUN<br/>Default: true]
    end

    O -.-> B
    P -.-> B
    Q -.-> I
```

## Component Descriptions

### Event Ingestion

- EventBridge bus receives incident events from various sources
- Organization-wide PutEvents policy (off by default)
- Development-only open policy for testing

### Incident Processing (Triager)

- Triggered by EventBridge events
- Validates incident envelopes
- Selects appropriate runbooks
- Summarizes incidents using Bedrock (when enabled)
- Enriches incidents using Athena (when enabled)
- Stores timeline in DynamoDB
- Stores artifacts in S3
- Publishes notifications to Slack via SNS

### Approval Processing (Approver)

- Receives approval events from Slack
- Executes SSM Automation documents
- Updates incident timeline
- Stores execution artifacts

### Data Storage

- DynamoDB for incident timeline
- S3 for artifacts and runbooks
- CloudWatch for logs and metrics

### Notification

- SNS topic for Slack notifications
- Chatbot integration with Slack
- CloudWatch alarms and dashboard

### Feature Flags

- FEATURE_BEDROCK: Enable/disable Bedrock integration
- FEATURE_ATHENA: Enable/disable Athena enrichment
- DRY_RUN: Enable/disable actual SSM execution

## Data Flow

1. Incident event is published to EventBridge
2. Triager Lambda is triggered
3. Incident is validated and processed
4. Summary is generated (Bedrock or stub)
5. Enrichment is added (Athena or stub)
6. Timeline entry is stored in DynamoDB
7. Artifact is stored in S3
8. Notification is sent to Slack via SNS
9. If approved, Approver Lambda executes SSM Automation
10. Action results are stored in DynamoDB and S3

## Security Boundaries

- IAM roles with least privilege
- KMS encryption for data at rest
- VPC endpoints (optional)
- API Gateway authentication for approvals
