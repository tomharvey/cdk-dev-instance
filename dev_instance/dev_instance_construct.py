from aws_cdk import (
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct
from dataclasses import dataclass


@dataclass
class DevInstanceOptions:
    ami: ec2.MachineImage = ec2.MachineImage.from_ssm_parameter(
        # Ubuntu 22.04 LTS (HVM)
        "/aws/service/canonical/ubuntu/server/jammy/stable/current/amd64/hvm/ebs-gp2/ami-id",
        os=ec2.OperatingSystemType.LINUX,
    )
    grant_admin_privileges: bool = True
    instance_type: str = "m6i.large"
    open_ssh: bool = False
    use_default_vpc: bool = True
    user_data: str = ""
    volume_name: str = "/dev/sda1"
    volume_size: int = 80


class DevInstance(Construct):
    def __init__(self, scope: Construct, construct_id: str, options: DevInstanceOptions, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, f"{construct_id}-VPC",
            is_default=options.use_default_vpc
        )

        instance = ec2.Instance(self, f"{construct_id}-DevInstance",
            instance_type=ec2.InstanceType(options.instance_type),
            machine_image=options.ami,
            block_devices=[
                ec2.BlockDevice(
                    device_name=options.volume_name,
                    volume=ec2.BlockDeviceVolume.ebs(options.volume_size),
                )
            ],
            vpc=vpc,
            user_data=ec2.UserData.custom(options.user_data)
        )
        self.instance = instance

        # Allow SSM access
        instance.role.add_managed_policy(
            policy=iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )

        if options.grant_admin_privileges:
            instance.role.add_managed_policy(
                policy=iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            )

        if options.open_ssh:
            instance.connections.allow_from_any_ipv4(port_range=ec2.Port.tcp(22), description="Allow SSH from anywhere")

        CfnOutput(self, "InstancePublicIp", value=instance.instance_public_ip)
        CfnOutput(self, "InstanceId", value=instance.instance_id)
