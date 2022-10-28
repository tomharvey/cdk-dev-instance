
# CDK Dev Instance

This will create an EC2 instance running docker, ready for you to connect to and
use with VSCode's dev containers

To deploy:

    ```
    cdk deploy -c github_username=$YOUR_GITHUB_USERNAME
    ```

(Optionally_ Supply your github username and the EC2 instance will download your
public key from github and add it to authorized_keys so you can ssh into the instance.

By default, this will provision:
    * m6i.large (2CPU 8GB RAM)
    * 80GB Disk

The instance will have AdministratorAccess to your AWS account, so any user accessing the instance
will be able to make Admin level API calls.

##### To delete

When you're finished you can run `cdk destroy` to remove all the resources.

This will delete the volume, so make sure you push any work to GitHub, S3 or some other
persistent storage.

### Connecting with AWS Session Manager
To connect to the instance you can use AWS's Session Manager

https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started.html


##### SSH access through SSM

Add the below to your `~/.ssh/config` file:


```
Host i-*
  ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```

##### Port forwarding
Using session manager you can forward a remote port to your local machine:

The below example will put the remote port 22 on your local port 2222
```
aws ssm start-session \
    --target $AWS_INSTANCE_ID \
    --document-name AWS-StartPortForwardingSession \
    --parameters '{"portNumber":["22"], "localPortNumber":["2222"]}'

```
