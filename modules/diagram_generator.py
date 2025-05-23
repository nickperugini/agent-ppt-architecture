
from diagrams import Diagram
from diagrams.aws.compute import Lambda, ECS
from diagrams.aws.integration import StepFunctions, Eventbridge
from diagrams.aws.network import APIGateway, ELB, VPC
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.onprem.client import Users

def generate_architecture_diagram(components: set, filename="solution_architecture"):
    filepath = f"{filename}.png"
    with Diagram("Serverless Architecture", show=False, filename=filename, outformat="png"):
        nodes = {}
        if "Client" in components:
            nodes["Client"] = Users("Client")
        if "APIGateway" in components:
            nodes["APIGateway"] = APIGateway("API Gateway")
        if "Lambda" in components:
            nodes["Lambda"] = Lambda("Lambda")
        if "S3" in components:
            nodes["S3"] = S3("S3 Bucket")
        if "DynamoDB" in components:
            nodes["DynamoDB"] = Dynamodb("DynamoDB")
        if "VPC" in components:
            nodes["VPC"] = VPC("VPC")
        if "ALB" in components:
            nodes["ALB"] = ELB("ALB")
        if "ECS" in components:
            nodes["ECS"] = ECS("ECS Cluster")
        if "StepFunctions" in components:
            nodes["StepFunctions"] = StepFunctions("Step Functions")
        if "EventBridge" in components:
            nodes["EventBridge"] = Eventbridge("EventBridge")

        if "Client" in nodes and "APIGateway" in nodes:
            nodes["Client"] >> nodes["APIGateway"]
        if "APIGateway" in nodes and "Lambda" in nodes:
            nodes["APIGateway"] >> nodes["Lambda"]
        if "Lambda" in nodes:
            for target in ["S3", "DynamoDB", "VPC", "ALB", "ECS", "StepFunctions", "EventBridge"]:
                if target in nodes:
                    nodes["Lambda"] >> nodes[target]

    return filepath
