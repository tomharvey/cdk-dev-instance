import aws_cdk as core
import aws_cdk.assertions as assertions

from dev_instance.dev_instance_stack import DevInstanceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in dev_instance/dev_instance_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DevInstanceStack(app, "dev-instance")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
