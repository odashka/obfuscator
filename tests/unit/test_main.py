import pytest
import os
import io
import json
import jsonschema
import boto3
from moto import mock_aws
from src.obfuscator.main import obfuscate

BUCKET = "mock-bucket"
KEY = "new-data/students.csv"

@pytest.fixture()
def s3_moto():
    with mock_aws():
        os.environ.pop("AWS_ENDPOINT_URL", None)
        
        s3_client = boto3.client("s3", region_name="us-east-1")

        s3_client.create_bucket(Bucket=BUCKET)

        with open('tests/students.csv', 'r') as file:
            s3_client.put_object(
                Bucket=BUCKET,
                Key=KEY,
                Body=file.read(),
                ContentType="application/csv",
            )

        yield s3_client

def test_obfuscate_returns_isntance_of_bytes_io(s3_moto):
    result = obfuscate(json.dumps(
        {
            "file_to_obfuscate": f"s3://{BUCKET}/{KEY}",
            "pii_fields": [
                "name",
                "email_address"
            ]
        }
    ))
    assert isinstance(result, io.BytesIO) # io.BytesIO is compatibale with boto3.client.S3.put_object() method

def test_obfuscate_returns_obfuscated_pii_fields(s3_moto):
    result = obfuscate(json.dumps(
        {
            "file_to_obfuscate": f"s3://{BUCKET}/{KEY}",
            "pii_fields": [
                "name",
                "email_address"
            ]
        }
    ))
    with open('tests/students_obfuscated.csv', 'r') as file:
        assert result.getvalue().decode("utf-8") == file.read()
             # BytesIO -> string   File -> string

def test_obfuscate_raises_error_on_malformed_json():
    with pytest.raises(json.JSONDecodeError):
        obfuscate("invalid JSON")

def test_obfuscate_raises_error_on_invalid_jsonschema_empty_object():
    with pytest.raises(jsonschema.ValidationError):
        obfuscate("{}")

def test_obfuscate_raises_error_on_invalid_jsonschema_missing_pii_fields():
    with pytest.raises(jsonschema.ValidationError):
        obfuscate("""
        {
            "file_to_obfuscate": "s3://bucket/object"
        }
        """)

def test_obfuscate_raises_error_on_invalid_jsonschema_missing_file_to_obfuscate():
    with pytest.raises(jsonschema.ValidationError):
        obfuscate("""
        {
            "pii_fields": ["name", "email_address"]
        }
        """)

def test_obfuscate_raises_error_on_invalid_jsonschema_wrong_value_type():
    with pytest.raises(jsonschema.ValidationError):
        obfuscate("""
        {
            "file_to_obfuscate": 123,
            "pii_fields": ["name", "email_address"]
        }
        """)

def test_obfuscate_raises_error_on_invalid_jsonschema_malformed_url():
    with pytest.raises(jsonschema.ValidationError):
        obfuscate("""
        {
            "file_to_obfuscate": "=abrakadabra=",
            "pii_fields": ["name", "email_address"]
        }
        """)

    with pytest.raises(jsonschema.ValidationError):
        obfuscate("""
        {
            "file_to_obfuscate": "",
            "pii_fields": ["name", "email_address"]
        }
        """)

def test_obfuscate_raises_error_on_nonexistent_object_retrieval(s3_moto):
    with pytest.raises(s3_moto.exceptions.NoSuchKey):
        obfuscate(json.dumps(
            {
                "file_to_obfuscate": f"s3://{BUCKET}/nonexistent",
                "pii_fields": [
                    "name",
                    "email_address"
                ]
            }
        ))
