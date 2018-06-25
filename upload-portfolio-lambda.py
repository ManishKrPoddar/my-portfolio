import boto3
from botocore.client import Config
import zipfile


def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

    build_bucket = s3.Bucket('portfoliobuild.manish.poddar.info')
    portfolio_bucket = s3.Bucket('portfolio.manishpoddar.in')

    # On Windows, this will need to be a different location than /tmp
    build_bucket.download_file('portfolio.zip', '/tmp/portfolio.zip')

    with zipfile.ZipFile('/tmp/portfolio.zip') as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm)
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    # TODO implement
    return 'Hello from Lambda'
