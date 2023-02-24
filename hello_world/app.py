import json
import boto3
import uuid

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Provide an event that contains the following keys:
        - extension: extension of image to be uploaded
        - imageName: name of the image to be stored in s3
        - path: s3 path to store object

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    presignedUploadUrl = create_presigned_url("jd-tier-list-images", "test")

    guid = uuid.uuid4()

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json'
        },
        "body": json.dumps({
            "message": presignedUploadUrl,
            "guid": str(guid)
        }),
    }

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to upload an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response