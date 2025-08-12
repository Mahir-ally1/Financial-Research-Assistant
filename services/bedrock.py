import boto3
from botocore.config import Config

from config.settings import settings

def _session():
    if settings.aws_profile:
        return boto3.Session(profile_name=settings.aws_profile, region_name=settings.aws_region)
    return boto3.Session(region_name=settings.aws_region)

def bedrock_client():
    return _session().client(
        "bedrock-runtime",
        region_name=settings.aws_region,
        config=Config(retries={"max_attempts": 3, "mode": "adaptive"}),
    )

def converse_json(messages, max_tokens=512, temperature=0.5, top_p=0.9) -> str:
    brt = bedrock_client()
    resp = brt.converse(
        modelId=settings.model_id,
        messages=messages,
        inferenceConfig={"maxTokens": max_tokens, "temperature": temperature, "topP": top_p},
    )
    return resp["output"]["message"]["content"][0]["text"]
