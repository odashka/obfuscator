# Obfuscator

A Python package to obfuscate CSV files at AWS S3. It takes object path and PII fields list as JSON string input and returns object compatible with S3 client PUT method as output.

## Usage

```shell
$ pip install git+https://github.com/odashka/obfuscator.git@v1.0.0
```

> [!WARNING]
> This packagae is not published to the standard Python Package Index (PyPI).
> You can find pre-built wheel package at GitHub repository [Releases](https://github.com/odashka/obfuscator/releases) page.

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
git clone https://github.com/odashka/obfuscator
cd obfuscator
make install_local
python -c "import obfuscator; obfuscator.obfuscate('...')"
```

### Debugging

```shell
LOG_LEVEL=DEBUG python -c "import obfuscator; obfuscator.obfuscate('...')"
```

## Test (MacOS)

### Requirements

```shell
make install_deps
```

### All

```shell
make test_all
```


### Unit

```shell
$ make test_unit
```

### Integration

```shell
make test_integration
```

### Check LocalStack S3 state

```shell
awslocal s3 ls                                                     # Check bucket list
awslocal s3 ls s3://northcoders/new-data/                          # Check bucket folder
awslocal s3 cp s3://northcoders/new-data/students_obfuscated.csv - # Check object content
```
