from aws_cdk import Stack
from constructs import Construct

from dev_instance.dev_instance_construct import DevInstance, DevInstanceOptions


class DevInstanceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_data = """
            #!/bin/bash
            sudo apt update -y
            sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

            # Add Docker
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
            sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
            apt-cache policy docker-ce
            sudo apt install -y docker-ce
            sudo usermod -aG docker ubuntu

            # Install github cli
            curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
                && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
                && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
                && sudo apt update \
                && sudo apt install gh -y
        """

        # If github_username is passed as context to the stack,
        # include the key from github in the authorized_keys
        # Example:
        # `cdk deploy -c github_username=YOUR_GITHUB_USERNAME``
        github_username=self.node.try_get_context("github_username")
        if github_username:
            user_data += f"""
                # Add public keys
                curl -sL https://github.com/{github_username}.keys >> /home/ubuntu/.ssh/authorized_keys
            """

        dev_instance_options = DevInstanceOptions(
            user_data=user_data
        )

        DevInstance(self, "DevInstance",
            options=dev_instance_options,
        )
