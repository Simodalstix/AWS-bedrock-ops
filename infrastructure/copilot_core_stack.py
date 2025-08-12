from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_sns as sns,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_chatbot as chatbot,
    aws_logs as logs,
    Duration,
    CfnOutput,
)
from constructs import Construct


class CopilotCoreStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # EventBus for receiving incident events
        event_bus = events.EventBus(
            self, "OpsCopilotBus", event_bus_name="ops-copilot-bus"
        )

        # S3 bucket for runbooks
        runbooks_bucket = s3.Bucket(
            self,
            "CopilotRunbooks",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        # S3 bucket for artifacts
        artifacts_bucket = s3.Bucket(
            self,
            "CopilotArtifacts",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
        )

        # DynamoDB table for incident timeline
        incident_table = dynamodb.Table(
            self,
            "IncidentTimeline",
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="ts", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
        )

        # SNS topic for Slack notifications
        slack_topic = sns.Topic(self, "SlackNotifications")

        # IAM role for Lambda functions
        lambda_role = iam.Role(
            self,
            "CopilotLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        # Add permissions to the Lambda role
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=["*"],
            )
        )

        # Add S3 permissions
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject", "s3:PutObject"],
                resources=[
                    artifacts_bucket.arn_for_objects("*"),
                    runbooks_bucket.arn_for_objects("*"),
                ],
            )
        )

        # Add DynamoDB permissions
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:PutItem", "dynamodb:Query"],
                resources=[incident_table.table_arn],
            )
        )

        # Add SNS permissions
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["sns:Publish"], resources=[slack_topic.topic_arn]
            )
        )

        # Add EventBridge permissions
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"], resources=[event_bus.event_bus_arn]
            )
        )

        # Triager Lambda function
        triager_fn = _lambda.Function(
            self,
            "TriagerFn",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="triager.handler",
            code=_lambda.Code.from_asset("lambda/triager"),
            role=lambda_role,
            environment={
                "RUNBOOKS_BUCKET": runbooks_bucket.bucket_name,
                "DDB_TABLE": incident_table.table_name,
                "BEDROCK_MODEL": "anthropic.claude-v2",
                "FEATURE_BEDROCK": "false",
                "FEATURE_ATHENA": "false",
            },
            timeout=Duration.minutes(5),
        )

        # EventBridge rule to trigger Triager
        rule = events.Rule(
            self,
            "TriagerRule",
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=events.EventField.from_path("$.source")
            ),
        )
        rule.add_target(targets.LambdaFunction(triager_fn))

        # Approver Lambda function
        approver_fn = _lambda.Function(
            self,
            "ApproverFn",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="approver.handler",
            code=_lambda.Code.from_asset("lambda/approver"),
            role=lambda_role,
            environment={"DDB_TABLE": incident_table.table_name, "DRY_RUN": "true"},
            timeout=Duration.minutes(5),
        )

        # Add SSM permissions to approver function
        approver_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ssm:StartAutomationExecution", "ssm:GetAutomationExecution"],
                resources=["*"],
            )
        )

        # Add CloudWatch metrics permissions to approver function
        approver_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
                conditions={"StringEquals": {"cloudwatch:namespace": "CopilotOps"}},
            )
        )

        # SSM Document for safe actions
        ssm.CfnDocument(
            self,
            "CopilotSafeAction",
            content={
                "schemaVersion": "0.3",
                "description": "Sample action to increase provisioned concurrency on a named Lambda",
                "parameters": {
                    "FunctionName": {
                        "type": "String",
                        "description": "Name of the Lambda function",
                    },
                    "Concurrency": {
                        "type": "String",
                        "description": "New concurrency value",
                    },
                },
                "mainSteps": [
                    {
                        "name": "increaseConcurrency",
                        "action": "aws:lambda:putProvisionedConcurrencyConfig",
                        "inputs": {
                            "FunctionName": "{{FunctionName}}",
                            "Qualifier": "$LATEST",
                            "ProvisionedConcurrentExecutions": "{{Concurrency}}",
                        },
                    }
                ],
            },
            document_type="Automation",
        )

        # Chatbot configuration
        chatbot.SlackChannelConfiguration(
            self,
            "SlackChannel",
            slack_channel_configuration_name="ops-copilot-notifications",
            slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",  # Replace with actual workspace ID
            slack_channel_id="YOUR_SLACK_CHANNEL_ID",  # Replace with actual channel ID
            notification_topics=[slack_topic],
        )

        # CloudWatch dashboard
        logs.Dashboard(self, "CopilotDashboard", dashboard_name="ops-copilot-dashboard")

        # Outputs
        CfnOutput(
            self,
            "EventBusArn",
            value=event_bus.event_bus_arn,
            export_name="OpsCopilotEventBusArn",
        )

        CfnOutput(
            self,
            "RunbooksBucket",
            value=runbooks_bucket.bucket_name,
            export_name="OpsCopilotRunbooksBucket",
        )

        CfnOutput(
            self,
            "ArtifactsBucket",
            value=artifacts_bucket.bucket_name,
            export_name="OpsCopilotArtifactsBucket",
        )

        CfnOutput(
            self,
            "IncidentTable",
            value=incident_table.table_name,
            export_name="OpsCopilotIncidentTable",
        )
