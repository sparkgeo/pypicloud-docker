from types import SimpleNamespace
from aws_cdk import core, aws_s3 as s3, aws_iam as iam
import os


class SharedResourceStack(core.Stack):
    def __init__(
        self, scope: core.Construct, id: str, config: SimpleNamespace, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = "earth2-shared-dataset-storage"
        self.data_bucket = s3.Bucket(
            self,
            id=bucket_name,
            bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )
        self.data_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:Get*",
                    "s3:Put*",
                    "s3:List*",
                    "s3:Delete*",
                ],
                resources=[
                    self.data_bucket.bucket_arn,
                    # self.data_bucket.bucket_arn + "/",
                    # self.data_bucket.bucket_arn + "/*",
                ],
                principals=[iam.AccountRootPrincipal()],
            )
        )
