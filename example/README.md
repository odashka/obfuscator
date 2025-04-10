
```
$ open /Applications/Docker.app
$ localstack start -d
$ localstack status services
$ awslocal s3 mb s3://northcoders
$ awslocal s3 ls
$ awslocal s3 cp ../tests/students.csv s3://northcoders/development/students.csv
$ awslocal s3 ls s3://northcoders/development/students.csv
$ python main.py
$ awslocal s3 ls s3://northcoders/development/
$ awslocal s3 cp s3://northcoders/development/students_obfuscated.csv -
```