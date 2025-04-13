# Obfuscator

A Python package to obfuscate CSV files at AWS S3. It takes object path and PII fields list as JSON string input and returns object compatible with S3 client PUT method as output.

## Usage

> [!WARNING]
> This packagae is not published to the standard Python Package Index (PyPI). You can find pre-built package at GitHub repository [Releases](https://github.com/odashka/obfuscator/releases) page.

```shell
$ pip install ~/Downloads/obfuscator-1.0.0-py3-none-any.whl
```

Make sure AWS credentials are available for Python AWS SDK (`boto3`).

```python
from obfuscator import obfuscate

obfuscate("""
{
    "file_to_obfuscate": "s3://bucket/object",
    "pii_fields": ["name", "email_address"]
}
""")
```

## Development

```shell
$ git clone https://github.com/odashka/obfuscator
$ cd obfuscator
$ pip install .
$ python -c "import obfuscator; obfuscator.obfuscate('...')"
```

### Debugging

```shell
LOG_LEVEL=DEBUG python -c "import obfuscator; obfuscator.obfuscate('...')" 
```

## Test

### Requirements (MacOS)

```
$ brew install --cask docker                  # Install Docker (for Mac) containers envrionments
$ brew install localstack                     # Install LocalStack
$ brew install localstack/tap/localstack-cli  # Install LocalStack CLI to run simulation
$ brew install awscli-local                   # Install AWS CLI for local usage
```

### Unit

#### Run unit tests

```
$ pytest test/unit 
```

### Integration

#### Start LocalStack

```
$ open /Applications/Docker.app # Start Docker
$ localstack start -d           # Start LocalStack
$ localstack status services    # Check LocalStack services availability status
```

#### Run integration tests

```
$ export PYTHONPATH=$(pwd)
$ pytest test/integration
```

#### Check LocalStack S3 state

```
$ awslocal s3 ls                                                     # Check bucket list
$ awslocal s3 ls s3://northcoders/new-data/                          # Check bucket folder
$ awslocal s3 cp s3://northcoders/new-data/students_obfuscated.csv - # Check object content
```

### All

#### Run all tests with print output

```
$ pytest -vvvrP tests
```