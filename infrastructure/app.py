#!/usr/bin/env python3
import aws_cdk as cdk
from copilot_core_stack import CopilotCoreStack

app = cdk.App()

# Core stack with all main components
CopilotCoreStack(app, "CopilotCoreStack")

app.synth()
