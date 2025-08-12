# Bedrock Ops Copilot

A minimal but production-shaped AIOps copilot that:

1. Ingests incidents via EventBridge
2. Summarizes with Amazon Bedrock
3. Posts a Slack card via AWS Chatbot
4. On approval, executes a safe action using SSM Automation
5. Persists timeline to DynamoDB and artefacts to S3
6. Emits structured logs/metrics and alarms

## Project Structure

- `/infrastructure/` - CDK app
- `/lambda/triager/` - EventBridge -> Bedrock -> Slack message JSON
- `/lambda/approver/` - handles Slack interaction -> SSM Automation
- `/runbooks/` - YAML + markdown
- `/scripts/` - mock-event, deploy helpers
- `/docs/` - ADR-0001, architecture diagram, runbook schema

## Implementation Plan

### 1. Project Structure

- Create all required directories and files
- Set up CDK project structure
- Create Lambda function directories

### 2. Incident Envelope Design

- Define the JSON contract for incident events
- Specify fields like id, severity, signal_type, etc.

### 3. CDK Infrastructure (CopilotCoreStack)

- EventBus: ops-copilot-bus
- Lambda: TriagerFn and ApproverFn
- DynamoDB: IncidentTimeline
- S3: copilot-artifacts and copilot-runbooks
- SSM Document: Copilot-SafeAction
- Chatbot/Slack configuration
- CloudWatch dashboard and alarms

### 4. Lambda Functions

- Triager: EventBridge -> Bedrock -> Slack message
- Approver: Slack interaction -> SSM Automation

### 5. Runbooks

- Define structure with YAML front-matter
- Create sample runbooks

### 6. Deployment Scripts

- Makefile with targets: bootstrap, synth, deploy, destroy, mock-event
- Mock event script

### 7. Documentation

- Architecture diagram
- ADR documentation
- Runbook schema

### 8. Testing Strategy

- Unit tests for envelope validation
- Integration tests
- Dry-run mode for ApproverFn
