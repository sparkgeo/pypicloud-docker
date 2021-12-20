from constructs import Construct
from aws_cdk import (
    Stack,
    aws_batch as batch,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as patterns,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elb,
    aws_route53 as r53,
    aws_efs as efs,
)


class MainStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "Vpc",
        )

        pypi = patterns.ApplicationLoadBalancedFargateService(
            self,
            id="PyPiService",
            platform_version=ecs.FargatePlatformVersion.VERSION1_4,
            cluster=ecs.Cluster(
                self,
                f"Cluster",
                vpc=vpc,
                container_insights=True,
            ),
            cpu=2,
            memory_limit_mib=4096,
            desired_count=1,
            protocol=elb.ApplicationProtocol.HTTPS,
            domain_zone=r53.HostedZone.from_lookup(
                self, id="HostedZone", domain_name="sparkgeo.dev"
            ),
            domain_name="pypi.sparkge.dev",
            redirect_http=True,
            task_image_options=patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../py3-baseimage"),
                container_port=8080,
                # environment={
                #     "PGADMIN_DEFAULT_EMAIL": "dev@sparkgeo.com",
                #     "PGADMIN_LISTEN_PORT": "5050",
                # },
                # secrets={
                #     "PGADMIN_DEFAULT_PASSWORD": "",
                # },
                enable_logging=True,
                # log_driver=ecs.LogDrivers.aws_logs(
                #     stream_prefix=svc, log_group=log_group
                # ),
            ),
        )

        file_system = efs.FileSystem(
            self,
            "PyPifileSystem",
            vpc=vpc,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING
        )

        accessPoint = file_system.add_access_point(
            "AccessPoint",
            path="/pypicloud",
            posix_user=efs.PosixUser(
                uid="999",
                gid="999",
            ),
            create_acl=efs.Acl(owner_gid="999", owner_uid="999", permissions="755"),
        )

        pypi.service.task_definition.add_volume(
            name="pypi-cloud",
            efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=file_system.file_system_id,
                transit_encryption="ENABLED",
                authorization_config=ecs.AuthorizationConfig(
                    access_point_id=accessPoint.access_point_id, iam="ENABLED"
                ),
            ),
        )

        pypi.service.connections.allow_from(file_system, ec2.Port.tcp(2049))
        pypi.service.connections.allow_to(file_system, ec2.Port.tcp(2049))
