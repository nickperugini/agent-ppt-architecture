
import re
import os

def read_all_code(base_path="./repo"):
    code = ""
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith((".py", ".tf", ".yml", ".yaml", ".json", ".js", ".ts")):
                try:
                    with open(os.path.join(root, file), encoding="utf-8") as f:
                        code += f"\n# File: {file}\n" + f.read()
                except Exception as e:
                    code += f"\n# Error reading {file}: {e}\n"
    return code

def detect_components_regex(code_text: str) -> set:
    components = {"Client"}
    checks = {
        "APIGateway": [r"event\['httpMethod'\]", r"aws_apigateway", r"apigatewayv2"],
        "Lambda": [r"def lambda_handler", r"aws_lambda_function", r"arn:aws:lambda"],
        "S3": [r"boto3\.client\(['\"]s3['\"]", r"aws_s3_bucket", r"upload_file", r"put_object"],
        "DynamoDB": [r"boto3\.client\(['\"]dynamodb['\"]", r"aws_dynamodb_table"],
        "VPC": [r"aws_vpc", r"vpc_config", r"subnet", r"lambda_subnet_ids"],
        "ALB": [r"aws_lb", r"aws_alb", r"boto3\.client\(['\"]elbv2['\"]"],
        "ECS": [r"aws_ecs", r"boto3\.client\(['\"]ecs['\"]"],
        "StepFunctions": [r"boto3\.client\(['\"]stepfunctions['\"]", r"aws_sfn"],
        "EventBridge": [r"boto3\.client\(['\"]events['\"]", r"eventbridge"]
    }
    for key, patterns in checks.items():
        for pattern in patterns:
            if re.search(pattern, code_text, re.IGNORECASE):
                components.add(key)
                break
    return components

def detect_components_llm(code_text: str, llm) -> set:
    response = llm.invoke(f"Which AWS services or components (e.g., Lambda, S3, API Gateway, VPC, ECS, Step Functions, EventBridge, etc.) are used in this code? Just return a list of component names:\n\n{code_text[:5000]}")
    response_text = response.content.lower() if hasattr(response, "content") else str(response).lower()
    components = {"Client"}
    keywords = {
        "lambda": "Lambda",
        "s3": "S3",
        "api gateway": "APIGateway",
        "dynamodb": "DynamoDB",
        "vpc": "VPC",
        "alb": "ALB",
        "ecs": "ECS",
        "step functions": "StepFunctions",
        "stepfunctions": "StepFunctions",
        "eventbridge": "EventBridge",
        "event bus": "EventBridge"
    }
    for word, comp in keywords.items():
        if word in response_text:
            components.add(comp)
    return components
