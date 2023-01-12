import boto3
import os
import secrets
import io
import re
from flask import url_for
import smtplib
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
        raise Exception('''There was a problem uploading the
                        image to the AWS S3 bucket''')

    image_url = s3_bucket_url + image_name
    return image_url


def resize_image(file):
    # Open Image
    image = Image.open(file)
    image_w, image_h = image.size

    if image_w > image_h:
        image_diff = (image_w - image_h) / 2
        cropped_image = image.crop((image_diff, 0,
                                    image_w - image_diff, image_h))
    elif image_h > image_w:
        image_diff = (image_h - image_w) / 2
        cropped_image = image.crop((0, image_diff,
                                    image_w, image_h - image_diff))
    else:
        cropped_image = None

    # Set size tuple to which image should be resized to
    # Resize the image to dimensions from size var
    (cropped_image if cropped_image else image).thumbnail((350, 350),
                                                          Image.Resampling
                                                          .LANCZOS)
    # Save the image to an in-memory file
    to_memory = io.BytesIO()
    (cropped_image if cropped_image else image).save(to_memory,
                                                     format=image.format)
    to_memory.seek(0)

    return to_memory


def send_reset_email(user):
    token = user.generate_pwd_token()
    FROM = "noreply@devbus.com"
    TO = user.email
    SUBJECT = "Your Password Reset Instructions"
    message = f'''From: {FROM}\nTo: {TO}\nSubject: {SUBJECT}
Hey...happens to the best of us!

Click the link below to  reset your password and get back to the fun!

{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and
no changes will be made.'''
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(os.environ.get("EMAIL_USER"),
                     os.environ.get("EMAIL_PASS"))
        server.sendmail(FROM, TO, message)
        server.close()
    except BaseException as e:
        return False


def password_check(password):
    """
    https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-pass
    word-how-to-check-conditions#32542964
    Verify the strength of 'password' and return boolean.
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = (re
                    .search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]',
                            password) is None)

    # overall result
    password_ok = not (length_error
                       or digit_error
                       or uppercase_error
                       or lowercase_error
                       or symbol_error)
    return password_ok