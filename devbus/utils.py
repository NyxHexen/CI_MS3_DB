import boto3, os, secrets
from botocore.exceptions import ClientError

# AWS S3 variables
s3_bucket_name = "ci-ms3-devbus"
s3_bucket_url = "https://{}.s3.eu-west-1.amazonaws.com/".format(s3_bucket_name)
client = boto3.client('s3',
                      aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.environ.get
                      ("AWS_SECRET_ACCESS_KEY"))


def upload_image(file):
    """
    Store a file on the AWS S3 bucket using boto3.
    The function renames the file to a random hex and
    tries to upload it to the bucket. If successful, returns
    the link to the image to be stored in DB.
    """
    random_hex = secrets.token_hex(8)
    # Using _ as throwaway variable
    _, file_ext = os.path.splitext(file.filename)
    image_name = random_hex + file_ext

    try:
        s3 = boto3.resource('s3')
        s3.Bucket(s3_bucket_name).put_object(
                Key=image_name,
                Body=file)
    except ClientError:
        raise Exception("There was a problem uploading the image to the AWS S3 bucket")
    
    image_url = s3_bucket_url + image_name
    return image_url