import boto3, os

# AWS S3 variables
s3_bucket_name = "ci-ms3-devbus"
s3_bucket_url = "https://{}.s3.eu-west-1.amazonaws.com/".format(s3_bucket_name)
client = boto3.client('s3',
                      aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.environ.get
                      ("AWS_SECRET_ACCESS_KEY"))

