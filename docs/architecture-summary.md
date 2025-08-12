# Bedrock Ops Copilot - Architecture Summary

## Project Overview

The bedrock-ops-copilot is a minimal but production-shaped AIOps solution that automates incident response workflows in AWS environments. It ingests incidents via EventBridge, analyzes them using Amazon Bedrock, notifies operators via Slack, and executes approved actions using SSM Automation.

## Key Components

### 1. Incident Ingestion

- **EventBridge Bus**: Central event bus (ops-copilot-bus) for receiving incident events
- **Incident Envelope**: Standardized JSON contract for incident events with fields like id, severity, signal_type, resource_arns, etc.

### 2. Incident Processing

- **Triager Lambda**: Processes incoming incidents, selects runbooks, generates summaries using Bedrock (when enabled), and notifies operators
- **Feature Flags**:
  - FEATURE_BEDROCK (default: false) - Enables/disables Bedrock integration
  - FEATURE_ATHENA (default: false) - Enables/disables Athena enrichment

### 3. Operator Notification

- **Slack Integration**: Notifications sent via AWS Chatbot and SNS
- **Approval Workflow**: Operators can approve or reject suggested actions via Slack buttons

### 4. Action Execution

- **Approver Lambda**: Handles approval responses and executes SSM Automation documents
- **SSM Automation**: Executes predefined runbooks with appropriate IAM permissions
- **Dry-run Mode**: Safe testing of approval workflows without actual changes

### 5. Data Persistence

- **DynamoDB**: Incident timeline storage with partition key (id) and sort key (ts)
- **S3**:
  - copilot-artifacts: Incident summaries and execution artifacts
  - copilot-runbooks: Operational runbooks used by the system

### 6. Monitoring & Observability

- **CloudWatch**: Dashboard and alarms for system health
- **Structured Logging**: EMF metrics for action_suggested, approval_latency_ms, etc.
- **X-Ray**: Distributed tracing for request flows

## Architecture Diagram

See [architecture-diagram.md](architecture-diagram.md) for the detailed Mermaid diagram.

## Security Design

- **Least Privilege IAM**: Fine-grained permissions for all components
- **KMS Encryption**: Data encryption at rest for S3 and DynamoDB
- **VPC Endpoints**: Optional private connectivity (behind feature flag)
- **API Gateway Security**: Authentication for approval endpoints

## Deployment & Operations

- **CDK Infrastructure**: Infrastructure as Code with Python
- **Makefile**: Standardized deployment commands (bootstrap, synth, deploy, destroy, mock-event)
- **Runbooks**: YAML + Markdown format with metadata front-matter
- **Testing**: Unit tests, integration tests, and dry-run capabilities

## Development Workflow

1. Deploy infrastructure with `make deploy`
2. Test with `make mock-event` to send sample incidents
3. Approve actions via simulated Slack interface
4. Monitor execution via CloudWatch dashboard

## Future Enhancements

- **Security Lake Integration**: Read SSM params and query Athena for security insights
- **Advanced Analytics**: More sophisticated incident correlation and analysis
- **Multi-account Support**: Extend to work across multiple AWS accounts
