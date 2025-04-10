import os
import boto3
import json
from obfuscator import obfuscate

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ENDPOINT_URL"] = "http://localhost:4566"

BUCKET = "northcoders"
KEY = "development/students.csv"

bytes_buffer = obfuscate(json.dumps(
    {
        "file_to_obfuscate": f"s3://{BUCKET}/{KEY}",
        "pii_fields": [
            "name",
            "email_address"
        ]
    }
))

boto3.client("s3").put_object(
    Bucket=BUCKET,
    Key=f"{KEY}_obfuscated.csv",
    Body=bytes_buffer,
    ContentType="application/csv",
)

