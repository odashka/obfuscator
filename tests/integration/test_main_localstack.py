import pytest
import os
import json
import boto3
from src.obfuscator.main import obfuscate

BUCKET = "northcoders"
INPUT_KEY = "new-data/students.csv"
OUTPUT_KEY = "new-data/students_obfuscated.csv"

@pytest.fixture()
def s3_localstack():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ENDPOINT_URL"] = "http://localhost:4566"

    s3_client = boto3.client("s3")

    s3_client.create_bucket(Bucket=BUCKET)

    with open('tests/students.csv', 'r') as file:
        s3_client.put_object(
            Bucket=BUCKET,
            Key=INPUT_KEY,
            Body=file.read(),
            ContentType="application/csv",
        )

    yield s3_client

    s3_client.delete_object(Bucket=BUCKET, Key=INPUT_KEY)
    s3_client.delete_object(Bucket=BUCKET, Key=OUTPUT_KEY)
    s3_client.delete_bucket(Bucket=BUCKET)

    os.environ.pop("AWS_ACCESS_KEY_ID", None)
    os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
    os.environ.pop("AWS_DEFAULT_REGION", None)
    os.environ.pop("AWS_ENDPOINT_URL", None)

@pytest.mark.integration
def test_obfuscate_happy_path(s3_localstack):
    result = obfuscate(json.dumps(
        {
            "file_to_obfuscate": f"s3://{BUCKET}/{INPUT_KEY}",
            "pii_fields": [
                "name",
                "email_address"
            ]
        }
    ))

    s3_localstack.put_object(
        Bucket=BUCKET,
        Key=OUTPUT_KEY,
        Body=result,
        ContentType="application/csv",
    )

    s3_object = s3_localstack.get_object(
        Bucket=BUCKET,
        Key=OUTPUT_KEY,
    )

    with open('tests/students_obfuscated.csv', 'r') as file:
        assert s3_object["Body"].read().decode("utf-8") == file.read()
             # BytesIO -> string   File -> string

    
