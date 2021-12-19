import os

from aws_cdk import App

from stacks.cicd_user import CICDStack
from stacks.main import MainStack


tags = {
    "Owner": "dev@sparkgeo.com",
    "Environment": "sparkgeo-main",
    "Git Branch": "master",
    "Project": "PyPi",
    "Repo": "https://github.com/sparkgeo/pypicloud-docker"
}


app = App()

# User for Github actions
cicd_user = CICDStack(app, f"PyPiCICDUserStack", tags=tags)

pypi = MainStack(app, f"PyPiMainStack", tags=tags)

app.synth()
