import os
import json
import jsonschema
import csv
import io
import boto3
import logging
from urllib.parse import urlparse

logger = logging.getLogger("obfuscator")
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logger.setLevel(log_level)

schema = {
    "type": "object",
    "properties": {
        "file_to_obfuscate": {
            "type": "string",
            "pattern": r"^s3://[^/]+(/.*)?$"
        },
        "pii_fields": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["file_to_obfuscate", "pii_fields"],
    "additionalProperties": False
}


def obfuscate(input):
    # TODO: add docstring
    params = json.loads(input)
    jsonschema.validate(params, schema)
    logger.debug(f"pramas: {params}")

    url = params['file_to_obfuscate']

    parsed_url = urlparse(url)
    bucket = parsed_url.netloc
    key = parsed_url.path.lstrip("/")

    pii_fields = params['pii_fields']

    string_buffer = io.StringIO()

    s3_client = boto3.client("s3")

    s3_object = s3_client.get_object(
        Bucket=bucket,
        Key=key
    )

    # NOTE: Wrap string object into StringIO object to satisfy csv.DictReader() protocol
    content = io.StringIO(s3_object["Body"].read().decode("utf-8"))

    csv_reader = csv.DictReader(content)
    csv_writer = csv.DictWriter(string_buffer, fieldnames=csv_reader.fieldnames, lineterminator='\n')

    csv_writer.writeheader()

    for row in csv_reader:
        for field in pii_fields:
            row[field] = "***"
        csv_writer.writerow(row)  # "\r\n"

    output = string_buffer.getvalue()
    logger.debug(f"output: {output}")

    bytes_buffer = io.BytesIO(output.encode("utf-8"))

    return bytes_buffer
