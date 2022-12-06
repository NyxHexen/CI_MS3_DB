import boto3, os, secrets, io
from botocore.exceptions import ClientError
from PIL import Image

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

    image = resize_image(file)

    # Generate random hex value
    random_hex = secrets.token_hex(8)
    # Using _ as throwaway variable
    _, file_ext = os.path.splitext(file.filename)
    # New image name using random hex value and
    # extension of file.
    image_name = random_hex + file_ext

    try:
        s3 = boto3.resource('s3')
        s3.Bucket(s3_bucket_name).put_object(
                Key=image_name,
                Body=image)
    except ClientError:
        raise Exception("There was a problem uploading the image to the AWS S3 bucket")
    
    image_url = s3_bucket_url + image_name
    return image_url


def resize_image(file):
    # Open Image
    image = Image.open(file)
    image_w, image_h = image.size

    if image_w > image_h:
        image_diff = (image_w - image_h) / 2
        cropped_image = image.crop((image_diff, 0, image_w - image_diff , image_h))
    elif image_h > image_w:
        image_diff = (image_h - image_w) / 2
        cropped_image = image.crop((0, image_diff, image_w, image_h - image_diff))
    else:
        cropped_image = None

    # Set size tuple to which image should be resized to
    # Resize the image to dimensions from size var
    (cropped_image if cropped_image else image).thumbnail((350, 350), Image.Resampling.LANCZOS)
    # Save the image to an in-memory file
    to_memory = io.BytesIO()
    (cropped_image if cropped_image else image).save(to_memory, format=image.format)
    to_memory.seek(0)

    return to_memory


