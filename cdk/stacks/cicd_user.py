"""

This stack is for creating the CI/CD user for use with Github actions.
When starting a new project, the sequence is as follows (assuming aws creds are set):

- cdk bootstrap
- cdk deploy CICDUser
- Go to AWS IAM console, and create an access key for the user. 
- Enter the new access key and secret into the project repo scerets.
- Push all changes, and Github actions will be start doing all further deploys.

"""
from constructs import Construct
from aws_cdk import (
    Stack,
    Arn,
    ArnComponents,
    aws_iam as iam
)


class CICDStack(Stack):
    def __init__(
        self, scope: Construct, id: str, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        cicd_user = iam.User(
            self,
            "CiCdUser",
        )

        cdk_policy = iam.Policy(
            self,
            "CdkDeployPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "sts:AssumeRole",
                        "sts:TagSession",
                    ],
                    resources=[
                        Arn.format(
                            components=ArnComponents(
                                service="iam",
                                region="",
                                resource="role",
                                resource_name="cdk-*"
                            ),
                            stack=self
                        ),
                    ],
                )
            ],
            users=[cicd_user]
        )