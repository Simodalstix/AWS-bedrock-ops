---
id: rds-maintenance
service: Amazon RDS
action: Apply maintenance updates
risk: MEDIUM
prerequisites:
  - Database must be in available state
  - Maintenance window should be configured
  - Backup should be recent
tags:
  - rds
  - database
  - maintenance
version: 1.0
---

# Apply RDS Maintenance Updates

This runbook applies pending maintenance updates to an RDS instance.

## Parameters

- DBInstanceIdentifier: Identifier of the RDS instance
- ApplyImmediately: Whether to apply updates immediately or during maintenance window

## Steps

1. Validate database state (available)
2. Check for recent backups
3. Review pending maintenance actions
4. Apply maintenance updates
5. Monitor database state during maintenance
6. Verify database functionality after maintenance

## Implementation

When executed via the bedrock-ops-copilot, this runbook will be triggered automatically when:

- An incident is detected related to pending maintenance
- The affected resource is an RDS instance
- Security or performance updates are required

The system will:

1. Validate the database is in a safe state for maintenance
2. Ensure recent backups exist
3. Schedule maintenance during configured maintenance window
4. Apply updates with proper IAM permissions
5. Monitor the database for successful completion
6. Alert if issues are detected after maintenance
