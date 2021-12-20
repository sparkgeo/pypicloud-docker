import os

from aws_cdk import App, Environment

from stacks.cicd_user import CICDStack
from stacks.main import MainStack


tags = {
    "Owner": "dev@sparkgeo.com",
    "Environment": "sparkgeo-main",
    "Git Branch": "master",
    "Project": "PyPi",
    "Repo": "https://github.com/sparkgeo/pypicloud-docker",
}

env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)

app = App()

# User for Github actions
cicd_user = CICDStack(app, f"PyPiCICDUserStack", env=env, tags=tags)

pypi = MainStack(app, f"PyPiMainStack", env=env, tags=tags)

app.synth()
