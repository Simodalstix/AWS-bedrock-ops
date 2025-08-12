---
id: ec2-reboot
service: Amazon EC2
action: Reboot instance
risk: MEDIUM
prerequisites:
  - Instance must be in a rebootable state
  - Instance should not be in critical production use
tags:
  - ec2
  - instance
  - maintenance
version: 1.0
---

# Reboot EC2 Instance

This runbook reboots an EC2 instance to resolve performance or connectivity issues.

## Parameters

- InstanceId: ID of the EC2 instance to reboot
- Region: AWS region of the instance

## Steps

1. Validate instance state (running or stopped)
2. Check for any ongoing operations
3. Send reboot command via EC2 API
4. Monitor instance state transitions
5. Verify instance health after reboot

## Implementation

When executed via the bedrock-ops-copilot, this runbook will be triggered automatically when:

- An incident is detected with MEDIUM or HIGH severity
- The affected resource is an EC2 instance
- Metrics indicate the need for a reboot

The system will:

1. Validate the instance is in a safe state for reboot
2. Check for any critical processes running
3. Execute the reboot with proper IAM permissions
4. Monitor the instance for successful restart
5. Alert if issues persist after reboot
