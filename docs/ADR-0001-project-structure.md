# ADR-0001: Project Structure

## Context

We need to establish a clear project structure for the bedrock-ops-copilot that separates concerns and follows AWS CDK best practices.

## Decision

We will organize the project with the following structure:

```
/
├── infrastructure/     # CDK application code
├── lambda/            # Lambda function code
│   ├── triager/       # EventBridge -> Bedrock -> Slack processing
│   └── approver/      # Slack interaction -> SSM Automation
├── runbooks/          # Operational runbooks (YAML + Markdown)
├── scripts/           # Helper scripts for development/deployment
├── docs/              # Documentation including ADRs
├── cdk.json           # CDK configuration
├── Makefile           # Build and deployment commands
└── README.md          # Project overview
```

## Consequences

- Clear separation of infrastructure code from application code
- Easy to locate and modify specific components
- Follows AWS CDK recommended project structure
- Facilitates testing and deployment
